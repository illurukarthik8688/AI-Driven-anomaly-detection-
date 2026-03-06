import os
import sys
import subprocess
from google import genai

MAX_RETRIES = 2

PIPELINE_STEPS = [
    {"name": "Install Dependencies", "cmd": "pip install -r requirements.txt"},
    {"name": "AI Failure Prediction", "cmd": "python predict_failure.py"},
    {"name": "Measure Build Time", "cmd": "python model.py"},
    {"name": "Detect Build Time Anomaly", "cmd": "python detect_build_time.py"},
    {"name": "Run Tests", "cmd": "python test.py"},
    {"name": "Build Docker Image", "cmd": "docker build -t cicd-anomaly ."}
]

def get_healing_script_from_llm(failed_step_name, failed_cmd, stdout, stderr):
    """Asks the LLM to write a concrete bash script to fix the failing code/environment."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[LLM Agent] GEMINI_API_KEY not found. Cannot auto-heal.")
        return None
        
    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are an autonomous AI DevOps self-healing agent orchestrating a CI/CD pipeline.

    A pipeline step just failed mid-flight.

    Failed Step: {failed_step_name}
    Command Executed: {failed_cmd}
    
    Error Output (stderr/stdout):
    {stderr}
    {stdout}
    
    Write a single, executable bash command or snippet that fixes this specific issue so the test or command will pass on the very next retry.
    For example, if a python test expects 200 but got 404, use `sed` to literally edit the python test file to expect the right thing (or vice versa), or install a missing package.
    
    CRITICAL: Reply ONLY with the raw bash command. No markdown formatting, no ````bash, no explanations. Just the command.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        # Clean up any potential markdown the LLM might stubbornly include
        script = response.text.replace("```bash", "").replace("```", "").strip()
        return script
    except Exception as e:
        print(f"[LLM Agent] Failed to contact Gemini: {e}")
        return None

def run_step(step_name, cmd):
    """Runs a single shell command and returns success status, stdout, and stderr."""
    print(f"\n========================================")
    print(f"▶ Running Step: {step_name}")
    print(f"▶ Command: {cmd}")
    print(f"========================================")
    
    # Run the command and capture output
    result = subprocess.run(
        cmd, 
        shell=True, 
        text=True, 
        capture_output=True
    )
    
    if result.returncode == 0:
        print(result.stdout)
        print(f"✅ Step '{step_name}' passed successfully.")
        return True, result.stdout, result.stderr
        
    else:
        print(result.stdout)
        print(result.stderr)
        print(f"❌ Step '{step_name}' FAILED with exit code {result.returncode}.")
        return False, result.stdout, result.stderr

def run_pipeline():
    print("🚀 Starting Proactive In-Flight Auto-Fixing Pipeline...\n")
    
    for step in PIPELINE_STEPS:
        success = False
        retries = 0
        
        while not success and retries <= MAX_RETRIES:
            if retries > 0:
                print(f"\n🔄 Retrying step '{step['name']}' (Attempt {retries}/{MAX_RETRIES})...")
                
            success, stdout, stderr = run_step(step['name'], step['cmd'])
            
            if success:
                break # Move to next step
                
            # If we failed, attempt to heal
            retries += 1
            if retries <= MAX_RETRIES:
                print(f"\n⚠️ Anomaly detected! Requesting mid-flight fix from LLM Agent...")
                fix_script = get_healing_script_from_llm(step['name'], step['cmd'], stdout, stderr)
                
                if fix_script:
                    print(f"[LLM Agent] Proposed Fix Script:\n------------------\n{fix_script}\n------------------")
                    print("[System] Executing LLM Fix...")
                    
                    fix_result = subprocess.run(fix_script, shell=True, text=True, capture_output=True)
                    if fix_result.returncode == 0:
                        print("✅ Fix executed successfully. Preparing to retry pipeline step...")
                    else:
                        print(f"❌ The fix script failed to run:\n{fix_result.stderr}")
                else:
                    print("[LLM Agent] No fix proposed. Retrying without changes just in case it was a network flake...")
                    
        if not success:
            print(f"\n🚨 CRITICAL FAILURE: Step '{step['name']}' failed persistently after {MAX_RETRIES} healing attempts.")
            sys.exit(1)
            
    print("\n🎉 Pipeline completed successfully! All anomalies were mitigated.")
    sys.exit(0)

if __name__ == "__main__":
    run_pipeline()
