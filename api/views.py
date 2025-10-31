from django.shortcuts import render
# Create your views here.
from django.shortcuts import render
from .forms import GameInfoForm

def game_info_view(request):
    user_json = None
    if request.method == "POST":
        form = GameInfoForm(request.POST)
        if form.is_valid():
            user_json = form.to_json()
    else:
        form = GameInfoForm()
    return render(request, "api/game_info.html", {"form": form, "user_json": user_json})

from rest_framework.decorators import api_view 
from rest_framework.response import Response 
from tasks.generate_universe import generate_universe 
from tasks.generate_scenario import generate_scenario 
from tasks.generate_char_img import generate_char_img
from tasks.generate_characters import generate_characters
from tasks.generate_locations import generate_locations
from celery.result import AsyncResult

@api_view(['POST']) 
def generate_universe_api(request): 
    user_json = request.data # JSON envoyé par le front 
    task = generate_universe.delay(user_json) # exécution asynchrone 
    return Response({"task_id": task.id})

@api_view(['POST'])
def generate_scenario_api(request):
    universe_json = request.data  # doit être output de generate_universe
    task = generate_scenario.delay(universe_json)
    return Response({"task_id": task.id})


@api_view(['POST'])
def generate_characters_api(request):
    """
    Endpoint API pour générer 3 personnages à partir d'un scénario.
    Input : JSON scénario généré par generate_scenario
    Output : task_id Celery pour récupération ultérieure
    """
    scenario_json = request.data
    task = generate_characters.delay(scenario_json)  # exécution asynchrone
    return Response({"task_id": task.id})

@api_view(['POST'])
def generate_char_img_api(request):
    """
    Endpoint API pour générer des images pour chaque personnage.
    Input : JSON des personnages généré par generate_characters
    Output : task_id Celery pour récupération ultérieure
    """
    characters_json = request.data
    task = generate_char_img.delay(characters_json)  # exécution asynchrone
    return Response({"task_id": task.id})



@api_view(['POST'])
def generate_locations_api(request):
    """
    Endpoint API pour générer des lieux emblématiques à partir d'un scénario.
    Input : JSON scénario généré par generate_scenario
    Output : task_id Celery pour récupération JSON
    """
    scenario_json = request.data
    task = generate_locations.delay(scenario_json)
    return Response({"task_id": task.id})

@api_view(['GET'])
def get_task_result(request, task_id):
    """
    Permet de récupérer le résultat JSON d'une tâche Celery
    """
    result = AsyncResult(task_id)
    if result.ready():
        return Response(result.result)
    return Response({"status": "pending"})

from rest_framework.decorators import api_view
from rest_framework.response import Response
from tasks.tasks_workflow import run_full_workflow
# from celery.result import AsyncResult

@api_view(['POST'])
def run_game_workflow(request):
    """
    Déclenche tout le pipeline (univers -> scénario -> personnages -> images -> lieux)
    et renvoie task_id pour récupérer le résultat JSON final.
    """
    user_json = request.data
    task_id = run_full_workflow(user_json)
    return Response({"task_id": task_id})

@api_view(['GET'])
def get_workflow_result(request, task_id):
    """
    Permet de récupérer le JSON final généré par le workflow complet
    """
    result = AsyncResult(task_id)
    if result.ready():
        return Response(result.result)
    return Response({"status": "pending"})
