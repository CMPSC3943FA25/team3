## Installation & Run Guide
Download the repo with either
- `git clone https://github.com/CMPSC3943FA25/team3.git`
- Clicking the green `Code` button at https://github.com/CMPSC3943FA25/team3/ and clicking "Download ZIP". Extract the ZIP to an empty folder of your choice

Download Python https://www.python.org/downloads/

Make sure Python is added to PATH during installation.

Open the project in your editor of choice.
Make sure you are in the project directory. You should see a frontend and backend directory when listing files and subdirectories in the directory.
- Type `dir` into the terminal on Windows to confirm
- Type `ls` into the terminal on Linux to confirm

Now copy these commands into your terminal
### Windows:
```
cd backend
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\python -m flask run
```

### Linux:
```
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m flask run
```
You should now have the flask server up and running!

I suggest creating a .flaskenv file in the backend directory with the contents:
```
FLASK_APP=app
FLASK_DEBUG=True
```
This allows for the app to restart on save.

# plant planner up and running - TEAM 3
- get local weather
- Is it safe to plant? T or F.
- Recommend plants that can survive the weather
  
