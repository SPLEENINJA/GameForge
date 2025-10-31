# api/ai_clients.py
import os
import json
import requests
from base64 import b64decode

HF_API_KEY = os.getenv("HF_API_KEY")

def call_text_model_and_parse(prompt: str):
    """
    Call an LLM via Hugging Face Inference API and parse JSON output.
    This is a simple implementation — adapt to your chosen model's response shape.
    Ensure you set HF_API_KEY in env.
    """
    API_URL = "https://api-inference.huggingface.co/models/gpt2"  # replace with a suitable HF model or your LLM endpoint
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 800, "temperature": 0.9}}
    r = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    text = r.json()[0].get("generated_text") if isinstance(r.json(), list) else r.json().get("generated_text", "")
    # Attempt to find JSON inside text — naive approach
    try:
        # If model returns JSON directly:
        return json.loads(text)
    except Exception:
        # fallback: try to extract {...} substring
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            try:
                return json.loads(text[start:end+1])
            except Exception:
                pass
    # final fallback: return simple defaults
    return {
        "title": "Untitled Game",
        "universe": {"genre": "", "atmosphere": "", "visual_style": ""},
        "main_story": {"act1": "", "act2": "", "act3": ""},
        "characters": [],
        "pitch_deck": []
    }

def generate_image_from_prompt(prompt: str):
    """
    Call an image model and return raw bytes of a PNG (or None on failure).
    Replace with real provider (Stability, HF diffusers endpoints, or replicate).
    This stub returns None so you don't accidentally hit APIs.
    """
    # Example for HF's image API would go here.
    return None
