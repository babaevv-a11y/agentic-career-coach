from services.jobs_service import fetch_jobs_from_file
from services.pipeline_service import (
    create_pipeline_entry,
    list_pipeline_entries,
    update_pipeline_status
)


# Tool names here should stay aligned with the project spec.
TOOLS = {
    "fetch_jobs": fetch_jobs_from_file,
    "sync_pipeline": {
        "create": create_pipeline_entry,
        "list": list_pipeline_entries,
        "update_status": update_pipeline_status
    }
}