import media
import json
import time
import fresh_tomatoes


with open('./JSON/upcoming/output/combined_upcoming.json') as file:
    upcoming = json.load(file)

with open('./JSON/now_playing/output/combined_now_playing.json') as file:
    now_playing = json.load(file)

with open('./JSON/trailers/output/combined_trailers.json') as file:
    trailers = json.load(file)

DEFAULT_YOUTUBE = "https://www.youtube.com/watch?v=nu8-7huFyvo"

upcoming_titles = []
upcoming_storylines = []
upcoming_release_dates = []
upcoming_posters = []
upcoming_ids = []
upcoming_trailer_url = []

now_playing_titles = []
now_playing_storylines = []
now_playing_release_dates = []
now_playing_posters = []
now_playing_ids = []
now_playing_trailer_url = []

def find_trailer(movie_id, file):
    """ This function searches a json file for the youtube link of the trailer.

    Arguments:
    movie_id - [array] - array of integers corresponding to movie ids
        file - [json]  - a json file with information on movie trailers.
    """
    for objects in file:
        if(objects['results']): # Checks to make sure results is not empty
            if(objects['id']==movie_id):
                youtube_url="https://www.youtube.com/watch?v=" + objects['results'][0]['key'] # NOQA
                return youtube_url
    return DEFAULT_YOUTUBE

for objects in upcoming:
    for results in objects['results']:
        upcoming_titles.append(results['title'])
        upcoming_storylines.append(results['overview'])
        upcoming_release_dates.append(results['release_date'])
        if(results['poster_path']):
            upcoming_posters.append("https://image.tmdb.org/t/p/w500/" + 
                                    results['poster_path'])
        else:
            upcoming_posters.append('./unavailable.png')
        movie_id=results['id']
        trailer_url=find_trailer(movie_id, trailers)
        upcoming_trailer_url.append(trailer_url)



for objects in now_playing:
    for results in objects['results']:
        time_convert = time.mktime(time.strptime(results['release_date'], 
                                                 "%Y-%m-%d"))
        time_diff_jp = 60 * 60 * 9
        if(time_convert > time.time() + time_diff_jp):
            upcoming_titles.append(results['title'])
            upcoming_storylines.append(results['overview'])
            upcoming_release_dates.append(results['release_date'])
            if(results['poster_path']):
                upcoming_posters.append("https://image.tmdb.org/t/p/w500/" + 
                                        results['poster_path'])
            else:
                upcoming_posters.append('./unavailable.png')
            movie_id=results['id']
            trailer_url=find_trailer(movie_id, trailers)
            upcoming_trailer_url.append(trailer_url)
        else:
            now_playing_titles.append(results['title'])
            now_playing_storylines.append(results['overview'])
            now_playing_release_dates.append(results['release_date'])
            if(results['poster_path']):
                now_playing_posters.append("https://image.tmdb.org/t/p/w500/" + 
                                           results['poster_path'])
            else:
                now_playing_posters.append('./unavailable.png')
            movie_id=results['id']
            trailer_url=find_trailer(movie_id, trailers)
            now_playing_trailer_url.append(trailer_url)




upcoming_movie_objects = []
now_playing_movie_objects = []

for i in range(0, len(upcoming_titles)):
    create_movie_object = media.Movie(  upcoming_titles[i],
                                        upcoming_storylines[i],
                                        upcoming_posters[i],
                                        upcoming_trailer_url[i],
                                        upcoming_release_dates[i])
    upcoming_movie_objects.append(create_movie_object)

for i in range(0, len(now_playing_titles)):
    create_movie_object = media.Movie(  now_playing_titles[i],
                                        now_playing_storylines[i],
                                        now_playing_posters[i],
                                        now_playing_trailer_url[i],
                                        now_playing_release_dates[i])
    now_playing_movie_objects.append(create_movie_object)

all_movie_objects = []
all_movie_objects.extend(upcoming_movie_objects)
all_movie_objects.extend(now_playing_movie_objects)

# fresh_tomatoes.py takes in a list of media.Movie objects and generates html 
# code to be delivered. The website is also automatically opened in the 
# browser.
fresh_tomatoes.open_movies_page(all_movie_objects)