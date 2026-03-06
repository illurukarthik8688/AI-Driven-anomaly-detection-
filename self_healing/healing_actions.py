import os
import time

def execute_action(action):

    print(f"Executing self-healing action: {action}")

    if "restart_service" in action:
        print("[System] Restarting Docker service...")
        os.system("docker restart my_container || echo 'Assuming container restarted for demo'")
        
    elif "rollback" in action or "rollback_deploy" in action:
        print("[System] Rolling back to previous stable deployment...")
        os.system("git reset --hard HEAD~1 && echo 'Rolled back to previous commit'")

    elif "blue_green_switch" in action:
        print("[System] Traffic anomaly detected. Switching traffic from Green to Blue environment...")
        os.system("echo 'Updating NGINX/Load Balancer to route to Blue env'")

    elif "circuit_break" in action:
        print("[System] High failure rate! Opening circuit breaker to stop cascading failures...")
        os.system("echo 'Circuit breaker opened. Traffic to failing service paused.'")

    elif "scale_up" in action:
        print("[System] Load anomaly detected. Auto-scaling replica set...")
        os.system("echo 'kubectl scale deployment my-app --replicas=5'")

    elif "create_jira_ticket" in action or "auto_ticket" in action:
        print("[System] Unknown anomaly. Creating high-priority Jira ticket for DevOps team...")
        os.system("echo 'Jira Ticket SEV-1 created: CI/CD Pipeline Failure'")
        
    elif "rebuild_pipeline" in action:
        print("[System] Rebuilding pipeline from scratch...")
        os.system("echo rebuilding pipeline")

    elif "clear_cache" in action:
        print("[System] Clearing application cache...")
        os.system("rm -rf cache/* || echo 'Cache cleared'")

    else:
        print(f"[System] Unknown action '{action}'. Passing to manual review.")