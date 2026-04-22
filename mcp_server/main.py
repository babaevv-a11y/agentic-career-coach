from fastapi import FastAPI
from fastapi.responses import JSONResponse
from mcp_server.schemas import JsonRpcRequest
from mcp_server.rpc_handlers import handle_rpc_call

app = FastAPI()


@app.get("/")
def root():
    print("[MCP] Root route was called")
    return {"message": "MCP server is running"}


@app.get("/health")
def health():
    print("[MCP] Health check route was called")
    return {"status": "ok"}


@app.post("/rpc")
def rpc_endpoint(request: JsonRpcRequest):
    print(f"[MCP] Incoming RPC request: method={request.method}, id={request.id}")

    if request.method == "sync_pipeline":
        action = (request.params or {}).get("action")
        print(f"[SYNC_PIPELINE] Action requested: {action}")

    response = handle_rpc_call(request.method, request.params)

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

    if request.method == "fetch_jobs":
        print(f"[FETCH_JOBS] Returning {len(response['result'])} matching jobs")

    if request.method == "sync_pipeline":
        print("[FIRESTORE] sync_pipeline request completed")

    return {
        "jsonrpc": "2.0",
        "result": response["result"],
        "id": request.id
    }