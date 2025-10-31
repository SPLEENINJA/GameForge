from django.urls import path
from .views import generate_universe_api, game_info_view, generate_scenario_api,generate_char_img_api, generate_characters_api,generate_locations_api, get_task_result
from .views import run_game_workflow, get_workflow_result

urlpatterns = [
    path("generate-universe/", generate_universe_api, name="generate_universe_api"),
       path("generate-scenario/", generate_scenario_api, name="generate_scenario_api"),
         path("generate-char-images/", generate_char_img_api, name="generate_char_img_api"),
            path("generate-characters/", generate_characters_api, name="generate_characters_api"),
                 path("generate-locations/", generate_locations_api, name="generate_locations_api"),
                     path("task-result/<str:task_id>/", get_task_result, name="get_task_result"),
                         path("form/", game_info_view, name="game_info_view"),
                                path("run-workflow/", run_game_workflow, name="run_game_workflow"),
                                     path("workflow-result/<str:task_id>/", get_workflow_result, name="get_workflow_result")
]