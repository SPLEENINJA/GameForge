# api/orchestrator.py

def generate_game_concept(title, genre, theme, inspiration):
    """
    Stub function for orchestrator.
    Returns a dummy game concept. Later replace with real AI calls.
    """
    return {
        "id": 1,
        "title": title or "Epic Adventure",
        "genre": genre or "Fantasy",
        "theme": theme or "Magic",
        "inspiration": inspiration or "Lord of the Rings",
        "story": "A hero embarks on a journey to save the kingdom.",
        "characters": [
            {"name": "Aria", "role": "Hero"},
            {"name": "Borin", "role": "Sidekick"},
        ],
        "image": "https://via.placeholder.com/200x150.png?text=Concept"
    }
