# api/tasks.py
import os
import json
from celery import shared_task
from django.core.files.base import ContentFile
from .models import GameProject, Asset, Character
from .ai_clients import call_text_model_and_parse, generate_image_from_prompt

@shared_task(bind=True, max_retries=2)
def generate_full_project_task(self, project_id):
    try:
        project = GameProject.objects.get(id=project_id)
        project.ai_generation_status = "processing"
        project.save()

        # Build prompt from project fields
        prompt = f"""Generate a JSON object with fields: title, universe, story, characters (2-4), pitch_deck.
User inputs:
genre: {project.genre}
visual_style: {project.visual_style}
keywords: {project.keywords}
"""
        parsed = call_text_model_and_parse(prompt)

        # store text outputs
        project.title = parsed.get("title", project.title)
        project.universe_text = parsed.get("universe")
        project.story_text = parsed.get("story")
        project.pitch_deck = parsed.get("pitch_deck")
        project.save()

        # characters
        chars = parsed.get("characters", [])
        for c in chars:
            ch = Character.objects.create(
                project=project,
                name=c.get("name", "Anon"),
                role=c.get("role", ""),
                char_class=c.get("class", ""),
                background=c.get("background", ""),
                gameplay_style=c.get("gameplay_style", ""),
            )
            # optional: generate an image per character
            img_prompt = f"{project.visual_style} portrait of {ch.name}, {ch.role}, {ch.background}"
            b64 = generate_image_from_prompt(img_prompt)  # returns bytes
            if b64:
                # save image to Asset
                file_content = ContentFile(b64, name=f"{project.id}_{ch.name}.png")
                asset = Asset.objects.create(project=project, file=file_content, purpose="character_art", generated_by="stable-diffusion")
                ch.art = asset
                ch.save()

        project.ai_generation_status = "done"
        project.save()
    except Exception as exc:
        project.ai_generation_status = "error"
        project.ai_error = str(exc)
        project.save()
        raise self.retry(exc=exc, countdown=10)
