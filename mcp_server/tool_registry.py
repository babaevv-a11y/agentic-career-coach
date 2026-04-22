from services.jobs_service import fetch_jobs_from_file
from services.pipeline_service import (
    create_pipeline_entry,
    list_pipeline_entries,
    update_pipeline_status
)

# This registry is the lookup table for tool names.
# The idea is that the RPC layer does not need to know implementation details.
# It only needs to know which backend function belongs to which tool name.
TOOLS = {
    "fetch_jobs": fetch_jobs_from_file,
    "sync_pipeline": {
        "create": create_pipeline_entry,
        "list": list_pipeline_entries,
        "update_status": update_pipeline_status
    }
}