from datetime import datetime, UTC
from services.firestore_client import get_firestore_client

COLLECTION_NAME = "internship_pipeline"


# Creates a new internship pipeline entry in Firestore.
def create_pipeline_entry(job_id, company, title, location, url, status="saved", notes="", deadline=""):
    db = get_firestore_client()
    doc_ref = db.collection(COLLECTION_NAME).document()

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

    doc_ref.set(payload)

    return {
        "message": "Pipeline entry created",
        "document_id": doc_ref.id,
        "data": payload
    }


# Lists all pipeline entries from Firestore.
def list_pipeline_entries():
    db = get_firestore_client()
    docs = db.collection(COLLECTION_NAME).stream()

    results = []
    for doc in docs:
        item = doc.to_dict()
        item["document_id"] = doc.id
        results.append(item)

    return results


# Updates the status of one existing pipeline entry.
def update_pipeline_status(document_id, status):
    db = get_firestore_client()
    doc_ref = db.collection(COLLECTION_NAME).document(document_id)

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