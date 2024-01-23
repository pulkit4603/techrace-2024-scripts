import csv

#CONVERTS CSV FILE TO PYTHON DICTIONARY
def csvToDict(csv_file_path):
    json_dict = {}

    #open csv file and read data into dictionary
    with open(csv_file_path, encoding='utf-8') as csv_file:
        csv_data = csv.DictReader(csv_file)
        for row in csv_data:
            teamID = str(row.pop('teamID'))
            row["isLoggedIn"] = False
            json_dict[teamID] = row
    return json_dict