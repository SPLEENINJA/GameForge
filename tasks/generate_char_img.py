# tasks/generate_char_img.py
from celery import shared_task
import json
import os
import io, base64

# Pipeline variable globale (sera initialisée à la première exécution)
_generator = None

def _init_local_generator():
    """Initialise la pipeline localement. Peut télécharger le modèle la première fois."""
    global _generator
    if _generator is not None:
        return _generator

    # Choix 1 : local (diffusers). Nécessite diffusers, accelerate, torch...
    try:
        from diffusers import StableDiffusionPipeline
        import torch
        model_id = "runwayml/stable-diffusion-v1-5"  # modèle plus standard
        pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32)
        if torch.cuda.is_available():
            pipe.to("cuda")
        else:
            pipe.to("cpu")
        _generator = pipe
        return _generator
    except Exception:
        _generator = None
        return None

def _call_hf_api(prompt):
    """Fallback : requêter HF Inference API (rapide à mettre en place)."""
    import requests
    HF_TOKEN = os.getenv("HF_API_TOKEN")
    if not HF_TOKEN:
        raise RuntimeError("HF_API_TOKEN non défini pour fallback API")
    API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": prompt}
    resp = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    # réponse peut être image(s) en base64 selon le endpoint ; adapter si nécessaire
    return resp.content

@shared_task(bind=True)
def generate_char_img(self, characters_data: dict):
    """
    Génère 1 image par personnage et renvoie {nom: image_base64}.
    Lazy init du modèle : évite téléchargement au moment de l'import.
    """
    output = {}

    # Récupère le générateur local si possible
    gen = _init_local_generator()

    for char in characters_data.get("personnages", []):
        prompt = (
            f"Portrait détaillé de {char.get('nom')}. "
            f"Rôle: {char.get('rôle_narratif', '')}. "
            f"Background: {char.get('background', '')}. "
            f"Classe: {char.get('classe', '')}. Style: réaliste, haute qualité."
        )

        # Si on a le pipeline local
        if gen is not None:
            # diffusers pipeline return PIL image
            image = gen(prompt, num_inference_steps=25).images[0]
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            img_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
            output[char['nom']] = img_b64
        else:
            # fallback : HF Inference API (renvoie raw bytes)
            try:
                img_bytes = _call_hf_api(prompt)
                img_b64 = base64.b64encode(img_bytes).decode("utf-8")
                output[char['nom']] = img_b64
            except Exception as e:
                output[char['nom']] = {"error": str(e)}

    return output
