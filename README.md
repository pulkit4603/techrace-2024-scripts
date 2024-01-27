<h2>TECHRACE 2024 SCRIPTS</h2>
[A repository of the automation scripts used in development of the official 2024 Techrace App]

This Python automation script watches specific directories for new CSV files and uses the data in these files to populate Firebase databases.

<h3>Getting Started</h3>
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

<h3>Prerequisites</h3>
You need Python 3.x and mainly the following Python packages:
    - watchdog
    - firebase_admin

You can install the packages required by this repository using pip:

    pip install -r requirements.txt

<h3>Installing</h3>
<h5>Clone the repository to your local machine:</h5>

    git clone {code url of this repository}

<h5>Run the script:</h5>

    python main.py

<h3>Usage</h3>
The script watches the following directories for new CSV files:
    ./csv/firestoreTeamData
    ./csv/firestoreClueData
    ./csv/realtimeTeamData

When a new CSV file is added to one of these directories, the script reads the data from the file and adds it to the corresponding Firebase database.

<h3>Built With</h3>
Python - The programming language used
Firebase - The database used

<h3>License</h3>
This project is licensed under the MIT License.
