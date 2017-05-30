import argparse  # Used to evaluate arguments
# Used to obtain all values passed to this program when called
import sys
import re  # Will be used to validate user inputs in case of -a argument
# Used to validate the existence of the database file with os.path.exists
import os.path

import fresh_tomatoes  # Provided by udacity, used to render the website
import media  # This custom module contains custom classes to store our data

# We customize the argument parser for our program
# It will display an examples section at the end
parser = argparse.ArgumentParser(prog='movieman.py',
                                 description='Movie database manager', epilog='Example: \
    python manager.py -d testdb.csv -l')

# Now we add the arguments that we will use for our logic
# This will be used to indicate the file
parser.add_argument('-d', action='store', type=str, required=False,
                    default='moviedb.csv', help='Indicates which CSV file to use as database. \
    This argument is optional and defaults to moviedb.csv', metavar='file')

"""We create this mutually exclusive group because we don't want to allow
launching the site, creating a new db file, listing, deleting and adding
movies all at the same time."""
group = parser.add_mutually_exclusive_group(required=True)

# This will be used to list all movies
group.add_argument('-l', action='store_true', required=False,
                   help='Lists all movies on the database.')

# This will be used to remove a movie
group.add_argument('-r', action='store', type=int, required=False,
                   help='Removes a movie from the database. The index is a number \
    equal or greater that zero indicating which movie should be deleted. \
    To check the index of available movies on the database use the listing \
    argument.', metavar='index')

# This will be used to add a movie
group.add_argument('-a', action='store_true', required=False,
                   help='Adds a movie to the database (Interactive).')

# Used to render the website and launch it through the default browser
group.add_argument('-w', action='store_true', required=False,
                   help='Loads the website into the default browser.')

# This will be used to create a new empty database file
group.add_argument('-c', action='store_true', required=False,
                   help='Creates an empty movies database file.')

# This simply prints the version of the program
parser.add_argument('--version', action='version', version='%(prog)s 0.1')

"""Now we parse the arguments passed to this program when called.
Te reason we skip the first one is that the first element is the path
of the file that was called, and that is not a valid argument.
The actual parsing is done by vars, who will parse a object of type
NameSpace that is returned by parse_args, and parse_args parses a list,
in this case sys.argv that is basically a list with all the arguments
passed to the program in the same order than provided. vars returns
a dictionary and then we will use that dictionary to build up the logic
of each case."""
inargs = vars(parser.parse_args(sys.argv[1:]))

# Create a new MoviesStore to be used during the execution of this program
tempMoviesStore = media.MoviesStore()

if (not inargs['c']):
    # Validate the existence of the file
    if (not os.path.exists(inargs['d'])):
        print("File {0} is not valid.".format(inargs['d']))
        exit(2)
    else:
        # Loading the database indicated on argument -d
        # (Or using the default value)
        tempMoviesStore.load_movies(inargs['d'])

# Acting depending on the arguments used
if (inargs['l']):  # List the movies on console
    print(tempMoviesStore)

elif (inargs['a']):  # Add a new movie
    # Initializing empty variables
    movie_title = ""
    duration = ""
    movie_storyline = ""
    poster_imageUrl = ""
    trailer_youtubeUrl = ""
    movie_language = ""
    movie_rate = ""
    print('Please enter movie details below (To cancel press control+c):')
    while (movie_title == ""):
        movie_title = raw_input('Movie title --> ')
        if (movie_title == ""):
            print "Movie's title cannot be empty."
    while (duration == ""):
        duration = raw_input('Movie duration (Format mm:ss, example for 1 \
hour, 10 minutes and 30 seconds: 70:30)--> ')
        if (duration == ""):
            print "Movie's duration cannot be empty."
        # Validates that the format of the input is MM:SS
        elif (not re.match("^((\d\d?\d):)([0-5]\d)$", duration)):
            print "Duration is not valid."
            duration = ""
    while (movie_storyline == ""):
        movie_storyline = raw_input('Movie description --> ')
        if (movie_storyline == ""):
            print "Movie's description cannot be empty."
    while (poster_imageUrl == ""):
        poster_imageUrl = raw_input('Movie poster image url --> ')
        if (poster_imageUrl == ""):
            print "Movie's poster image url cannot be empty."
        # Validates that the format of the url, can be improved, \
        # validation can be done directly on the class and raise and exception
        elif (not re.match('(\b(https?)://)?[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]',
                           poster_imageUrl)):
            print ("Not a valid URL")
            poster_imageUrl = ""
    while (trailer_youtubeUrl == ""):
        trailer_youtubeUrl = raw_input('Movie youtube trailer url --> ')
        if (trailer_youtubeUrl == ""):
            print "Movie's youtube trailer url cannot be empty."
        # Validates that the format of the url, can be improved, \
        # validation can be done directly on the class and raise and exception
        elif (not re.match('(\b(https?)://)?[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]',
                           trailer_youtubeUrl)):
            print ("Not a valid URL")
            trailer_youtubeUrl = ""
    while (movie_language == ""):
        movie_language = raw_input('Movie language --> ')
        if (movie_language == ""):
            print "Movie's language cannot be empty"
    while (movie_rate == ""):
        movie_rate = raw_input('Movie rate (Valid rates: {0}) \
        --> '.format(media.Movie.VALID_RATINGS))
        if (movie_rate == ""):
            print "Movie's rate cannot be empty"
        elif (movie_rate not in media.Movie.VALID_RATINGS):  # Validates the rate
            print "Provided rate is not valid."
            movie_rate = ""
    # Confirmation before saving
    print("Details entered: \n \
    Title: {0}\n \
    Duration: {1}\n \
    Description: {2}\n \
    Poster URL: {3}\n \
    Youtube trailer URL: {4}\n \
    Language: {5}\n \
    Rate: {6}\n".format(movie_title, duration, movie_storyline,
                        poster_imageUrl, trailer_youtubeUrl, movie_language, movie_rate))

    confirmation = ""
    while (confirmation == ""):
        confirmation = raw_input("Enter Y to confirm and save the movie to the \
database or press N to cancel: ")
        if confirmation == "" or confirmation not in ("Y", "N", "y", "n"):
            print("Please enter Y or N")
            confirmation = ""
    tempMoviesStore.add_movie(media.Movie(movie_title, duration,
                                          movie_storyline, poster_imageUrl, trailer_youtubeUrl, movie_language, movie_rate))
    # This saves the database with the modifications
    tempMoviesStore.save_movies(inargs['d'])

elif (inargs['r'] is not None):  # Removes a movie
    # We have to check if the provided index is a valid one
    if (inargs['r'] > (len(tempMoviesStore) - 1) or inargs['r'] < 0):
        print('The provided index number is invalid')
        exit(1)  # If it is not valid we announce a message and exit with RC:1
    tempMovieName = tempMoviesStore.get_movie(inargs['r']).title
    tempMoviesStore.del_movie(inargs['r'])
    tempMoviesStore.save_movies(inargs['d'])
    print tempMovieName + ' was deleted and the database was saved.'
    # tempMoviesStore.save_movies(inargs['d'])

elif (inargs['c']):  # Add a new movie
    # Try to create the new database
    try:
        tempMoviesStore.create_moviesdb(inargs['d'])
    # If there was any proble show a message and the error message
    except Exception:
        print('There was a problem creating the new database.')
        raise

elif (inargs['w']):  # Load the website
    print(fresh_tomatoes.open_movies_page(tempMoviesStore.get_movies()))
