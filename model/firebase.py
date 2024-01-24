import firebase_admin
from firebase_admin import credentials, firestore, db

cred = credentials.Certificate('./secrets/service-account-key.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://techrace-2024-default-rtdb.firebaseio.com'})

realtimeDB = db.reference("/")
realtimeTeamDB = db.reference("/dev-teams");
firestoreDB = firestore.client()

# objectname = {"balance": 1000, "currentClueIndex": int("1")}
# print(realtimeTeamDB.child("007").update(objectname))