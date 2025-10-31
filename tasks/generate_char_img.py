from celery import shared_task
from transformers import pipeline
import json

generator = pipeline(
    "image-generation",
    model="CompVis/stable-diffusion-v1-4",
    device_map="auto",
    trust_remote_code=True,
)

@shared_task
def generate_char_img(characters_data: dict):
    """
    Génère 1 image par personnage selon son background et rôle.
    Retourne un dict {nom_personnage: image_b64}.
    """
    output = {}
    for char in characters_data.get("personnages", []):
        prompt = f"""
        Crée un portrait détaillé de {char['nom']} :
        rôle narratif : {char.get('rôle_narratif', '')}
        background : {char.get('background', '')}
        classe : {char.get('classe', '')}
        style artistique réaliste, haute qualité.
        """
        # Génération
        images = generator(prompt, num_inference_steps=25)  # peut être ajusté
        # images[0]['image'] est un objet PIL.Image
        # ici on convertit en base64 pour stockage/JSON
        import io, base64
        buf = io.BytesIO()
        images[0]['image'].save(buf, format="PNG")
        img_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        output[char['nom']] = img_b64

    return output