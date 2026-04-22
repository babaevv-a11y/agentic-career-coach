from datetime import datetime, UTC
from services.firestore_client import get_firestore_client

COLLECTION_NAME = "internship_pipeline"


# This service handles all internship pipeline operations.
# Firestore is acting as the central state store for saved jobs and application progress.
# Creates a new pipeline entry in Firestore.
def create_pipeline_entry(job_id, company, title, location, url, status="saved", notes="", deadline=""):
    db = get_firestore_client()
    doc_ref = db.collection(COLLECTION_NAME).document()

    # We store timestamps so we can track when the entry was created and when it was last updated.
    now = datetime.now(UTC).isoformat()

    payload = {
        "job_id": job_id,
        "company": company,
        "title": title,
        "location": location,
        "url": url,
        "status": status,
        "notes": notes,
        "deadline": deadline,
        "created_at": now,
        "updated_at": now
    }

    # Write the new internship entry into Firestore.
    doc_ref.set(payload)

    return {
        "message": "Pipeline entry created",
        "document_id": doc_ref.id,
        "data": payload
    }


# Reads all current internship pipeline entries from Firestore.
def list_pipeline_entries():
    db = get_firestore_client()
    docs = db.collection(COLLECTION_NAME).stream()

    results = []
    for doc in docs:
        item = doc.to_dict()

        # Firestore stores the document id separately from the fields.
        # Adding it back into the returned item makes update operations easier later.
        item["document_id"] = doc.id
        results.append(item)

    return results


# Updates only the status field for an existing internship entry.
# Example: saved -> applied -> interviewing.
def update_pipeline_status(document_id, status):
    db = get_firestore_client()
    doc_ref = db.collection(COLLECTION_NAME).document(document_id)

    # Before updating, make sure the entry actually exists.
    if not doc_ref.get().exists:
        return {
            "error": f"Pipeline entry not found: {document_id}"
        }

    doc_ref.update({
        "status": status,
        "updated_at": datetime.now(UTC).isoformat()
    })

    return {
        "message": "Pipeline status updated",
        "document_id": document_id,
        "new_status": status
    }