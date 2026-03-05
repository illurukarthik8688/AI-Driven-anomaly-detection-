import os

def execute_action(action):

    if "restart_service" in action:
        os.system("docker restart my_container")

    elif "rebuild_pipeline" in action:
        os.system("echo rebuilding pipeline")

    elif "clear_cache" in action:
        os.system("rm -rf cache/*")

    else:
        print("No action needed")