from mcp_server.tool_registry import TOOLS



def handle_rpc_call(method, params):
    params = params or {}

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

    if method == "sync_pipeline":
        action = params.get("action")

        if action not in TOOLS["sync_pipeline"]:
            return {
                "error": f"Unknown sync_pipeline action: {action}"
            }

        pipeline_function = TOOLS["sync_pipeline"][action]

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

        if action == "list":
            result = pipeline_function()
            return {"result": result}

        if action == "update_status":
            result = pipeline_function(
                document_id=params.get("document_id"),
                status=params.get("status")
            )

            if "error" in result:
                return result

            return {"result": result}

    return {
        "error": f"Unknown method: {method}"
    }