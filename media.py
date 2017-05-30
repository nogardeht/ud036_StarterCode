import csv
import webbrowser


"""This file is used as a module and no main program
executable code should be placed here"""


class Video(object):
    """This Video class is not intended to be used as a main class,
    it is just a template we use for subclasses"""

    def __init__(self, title, duration, language):
        self.title = title
        self.duration = duration
        self.language = language


class Movie(Video):
    """This class provides a way to store movie related information.
Available properties:
    title: The title of the movie
    duration: The duration of the movie
    language: The language of the movie
    storyline: A brief description of the movie
    poster_image_url: A url to the image of the poster
    trailer_youtube_url: A url to the trailer in youtube
    movie_rate: The rate of the movies. Only ratings of property VALID_RATINGS are valid.
    VALID_RATINGS: The valid ratings for any movie of this class"""
    VALID_RATINGS = ["G", "PG", "PG-13", "R"]

    def __init__(self, movie_title, duration, movie_storyline,
                 poster_imageUrl, trailer_youtubeUrl, movie_language, movie_rate):
        Video.__init__(self, movie_title, duration, movie_language)
        self.storyline = movie_storyline
        self.poster_image_url = poster_imageUrl
        self.trailer_youtube_url = trailer_youtubeUrl
        if movie_rate in self.VALID_RATINGS:
            self.rate = movie_rate
        else:
            raise Exception(ValueError('The rate for ' + movie_title +
                                       ' is not a valid rate'))

    def show_trailer(self):
        webbrowser.open(self.trailer_youtube_url)

    def __str__(self):
        return 'Movie: {0}, Duration: {1}, Lang: {2}'.format(self.title,
                                                             self.duration, self.language)


class MoviesStore(object):
    """This class provides a way to store a list of movies.
Available properties:
    moviesList: A list with all the movies (Internal use)
    len: The amount of movies stored on this class (Internal use)
Available methods:
    load_movies(csvpath): This will automatically load all the movies from a provided csv file path into moviesList
    add_movie(movie): Adds a movie to moviesList, the parameter should provide an object of type Movie
    del_movie(index): Removes a movie from moviesList based on its index, the input parameter is an integer
    get_movie(index): Returns an object of type Movie with the movie on the index position provided of moviesList
    get_movies(): Returns the whole list of movies
    save_movies(csvpath): Saves the list of moviesList to a provided csv file path
    create_moviesdb(csvpath): Creates a empty file to be used as a database
Comments
    1. __str__ returns a formated summary of the movies in moviesList, the index is indicated in that summary in order to facilitate the use of other functions.
    2. __len__ returns an integer that is the amount of movies in moviesList"""

    def __init__(self):
        # Initialized as empty
        self.moviesList = []
        # We could use also the len of self.moviesList.
        # To be improved in a future version
        self.len = 0

    def __str__(self):
        # Prints all movies on the store with index in front
        # This is used to build up the string below that
        # displays the position of each movie
        index = 0
        movieSumm = []  # This will store all existing movies
        for movie in self.moviesList:
            movieSumm.append('Position: {4}, Movie: "{0}", Duration: "{1}", \
Language: "{2}", Rate: "{3}"'.format(movie.title, movie.duration,
                                     movie.language, movie.rate, index))
            index += 1
        # This returns a line separated summary of available movies
        return '\n'.join(movieSumm)

    def __len__(self):
        return self.len

    def load_movies(self, csvpath):
        with open(csvpath, 'rb') as csvFile:
            moviesReader = csv.reader(csvFile, delimiter=',', quotechar='"')
            for row in moviesReader:
                newMovie = Movie(row[0], row[1], row[2], row[3], row[4],
                                 row[5], row[6])
                self.add_movie(newMovie)

    def add_movie(self, movie):
        self.moviesList.append(movie)
        self.len += 1

    def del_movie(self, index):
        try:
            self.moviesList.pop(index)
            self.len -= 1
        except IndexError:
            print "Non valid index provided"

    def get_movie(self, index):
        try:
            return self.moviesList[index]
        except IndexError:
            print "Non valid index provided"

    def get_movies(self):
        return self.moviesList

    def save_movies(self, csvpath):
        if len(self) > 0:
            with open(csvpath, 'wb') as csvfile:
                moviesWriter = csv.writer(csvfile, delimiter=',',
                                          quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for movie in self.get_movies():
                    moviesWriter.writerow([movie.title, movie.duration,
                                           movie.storyline, movie.poster_image_url,
                                           movie.trailer_youtube_url, movie.language, movie.rate])

    def create_moviesdb(self, csvpath):
        open(csvpath, 'a')
