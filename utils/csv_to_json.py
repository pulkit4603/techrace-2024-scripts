import csv
import json
from datetime import datetime

#CONVERTS CSV FILE TO JSON FILE
def csvToJson(csv_file_path, json_file_path):
    current_time = datetime.now()
    json_dict = {}
    #open csv file and read data into dictionary
    with open(csv_file_path, encoding='utf-8') as csv_file:
        csv_data = csv.DictReader(csv_file)
        for row in csv_data:
            teamID = str(row.pop('teamID'))
            row["isLoggedIn"] = False
            json_dict[teamID] = row
    json_dict["updatedAt"] = str(current_time)

    # Convert dict to JSON object
    json_object = json.dumps(json_dict, indent=4)

    # Cre
    # Read the existing data from the file
    with open(json_file_path, "a+") as json_file:
        json_file.seek(0)  # Move the file pointer to the beginning of the file
        try:
            data = json.load(json_file)
            # If the file is empty, initialize data as an empty list
            if data is None:
                data = []
        except json.JSONDecodeError:
            # If the file does not contain valid JSON, initialize data as an empty list
            data = []

    # Append the new JSON object to the data
    data.append(json.loads(json_object))

    # Write the updated data back to the file
    with open(json_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
