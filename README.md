# coa_flask_app
The back-end RESTApis for the COA website

## Getting Started (Windows/GitBash)

1. Install python3 
2. Install flask: `pip install Flask`
3. Clone coa_flask_app project. 
4. Navigate into the coa_flask_app directory: `cd coa_flask_app`
5. Create a virtual environment: `python -m venv venv`
6. Bring up virtual environment: `source ./venv/Scripts/activate`. You should see something in the command line indicating that you are running in a virtual environment now. Note, to exit the virtual environment, run `deactivate`. 
7. `export FLASK_APP=create_application.py`
8. `export FLASK_ENV=development`
9. Set other DB related environment variables.
10. Install dependencies: `pip install requirements.txt`. If you get any errors like "Could not find a version that satisfies the requirement requirements.txt", then upgrade the dependencies: `pip install --upgrade -r requirements.txt`.
11. Start server: `flask run`

To test that the flask app is running and properly connected to the database, use the curl command or access the local server through a browser.

Ex: `curl http://127.0.0.1:5000/locations` or open http://127.0.0.1:5000/locations
