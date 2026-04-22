from mcp_server.tool_registry import TOOLS


# This file is the middle layer between the incoming RPC request and the actual backend logic.
# In other words, /rpc receives the request in main.py, and this file decides which tool to run.
def handle_rpc_call(method, params):
    # params can be empty, so this makes sure we always have a dictionary to work with.
    params = params or {}

    # First tool: fetch_jobs
    # This is the simpler tool because it just reads mock job data and applies filters.
    if method == "fetch_jobs":
        tool_function = TOOLS["fetch_jobs"]

        result = tool_function(
            role=params.get("role"),
            location=params.get("location"),
            keyword=params.get("keyword")
        )

        return {
            "result": result
        }

    # Second tool: sync_pipeline
    # This one is more complex because it supports multiple actions instead of just one.
    if method == "sync_pipeline":
        action = params.get("action")

        # The action tells us which pipeline operation the caller wants:
        # create, list, or update_status.
        if action not in TOOLS["sync_pipeline"]:
            return {
                "error": f"Unknown sync_pipeline action: {action}"
            }

        pipeline_function = TOOLS["sync_pipeline"][action]

        # Create a new internship entry in Firestore.
        if action == "create":
            result = pipeline_function(
                job_id=params.get("job_id"),
                company=params.get("company"),
                title=params.get("title"),
                location=params.get("location"),
                url=params.get("url"),
                status=params.get("status", "saved"),
                notes=params.get("notes", ""),
                deadline=params.get("deadline", "")
            )
            return {"result": result}

        # List all current pipeline entries from Firestore.
        if action == "list":
            result = pipeline_function()
            return {"result": result}

        # Update the status of one specific entry, for example saved -> applied.
        if action == "update_status":
            result = pipeline_function(
                document_id=params.get("document_id"),
                status=params.get("status")
            )

            if "error" in result:
                return result

            return {"result": result}

    # If the method name does not match any registered tool, return an error.
    return {
        "error": f"Unknown method: {method}"
    }