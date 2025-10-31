from celery import chain
from .generate_universe import generate_universe
from .generate_scenario import generate_scenario
from .generate_characters import generate_characters
from .generate_char_img import generate_char_img
from .generate_locations import generate_locations

def run_full_workflow(user_json):
    """
    Orchestration complète du pipeline :
    univers -> scénario -> personnages -> images -> lieux
    """
    workflow = chain(
        generate_universe.s(user_json),
        generate_scenario.s(),
        generate_characters.s(),
        generate_char_img.s(),
        generate_locations.s()
    )
    task = workflow.apply_async()
    return task.id