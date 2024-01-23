import os
from utils.csv_to_dict import csvToDict
from utils.csv_to_json import csvToJson
from model.firebase import firestoreDB
from config import firestore_config
teamDB = firestore_config.fsTeamDBName

#ADD TEAM DATA TO FIRESTORE
def fsAddTeamData(csv_file_path):
    #get team data from csv file
    all_teams_data = csvToDict(csv_file_path)
    for team in all_teams_data:
        #add team to firestore
        firestoreDB.collection(teamDB).document(team).set(all_teams_data[team])
        print("Added team: " + team + " to firestore")
    #add team data to firestore
    os.remove(csv_file_path)   

csv_path = firestore_config.teamCSV
json_path = firestore_config.teamJSON
if (__name__ == '__main__'):
    csvToJson(csv_path, json_path)
    fsAddTeamData(csv_path)
