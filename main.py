import os
import sys
import time
import logging
from config.clue_routes import random_route
from config import firestore_config
from config import realtime_config
from utils.csv_to_dict import csvToDict
from utils.csv_to_json import csvToJson
from utils.password_generator import generate_password
from utils.emailer import send_email
from model.firebase import firestoreDB, realtimeTeamDB
teamDB = firestore_config.fsTeamDBName
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
MODE = "DEV" # PROD or DEV

class MyHandler(LoggingEventHandler):
    def __init__(self, function_to_run):
        super().__init__()
        self.function_to_run = function_to_run

    def on_created(self, event):
        try:
            super().on_created(event)

            # check if the created file is a .csv file
            if event.src_path.endswith('.csv'):
                print(f'File created: {event.src_path} running {self.function_to_run}') #@pulkit dumb logging
                self.function_to_run(event.src_path)
        except Exception as e:
            print("Error: ", e)
            send_email("POSSIBLE APP CRASH: Error in on_created in MyHandler", str(e))

#DEFINE FUNCTIONS TO RUN:
#Adds team data to firestore
def fsAddTeamData(csv_file_path):
    try:
        print("\nSTART FSADDTEAMDATA\n")
        json_file_path = firestore_config.teamJSON #customizable json file path
        #get team data from csv file
        all_teams_data = csvToDict(csv_file_path, "teamID")
        for team in all_teams_data:
            if all_teams_data[team]["player2"] == "":
                all_teams_data[team].pop("player2")
            #add team to firestore
            firestoreDB.collection(teamDB).document(team).set(all_teams_data[team])
            print("Added team " + team + " to firestore")
        #add team data to firestore
        csvToJson(all_teams_data, json_file_path)
        os.remove(csv_file_path)
        print("\nEND FSADDTEAMDATA\n")
        return
    except Exception as e:
        print("Error: ", e)
        send_email("POSSIBLE APP CRASH: Error in adding team data to firestore", str(e))

#Adds clue data (and at the same time volunteer data) to firestore
def fsAddClueData(csv_file_path):
    try:
        volunteer = {}
        print("\nSTART FSADDCLUEDATA\n")
        json_file_path = firestore_config.clueJSON #customizable json file path
        #get clue data from csv file
        all_clues_data = csvToDict(csv_file_path, "clueID")
        for clue in all_clues_data:
            #add clue to firestore
            firestoreDB.collection(firestore_config.fsClueDBName).document(clue).set(all_clues_data[clue])

            #set up volunteer data
            volunteer = {
                "targetLocationLatitude": all_clues_data[clue]["targetLocationLatitude"],
                "targetLocationLongitude": all_clues_data[clue]["targetLocationLongitude"],
                "isLoggedIn": False,
                "password": generate_password(clue, True) if MODE == "DEV" else generate_password()
                }
            #add volunteer to firestore
            firestoreDB.collection(firestore_config.fsVolunteerDBName).document(clue).set(volunteer)
            print("Added clue " + clue + " to firestore")
        #add clue data to firestore
        csvToJson(all_clues_data, json_file_path)
        os.remove(csv_file_path)
        print("\nEND FSADDCLUEDATA\n")
        return
    except Exception as e:
        print("Error: ", e)
        send_email("POSSIBLE APP CRASH: Error in adding clue/volunteer data to firestore", str(e))

#Adds team data to realtime database
def rtAddTeamData(csv_file_path):
    try:
        print("\nSTART RTDBADDTEAMDATA\n")
        json_file_path = realtime_config.teamJSON #customizable json file path
        #get team data from csv file
        all_teams_data = csvToDict(csv_file_path, "teamID")
        for team in all_teams_data:
            all_teams_data[team]["route"] = random_route()
            all_teams_data[team]["balance"] = int(all_teams_data[team]["balance"])
            all_teams_data[team]["currentClueIndex"] = int(all_teams_data[team]["currentClueIndex"])
            all_teams_data[team]["extraLoc"] = int(all_teams_data[team]["extraLoc"])
            all_teams_data[team]["isFrozen"] = False
            all_teams_data[team]["isInvisible"] = False
            all_teams_data[team]["isMeterOff"] = False
            all_teams_data[team]["noSkipUsed"] = int(all_teams_data[team]["noSkipUsed"])
            all_teams_data[team]["mystery"] = int(all_teams_data[team]["mystery"])
            #add team to realtime database
            realtimeTeamDB.child(team).set(all_teams_data[team])
            print("Added team " + team + " to realtime database")
        #add team data to realtime database
        csvToJson(all_teams_data, json_file_path)
        os.remove(csv_file_path)
        print("\nEND RTDBADDTEAMDATA\n")
        return
    except Exception as e:
        print("Error: ", e)
        send_email("POSSIBLE APP CRASH: Error in adding team data to realtime database", str(e))

#DEFINE DIRECTORIES TO WATCH & FUNCTIONS TO RUN
watch_and_run = {
    "./csv/firestoreTeamData": fsAddTeamData,
    "./csv/firestoreClueData": fsAddClueData,
    "./csv/realtimeTeamData": rtAddTeamData
}

#SCHEDULE WATCHDOG FOR EACH DIRECTORY
for directory, function_to_run in watch_and_run.items():
    event_handler = MyHandler(function_to_run)
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()