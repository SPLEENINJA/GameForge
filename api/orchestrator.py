# api/orchestrator.py     

from transformers import pipeline
# from diffusers import StableDiffusionPipeline
import torch, os, random, requests, base64
from dotenv import load_dotenv
from django.conf import settings
load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")

HF_MODEL_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Accept": "image/png"
}

# ===============================
# 🖼️ Function: Generate Concept Art via Hugging Face API
# ===============================
def generate_concept_art(prompt):
    os.makedirs("media/generated_art", exist_ok=True)

    response = requests.post(
        HF_MODEL_URL,
        headers=headers,
        json={"inputs": prompt}
    )

    if response.status_code != 200:
        raise Exception(f"Image generation failed: {response.text}")

    # Save the image
    file_name = f"{prompt.replace(' ', '_')}_{random.randint(1000,9999)}.png"
    image_path = f"media/generated_art/{file_name}"

    with open(image_path, "wb") as f:
        f.write(response.content)

    return image_path


# Load the text generation model once (it caches automatically)
text_generator  = pipeline(
    "text-generation",
    model="gpt2",  # good open-source creative model
    device_map="auto"
)


 

def generate_game_concept(title, genre, theme, inspiration):
    
    prompt = f"""
    You are a creative game designer. Generate a new video game concept with:
    - Title: {title}
    - Genre: {genre}
    - Theme: {theme}
    - Inspiration: {inspiration}

    Provide:
    1. A short story (3 paragraphs max)
    2. Two characters (name + short role)
    3. A short art style description
    """

    # Generate AI text
    response = text_generator (
        prompt,
        max_new_tokens=300,
        temperature=0.8,
        do_sample=True,
        top_p=0.9
    )[0]["generated_text"]

    image_prompt = f"{genre} game with theme {theme}, concept art, {inspiration} style"
    image_path = generate_concept_art(image_prompt)

    public_image_url = settings.MEDIA_URL + image_path.replace("media/", "")

    print("image___path:", public_image_url)  # Now safe to print

    # Basic structure for now
    return {
        "title": f"Generated Game Concept: {title}",
        "genre": genre,
        "theme": theme,
        "inspiration": inspiration,
        "main_story": response,
        "characters": [
            {"name": random.choice(["Aeris", "Kael", "Nova", "Luna", "Riven"]), "role": "Hero"},
            {"name": random.choice(["Draven", "Mira", "Cyrus", "Erebus", "Vex"]), "role": "Villain"},
        ],
        "image": public_image_url,  # path to saved concept art
    }



# codes for image creator model

# # ===============================
# # 🎨 IMAGE GENERATION (Stable Diffusion)
# # ===============================
# device = "cuda" if torch.cuda.is_available() else "cpu"
 
# # ⚠️ Will download ~4GB model the first time
# image_generator = StableDiffusionPipeline.from_pretrained(
#     "stabilityai/stable-diffusion-2",
#     torch_dtype=torch.float16 if device == "cuda" else torch.float32
# ).to(device)
 
  
# # ===============================
# # 🖼️ Function: Generate Concept Art
# # ===============================
# def generate_concept_art(prompt):
#     # Ensure media folder exists
#     os.makedirs("media/generated_art", exist_ok=True)
 
#     image = image_generator(prompt).images[0]
#     file_name = f"{prompt.replace(' ', '_')}_{random.randint(1000,9999)}.png"
#     image_path = f"media/generated_art/{file_name}"
#     image.save(image_path)
#     return image_path
 
    # # 🎨 Generate concept art
    # image_prompt = f"{genre} game with theme {theme}, concept art, {inspiration} style"
    # image_path = generate_concept_art(image_prompt)






