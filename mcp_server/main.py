import json
import asyncio
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse

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


@app.post("/sse")
async def sse_endpoint(request: JsonRpcRequest):
    print(f"[MCP-SSE] Incoming streaming request: method={request.method}, id={request.id}")

    async def event_generator():
        yield {
            "event": "received",
            "data": json.dumps({
                "jsonrpc": "2.0",
                "message": "MCP server received request",
                "method": request.method,
                "id": request.id
            })
        }

        await asyncio.sleep(0.2)

        if request.method == "sync_pipeline":
            action = (request.params or {}).get("action")
            print(f"[SYNC_PIPELINE] SSE action requested: {action}")

        response = handle_rpc_call(request.method, request.params)

        if "error" in response:
            print(f"[MCP-SSE] Error: {response['error']}")
            yield {
                "event": "error",
                "data": json.dumps({
                    "jsonrpc": "2.0",
                    "error": response["error"],
                    "id": request.id
                })
            }
            return

        if request.method == "fetch_jobs":
            print(f"[FETCH_JOBS] SSE returning {len(response['result'])} matching jobs")

        if request.method == "sync_pipeline":
            print("[FIRESTORE] SSE sync_pipeline request completed")

        yield {
            "event": "result",
            "data": json.dumps({
                "jsonrpc": "2.0",
                "result": response["result"],
                "id": request.id
            })
        }

    return EventSourceResponse(event_generator())