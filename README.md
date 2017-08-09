# Japan's Theaters Now

A simple website based off Udacity's Full Stack Nanodegree Fresh Tomatoes 
website. Japan's Theaters Now is set-up to show the current playing movies as 
well as movies being released in the near future. The goal is to automate the
collection and serving of the movie data as much as possible.

# Running the webpage

To run this website download or clone all the contents in this folder.
    git clone REPOSITORY_URL

To get the current data run API_calls.py from the command line. If you allow 
the process to keep running the data will be updated daily at 1:00 AM in Tokyo.
In order to run this file you will need to sign up for an API Key at 
https://developers.themoviedb.org/3/getting-started and replace the variable 
THEMOVIEDB_API_KEY in the code. For convenience, I have uploaded some data 
as of August 9th, 2017. If you do not want to sign up for an API Key you may 
skip this step. The server data will not update in that case.
    python3 API_calls.py

Then you can create the webpage html by running construct_site.py
    python3 construct_site.py

# Potential Issues

1. Missing data from the API does not have a fallback option. Therefore if a 
   poster_url is missing we just load unavailable.png. Similarly if a youtube
   trailer link is missing we just load a default video.
2. construct_site.py is not set to update the html file automatically. We could
   have added a similar loop as we did for the API_calls.py. I chose not to 
   because I don't think the user would appreciate the movie webpage opening
   every 24 Hours.
