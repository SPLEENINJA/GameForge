from celery import shared_task
from transformers import pipeline
import json

generator = pipeline(
    "text-generation",
    model="distilbert/distilgpt2",
    device_map="auto",   # gère CPU/GPU automatiquement
    trust_remote_code=True,  # si le modèle a du code custom
    max_new_tokens=600,
    temperature=0.7
)

@shared_task
def generate_characters(scenario_data: dict):
    """
    Crée entre 3 personnages cohérents avec le scénario.
    Inclut aspects narratifs et gameplay.
    """
    prompt = f"""
    À partir de ce scénario :
    {json.dumps(scenario_data, ensure_ascii=False, indent=2)}

    Génère entre 3 personnages au format JSON :
    {{
      "personnages": [
        {{
          "nom": str,
          "classe": str,
          "rôle_narratif": str,
          "background": str,
          "compétences_gameplay": [str]
        }}
      ]
    }}
    """

    result = generator(prompt, max_new_tokens=700, temperature=0.8)[0]["generated_text"]
    try:
        return json.loads(result)
    except Exception:
        return {"error": "JSON invalide", "raw_output": result}
