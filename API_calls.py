import time
import httplib2
import json
import os
import io


THEMOVIEDB_API_KEY = "REDACTED"

h = httplib2.Http()


def save_json(directory, file_name, json_data):
    """ saves results from an httplib2.Http() request into a file.
        Arguments:
        directory - [string] - directory to save data with trailing /
        file_name - [string] - file name to call the file. String should be in 
                               the form FILENAME.ext
        json_data - this is a string version of the results from httplib2.Http()
                    in utf8.
    """

    # Found this save version on stackoverflow because it was a cleaner output 
    # than my first pass
    # https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file # NOQA
    try:
        to_unicode = unicode
    except NameError:
        to_unicode = str

    with io.open(directory+file_name, 'w', encoding='utf8') as outfile:
        str_ = json.dumps(json_data,
                          indent=4, sort_keys=True,
                          separators=(',', ': '), ensure_ascii=False)

        outfile.write(to_unicode(str_))


def themoviedb_upcoming():
    """Sends an API request to themoviedb.org for upcoming releases in Japan."""
    request_url = "https://api.themoviedb.org/3/movie/upcoming?api_key=%s&language=en-US&region=JP" %(THEMOVIEDB_API_KEY) # NOQA

    directory = "./JSON/upcoming/"
    # Create the directory if it does not exist.
    os.makedirs(directory, exist_ok=True)
    response, results = h.request(request_url, 'GET')

    # Verify the API Call was completed successfully
    if(response['status'] == '200'):
        str_results = str(results, 'utf8')
        json_results = json.loads(str_results)
        save_json(directory, 'upcoming.JSON', json_results)

        if(json_results['total_pages'] > 1):
            for i in range (2, json_results['total_pages'] + 1):
                request_url="https://api.themoviedb.org/3/movie/now_playing?api_key=%s&language=en-US&page=%s&region=JP" %(THEMOVIEDB_API_KEY, str(i)) # NOQA
                response, results = h.request(request_url, 'GET')
                str_results = str(results, 'utf8')
                new_json_results = json.loads(str_results)
                save_json(directory, 'now_playing%s.JSON' %(i),new_json_results)
    else:
        print(time.ctime(), "ERROR in API_calls.py : themoviedb_upcoming() " 
                            "Status:", response['status'])


def themoviedb_now_playing():
    """
    Sends an API request to themoviedb.org for movies now_playing in theaters
    in Japan.
    """
    request_url = "https://api.themoviedb.org/3/movie/now_playing?api_key=%s&language=en-US&region=JP" %(THEMOVIEDB_API_KEY) # NOQA

    directory = "./JSON/now_playing/"
    os.makedirs(directory, exist_ok=True)
    response, results = h.request(request_url, 'GET')
    if(response['status'] == '200'):
        str_results = str(results, 'utf8')
        json_results = json.loads(str_results)
        save_json(directory, 'now_playing.JSON', json_results)

        if(json_results['total_pages'] > 1):
            for i in range (2, json_results['total_pages'] + 1):
                request_url="https://api.themoviedb.org/3/movie/now_playing?api_key=%s&language=en-US&page=%s&region=JP" %(THEMOVIEDB_API_KEY, str(i)) # NOQA
                response, results = h.request(request_url, 'GET')
                str_results = str(results, 'utf8')
                new_json_results = json.loads(str_results)
                save_json(directory, 'now_playing%s.JSON' %(i),new_json_results)
    else: 
        print(time.ctime(), "ERROR in API_calls.py : themoviedb_now_playing() "
                            "Status:", response['status'])


def themoviedb_trailer_search(movie_id_array, directory):
    """ 
    Send and API request to themoviedb.org for each movie id in the given 
    movie_id_array
    Arguments: 
    movie_id_array - [array] movie id's as given by themoviedb.org search API or
                             movie API
    directory - [string] directory of where to save the results with trailing /
    """
    os.makedirs(directory, exist_ok=True)
    for movies in movie_id_array:
        request_url = "https://api.themoviedb.org/3/movie/%s/videos?api_key=%s" %(str(movies), THEMOVIEDB_API_KEY ) # NOQA
        resp, results = h.request(request_url, 'GET')
        str_results = str(results,'utf8')
        json_results = json.loads(str_results)
        save_json(directory, '%s.JSON' %(str(movies)), json_results)
        print(time.ctime(), "TRAILER INFO SAVED:", str(movies))


def combine_results(directory, file_name):
    """
    Loads and saves all the results from JSON files in a directory into a new 
    JSON file. This file is named as file_name.JSON
    Arguments:
    directory - [string] directory that contains JSON files to combine.
    file_name - [string] desired file_name in format FILENAME.JSON
    """
    output=[]
    os.makedirs(directory+"/output/", exist_ok=True)
    for files in os.listdir(directory):
        if(files.endswith(".json") or files.endswith(".JSON")):
            with open(directory + "/" + files) as file:
                current_file = json.load(file)
                output.append(current_file)
    save_json(directory + "/output/", file_name,output)
    print(time.ctime(), "COMBINED FOLDER :", directory)


def get_movie_ids(directory,file_name):
    """
    After having some results from themoviedb_upcoming() or 
    themoviedb_now_playing() we use this to extract the movie ids.
    Arguments:
    directory - [string] The directory of the json file with the results with trailing /.
    file_name - [string] name of the json file.
    """
    movie_ids = []
    with open(directory+file_name) as file:
        temp_file = json.load(file)
    for objects in temp_file:
        for results in objects['results']:
            movie_ids.append(results['id'])
    return movie_ids


def update_server_info():
    """
    Call this function when you want to update all the json information at once.
    These include themoviedb_upcoming(), themoviedb_now_playing(), 
    themoviedb_trailer_search(). All the results will also be combined via 
    combine_results().
    """
    themoviedb_upcoming()
    themoviedb_now_playing()
    combine_results("./JSON/upcoming/", "combined_upcoming.json")
    combine_results("./JSON/now_playing/", "combined_now_playing.json")
    upcoming_ids = get_movie_ids("./JSON/upcoming/output/",
                                 "combined_upcoming.json")
    now_playing_ids = get_movie_ids("./JSON/now_playing/output/",
                                    "combined_now_playing.json")
    themoviedb_trailer_search(upcoming_ids, "./JSON/trailers/")
    themoviedb_trailer_search(now_playing_ids, "./JSON/trailers/")
    combine_results("./JSON/trailers/", "combined_trailers.json")


# On first run this file will always update the server information.
update_server_info()
print(time.ctime(),"SERVER UPDATED")

# Finds time difference in Japan
time_diff_jp=60*60*9
time_now= time.time()
time_until_1am_jp = (86400+(60*60)) - ((time_now+time_diff_jp) % 86400)
time.sleep(time_until_1am_jp)

while(True): # Updates Daily
    update_server_info()
    print("Current server data saved at: ", time.ctime())
    time.sleep(60*60*24)
