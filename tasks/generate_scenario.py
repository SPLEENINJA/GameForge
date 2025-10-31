from celery import shared_task
from transformers import pipeline
import json

generator = pipeline(
    "text-generation",
    model="distilbert/distilgpt2",
    device_map="auto",
    trust_remote_code=True
)

@shared_task
def generate_scenario(universe_json: dict):
    """
    Génère un scénario 3 actes basé sur l'univers fourni.
    Input : JSON output de generate_universe
    Output : JSON structuré avec acte_1, acte_2, acte_3
    """
    prompt = f"""
    À partir de cet univers :
    {json.dumps(universe_json, ensure_ascii=False, indent=2)}

    Génère un scénario narratif structuré en JSON :
    {{
      "titre": str,
      "acte_1": {{"résumé": str, "objectif": str, "conflit": str}},
      "acte_2": {{"résumé": str, "retournement": str, "évolution_personnages": str}},
      "acte_3": {{"résumé": str, "dénouement": str, "message_final": str}}
    }}
    """
    result = generator(prompt, max_new_tokens=800, temperature=0.7)
    try:
        return json.loads(result[0]["generated_text"])
    except Exception:
        return {"error": "JSON invalide", "raw_output": result[0]["generated_text"]}
