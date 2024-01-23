import os
import sys
import time
import logging
from config import firestore_config
from utils.csv_to_dict import csvToDict
from utils.csv_to_json import csvToJson
from model.firebase import firestoreDB
teamDB = firestore_config.fsTeamDBName
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler


class MyHandler(LoggingEventHandler):
    def __init__(self, function_to_run):
        super().__init__()
        self.function_to_run = function_to_run

    def on_created(self, event):
        super().on_created(event)

        # check if the created file is a .csv file
        if event.src_path.endswith('.csv'):
            print(f'File created: {event.src_path} running {self.function_to_run}') #@pulkit dumb logging
            self.function_to_run(event.src_path)

#DEFINE FUNCTIONS TO RUN:
#Adds team data to firestore
def fsAddTeamData(csv_file_path):
    print("\nSTART FSADDTEAMDATA\n")
    json_file_path = firestore_config.teamJSON #customizable json file path
    #get team data from csv file
    all_teams_data = csvToDict(csv_file_path, "teamID")
    for team in all_teams_data:
        #add team to firestore
        firestoreDB.collection(teamDB).document(team).set(all_teams_data[team])
        print("Added team " + team + " to firestore")
    #add team data to firestore
    csvToJson(all_teams_data, json_file_path)
    os.remove(csv_file_path)
    print("\nEND FSADDTEAMDATA\n")
    return

#Adds clue data to firestore
def fsAddClueData(csv_file_path):
    print("\nSTART FSADDCLUEDATA\n")
    json_file_path = firestore_config.clueJSON #customizable json file path
    #get clue data from csv file
    all_clues_data = csvToDict(csv_file_path, "clueID")
    for clue in all_clues_data:
        #add clue to firestore
        firestoreDB.collection(firestore_config.fsClueDBName).document(clue).set(all_clues_data[clue])
        print("Added clue " + clue + " to firestore")
    #add clue data to firestore
    csvToJson(all_clues_data, json_file_path)
    os.remove(csv_file_path)
    print("\nEND FSADDCLUEDATA\n")
    return

#DEFINE DIRECTORIES TO WATCH & FUNCTIONS TO RUN
watch_and_run = {
    "./csv/firestoreTeamData": fsAddTeamData,
    "./csv/firestoreClueData": fsAddClueData,

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