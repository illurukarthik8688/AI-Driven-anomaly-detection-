import google.generativeai as genai
import os

# Load API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def get_healing_action(stage, job, task):

    prompt = f"""
    You are an AI DevOps engineer.

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

    response = model.generate_content(prompt)

    return response.text


if __name__ == "__main__":

    action = get_healing_action("Deploy", "deploy_to_dev", "deploy")

    print("LLM Suggested Action:")
    print(action)