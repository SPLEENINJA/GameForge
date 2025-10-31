from celery import shared_task
from transformers import pipeline
import json

# Initialiser le modèle une seule fois (chargé au démarrage du worker)
# DavidAU/OpenAi-GPT-oss-20b-abliterated-uncensored-NEO-Imatrix-gguf
generator = pipeline(
    "text-generation",
    model="distilbert/distilgpt2",
    device_map="auto",   # gère CPU/GPU automatiquement
    trust_remote_code=True,  # si le modèle a du code custom
    max_new_tokens=600,
    temperature=0.7
)



@shared_task
def generate_universe(user_data: dict):
    prompt = f"""
    Crée un univers de jeu vidéo cohérent basé sur :
    - Genre : {user_data.get('genre')}
    - Ambiance : {user_data.get('ambiance')}
    - Mots-clés : {', '.join(user_data.get('mots_cles', []))}
    - Références : {', '.join(user_data.get('references', []))}

    Réponds uniquement en JSON structuré :
    {{
        "titre": str,
        "pitch": str,
        "monde": {{
            "description": str,
            "technologie": str,
            "société": str,
            "conflit_central": str
        }},
        "thèmes_majeurs": [str]
    }}
    """

    result = generator(prompt, max_new_tokens=600, temperature=0.8)[0]["generated_text"]

    try:
        return json.loads(result)
    except Exception:
        return {"error": "JSON invalide", "raw_output": result}
