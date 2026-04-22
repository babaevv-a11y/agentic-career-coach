from pydantic import BaseModel
from typing import Optional, Dict, Any


class JsonRpcRequest(BaseModel):
    jsonrpc: str
    method: str
    params: Optional[Dict[str, Any]] = None
    id: int