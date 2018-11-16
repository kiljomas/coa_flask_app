# coa_flask_app
The back-end RESTApis for the COA website

## Getting Started (Windows/GitBash)

1. Install python3 
2. Install flask: `pip install Flask`
3. Clone coa_flask_app project. 
4. Navigate into the coa_flask_app directory: `cd coa_flask_app`
5. Bring up virutal environment: `source ./venv/Scripts/activate`. You should see something in the command line indicating that you are running in a virtual environment now. Note, to exit the virtual environment, run `deactivate`. 
6. `export FLASK_APP=create_application.py`
7. `export FLASK_ENV=development`
8. Set other DB related environment variables.
9. Install dependencies: `pip install requirements.txt`. If you get any errors like "Could not find a version that satisfies the requirement requirements.txt", then upgrade the dependencies: `pip install --upgrade -r requirements.txt`.
10. Start server: `flask run`

To test that the flask app is running and properly connected to the database, use the curl command or access the local server through a browser.

Ex: `curl http://127.0.0.1:5000/getsitesdropdownlist` or open http://127.0.0.1:5000/getsitesdropdownlist
