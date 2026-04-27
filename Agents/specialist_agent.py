import json
import requests

MCP_SSE_URL = "https://acc-mcp-server-134991748283.us-east1.run.app/sse"


def call_mcp_sse(method, params, request_id):
    """
    This function represents the Career Specialist calling the MCP server.

    The MCP server is deployed on Cloud Run, and this call uses the /sse endpoint.
    The request follows JSON-RPC format, and the response comes back as SSE events.
    """
    print(f"[SPECIALIST] Calling MCP server with method={method}")

    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": request_id
    }

    response = requests.post(
        MCP_SSE_URL,
        headers={"Content-Type": "application/json"},
        json=payload,
        stream=True,
        timeout=30
    )

    response.raise_for_status()

    final_result = None

    for line in response.iter_lines(decode_unicode=True):
        if not line:
            continue

        print(f"[MCP-SSE] {line}")

        if line.startswith("data:"):
            data_text = line.replace("data:", "").strip()

            try:
                data = json.loads(data_text)
            except json.JSONDecodeError:
                continue

            if "result" in data:
                final_result = data["result"]

    return final_result


def find_jobs(role=None, location=None, keyword=None):
    """
    Uses the fetch_jobs MCP tool.

    This is where internship search work happens.
    The Lead Orchestrator does not fetch jobs directly.
    """
    print("[SPECIALIST] Handling job search task")

    params = {
        "role": role,
        "location": location,
        "keyword": keyword
    }

    return call_mcp_sse("fetch_jobs", params, request_id=1)


def save_job_to_pipeline(job):
    """
    Uses the sync_pipeline MCP tool to save a job into Firestore.

    Firestore is not touched directly by this agent.
    The agent only talks to the MCP server.
    """
    print("[SPECIALIST] Saving selected job into internship pipeline")

    params = {
        "action": "create",
        "job_id": job.get("job_id"),
        "company": job.get("company"),
        "title": job.get("title"),
        "location": job.get("location"),
        "url": job.get("url"),
        "status": "saved",
        "notes": "Saved through agent orchestration demo",
        "deadline": ""
    }

    return call_mcp_sse("sync_pipeline", params, request_id=2)


def list_pipeline():
    """
    Uses the sync_pipeline MCP tool to list current Firestore pipeline records.
    """
    print("[SPECIALIST] Listing current internship pipeline")

    params = {
        "action": "list"
    }

    return call_mcp_sse("sync_pipeline", params, request_id=3)