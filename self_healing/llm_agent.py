from google import genai
import os
from self_healing.healing_actions import execute_action

def get_healing_action(stage, job, task):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "rebuild_pipeline"
        
    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are an autonomous AI DevOps self-healing agent.

    A CI/CD pipeline or deployment failed.

    Stage: {stage}
    Job: {job}
    Task: {task}
    
    As an AI, you must automatically select the exact right DevOps action to execute to heal the system.
    
    Reply ONLY with the exact name of ONE of the actions below. No explanation, no markdown.

    Possible actions:
    - rollback_deploy (Use if new code is failing tests/crashing)
    - restart_service (Use if service is hung or unresponsive)
    - blue_green_switch (Use if green env is failing, fallback to blue)
    - circuit_break (Use to stop cascading failures immediately)
    - scale_up (Use if failure is due to high load/build time)
    - clear_cache (Use if there are stale dependencies/cache issues)
    - auto_ticket (Use if you cannot self-heal this and it needs a human)
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    # Clean the response to ensure it's just the action string
    return response.text.strip()


if __name__ == "__main__":

    action = get_healing_action("Deploy", "deploy_to_dev", "deploy")

    print("LLM Suggested Action:")
    print(action)
    
    # Actually execute the action
    execute_action(action)
    print("Self-healing complete. Returning 0 exit code.")
    import sys
    sys.exit(0)