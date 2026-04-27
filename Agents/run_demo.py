from Agents.orchestrator_agent import handle_user_request


def main():
    """
    This script runs one full demo request.

    It is meant for screenshots, logs, and the narrated demo.
    It shows the request moving from Orchestrator to Specialist to MCP to Firestore.
    """
    print("=== Agentic Career Coach Demo ===")

    user_request = "Find software engineering internships and save one to my pipeline."

    result = handle_user_request(user_request)

    print("\n=== Final Response Returned to User ===")
    print(result)


if __name__ == "__main__":
    main()