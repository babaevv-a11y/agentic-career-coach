from Agents.specialist_agent import find_jobs, save_job_to_pipeline, list_pipeline


def handle_user_request(user_message):
    """
    This function represents the Lead Orchestrator.

    It receives the user request, decides what the request means,
    and delegates backend-heavy work to the Career Specialist.
    """
    print("[ORCHESTRATOR] User request received")
    print(f"[ORCHESTRATOR] Request text: {user_message}")

    message = user_message.lower()

    if "internship" in message or "job" in message:
        print("[ROUTING] Internship/job request detected")
        print("[ORCHESTRATOR] Delegating job search to Career Specialist")

        jobs = find_jobs(role="Intern", keyword="software")

        if not jobs:
            return "No matching internships were found."

        selected_job = jobs[0]

        print("[ORCHESTRATOR] Career Specialist returned job results")
        print("[ORCHESTRATOR] Delegating pipeline save to Career Specialist")

        save_result = save_job_to_pipeline(selected_job)

        print("[ORCHESTRATOR] Asking Career Specialist to list current pipeline")
        pipeline = list_pipeline()

        return {
            "message": "I found an internship and saved it to the pipeline.",
            "selected_job": selected_job,
            "save_result": save_result,
            "current_pipeline": pipeline
        }

    print("[ROUTING] General request detected")
    return "I can help search for internships, save jobs, update application status, and review your internship pipeline."