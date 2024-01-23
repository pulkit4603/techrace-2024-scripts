import csv

#CONVERTS CSV FILE TO PYTHON DICTIONARY
def csvToDict(csv_file_path, docID):
    json_dict = {}

    #open csv file and read data into dictionary
    with open(csv_file_path, encoding='utf-8') as csv_file:
        csv_data = csv.DictReader(csv_file)
        for row in csv_data:
            key = str(row.pop(docID))
            # all extra attributes
            if (docID=="teamID"):
                row["isLoggedIn"] = False
            elif (docID=="clueID"):
                row[docID] = key
            json_dict[key] = row
    return json_dict