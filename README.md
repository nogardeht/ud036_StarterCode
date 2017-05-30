# Movie Manager example project
This project was created for the udemy fullstack programmer course.
It was developed and tested using Python 2.7.11, execution under
other different versions could work but is not guaranteed.

All code was checked to be pep8 compliant using pep8 module:
python -m pep8 .

This programs generates HTML code with a lsit of movied that should be 
preloaded by the user into a file called "database". That file is a CSV 
that containes thedata used by the program to render the website html file.

All the interaction of the user should be done using manager.py, media.py is
part of the project and contains the classes used by the program, however it
is not intended for any user interaction.

manager.py works using arguments, and it includes a help manual that can be
called with -h or --help as per standard.


The information from the help is the following:
--------------------------------------------------------------------------------
usage: movieman.py [-h] [-d file] (-l | -r index | -a | -w | -c) [--version]

Movie database manager

optional arguments:
  -h, --help  show this help message and exit
  -d file     Indicates which CSV file to use as database. This argument is
              optional and defaults to moviedb.csv
  -l          Lists all movies on the database.
  -r index    Removes a movie from the database. The index is a number equal
              or greater that zero indicating which movie should be deleted.
              To check the index of available movies on the database use the
              listing argument.
  -a          Adds a movie to the database (Interactive).
  -w          Loads the website into the default browser.
  -c          Creates an empty movies database file.
  --version   show program's version number and exit

Example: python manager.py -d testdb.csv -l
--------------------------------------------------------------------------------

As shown, the most important command to be taken into account (still optional)
is -d that indicates the "database" file being used to render the html file.
If this parameter is not indicated it defaults to "moviedb.csv", that file is
provided as example data, and can be deleted or replaced as required.

In order to execute manager.py at least one of the arguments -l, -r, -a, -w, -c
or --version should be indicated, otherwise the program will not execute.

If any --version, -h or --help are indicated none of the other arguments will
be evaluated.

Only one of the arguments -l, -r, -a, -w, or -c could be indicated used
per execution, if two or more of those arguments are called on the same 
execution the program will fail indicating it is not possible.
Example:
--------------------------------------------------------------------------------
>C:\Python27\python.exe manager.py -l -a
usage: movieman.py [-h] [-d file] (-l | -r index | -a | -w | -c) [--version]
movieman.py: error: argument -a: not allowed with argument -l
--------------------------------------------------------------------------------

Instructions for all arguments are provided through the program help, the only 
additonal comments to the help are:
*-a is an interactive command, it will prompt for all the details during the 
execution, once all the details were provided it will display a summary
with all the information and ask for confirmation before saving the movie
to the database file indicated through the -d argument.
*-r validates the index is valid but it does not ask for any confirmation
before deleting the movie from the database file, however it confirms the 
entry was deleted with a message after its execution.
*-c creates a file that should be indicated through the -d command, if no
file was passed through the argument -d then it will use its default value. If
the file already exists it will not be deleted.
*-w Will render the the website to a file named fresh_tomatoes.html, that
file will be then launched through the default internet browser. If this file
exists it will be overwritten.