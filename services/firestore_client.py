from google.cloud import firestore


# Keep Firestore setup in one place so the rest of the code stays clean.
def get_firestore_client():
    return firestore.Client()
    