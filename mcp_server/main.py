from fastapi import FastAPI
from fastapi.responses import JSONResponse
from mcp_server.schemas import JsonRpcRequest
from mcp_server.rpc_handlers import handle_rpc_call

# This is the entry point for the MCP server.
# FastAPI gives us the HTTP routes, and /rpc acts as the main tool gateway.
app = FastAPI()


@app.get("/")
def root():
    # Simple root route so we can quickly tell the server is up.
    print("[MCP] Root route was called")
    return {"message": "MCP server is running"}


@app.get("/health")
def health():
    # Health route is useful for testing and later for Cloud Run health checks.
    print("[MCP] Health check route was called")
    return {"status": "ok"}


@app.post("/rpc")
def rpc_endpoint(request: JsonRpcRequest):
    # Every MCP-style request enters here first.
    # We log the method and id so it is easier to trace one request from start to finish.
    print(f"[MCP] Incoming RPC request: method={request.method}, id={request.id}")

    # If the request is for the pipeline, log the specific action too.
    # That makes it much easier to explain create/list/update in demo or code review.
    if request.method == "sync_pipeline":
        action = (request.params or {}).get("action")
        print(f"[SYNC_PIPELINE] Action requested: {action}")

    # Pass the request into the handler layer.
    # The handler decides which backend function to call.
    response = handle_rpc_call(request.method, request.params)

    # If the handler returns an error, convert it into a clean JSON style error response.
    if "error" in response:
        print(f"[MCP] RPC error: {response['error']}")
        return JSONResponse(
            status_code=400,
            content={
                "jsonrpc": "2.0",
                "error": response["error"],
                "id": request.id
            }
        )

    # Extra logging for fetch_jobs so we can see how many job matches came back.
    if request.method == "fetch_jobs":
        print(f"[FETCH_JOBS] Returning {len(response['result'])} matching jobs")

    # Extra logging for Firestore-backed pipeline work.
    if request.method == "sync_pipeline":
        print("[FIRESTORE] sync_pipeline request completed")

    # Successful JSON-RPC style response.
    return {
        "jsonrpc": "2.0",
        "result": response["result"],
        "id": request.id
    }