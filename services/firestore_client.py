from google.cloud import firestore


# Firestore client setup is kept in one small helper so the rest of the code
# does not have to repeat connection logic in every function.
def get_firestore_client():
    return firestore.Client()
