from google import genai
import os

def get_healing_action(stage, job, task):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "retry_job"
        
    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are an AI DevOps engineer if u know u know.

    A CI/CD pipeline may fail.

    Stage: {stage}
    Job: {job}
    Task: {task}

    Suggest the best recovery action.

    Possible actions:
    - retry_job
    - restart_stage
    - rollback_deploy
    - ignore
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


if __name__ == "__main__":

    action = get_healing_action("Deploy", "deploy_to_dev", "deploy")

    print("LLM Suggested Action:")
    print(action)