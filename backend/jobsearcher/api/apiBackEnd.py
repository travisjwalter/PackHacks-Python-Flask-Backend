from flask import Flask, request, jsonify
from indeedScraper import getList
from flask_cors import CORS

## This file is the Flask GET API endpoint for the Backend PackHacks workshop.
## We import flask and the getList function from the indeedScraper file we created.
## @author Travis Walter - 3/16/2021

app = Flask(__name__)
CORS(app)

## This is the API GET @ endpoint /retrieveJobs that returns the list of jobs to the caller.
## It uses the Indeed Scraper and returns the parsed information as JSON.
@app.route('/retrieveJobs', methods=['GET'])

## This is the function that is run when the /retrieveJobs endpoint is called, which runs
## the Indeed API call and returns the JSON.
def getJobs():
    data = []
    if request.method == 'GET': # Checks if it's a GET request
        ## This function scrapes the Indeed Job Search website for Software Engineering Jobs
        ## within 50 miles of Raleigh, NC. (This location and radius can be changed in the
        ## indeedScraper.py). getList returns a list of dictionaries, which is placed into the
        ## data list.
        data = getList()

        ## Transfer list of dictionary to JSON for returning to the front end (you can do anything
        ## here with formatting but our frontend team was more comfortable with JSON).
        response = jsonify(data);

        ## When jsonifying the dictionary list, there is a field for status_code, which we will use
        ## here for the HTTP request status returned with the dictionary. You can return any status
        ## code here to let your user know what's going on. We are using the 202 (Accepted) so the
        ## user knows that the GET action was accepted.
        response.status_code = 202

        ## Return the JSON response to the user.
        return response