import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('./secrets/service-account-key.json')
firebase_admin.initialize_app(cred)

# rtdb = firebase_admin.database();
# realtimeDB = rtdb.ref("/");
firestoreDB = firestore.client()