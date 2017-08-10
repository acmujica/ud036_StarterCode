import webbrowser

class Movie():
    """The class Movie describes the basic building blocks to describe the 
    parts of our movie_tile. For more information about the arguments please
    see the __init__ function.
    """
    def __init__(self, title, storyline, poster_url, trailer_url, release_date):
        """Arguments:
                title - [string] - The movie title.
            storyline - [string] - Overview of the movie plot.
           poster_url - [string] - URL to the location of the movie poster file.
          trailer_url - [string] - Typically a youtube trailer link
        release_dates - [string] - Contains the release_date of the movie.
        """
        self.title = title
        self.storyline = storyline
        self.poster_url = poster_url
        self.trailer_url = trailer_url
        self.release_date = release_date

    def show_trailer(self):
        """Opens the movie as provided by the trailer_url argument."""
        webbrowser.open(self.trailer_url)