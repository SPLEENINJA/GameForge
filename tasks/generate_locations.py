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
def generate_locations(scenario_data: dict):
    """
    Génère 2 lieux emblématiques avec descriptions immersives courtes et incitative à découvrir le jeu.
    Reliés à l univers et au scénario.
    """
    prompt = f"""
    À partir de ce scénario et de son univers :
    {json.dumps(scenario_data, ensure_ascii=False, indent=2)}

    Crée un JSON structuré :
    {{
      "lieux": [
        {{
          "nom": str,
          "type": str,
          "description": str,
          "importance_narrative": str
        }}
      ]
    }}
    """

    result = generator(prompt, max_new_tokens=700, temperature=0.8)[0]["generated_text"]
    try:
        return json.loads(result)
    except Exception:
        return {"error": "JSON invalide", "raw_output": result}
