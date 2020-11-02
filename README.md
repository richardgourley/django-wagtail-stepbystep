# Django and Wagtail step by step

A step by step reference guide with all of the steps and command line prompts required for setting up a wagtail site with the following:
- A virtual environment.
- Setting up python-decouple in order to avoid having secret keys and database passwords displayed in your settings files when using Github.
- Working with Django models
- Adding django models to the admin page
- Adding a root menu for a group of django models - eg. a folder named 'Properties' with models inside such as 'Commercial, Residential' etc.
- Setting up a MySQL database (can be left as SQLlite or adapted to Postgres as required.)
- Setting up Bootstrap scss variables using django compress and django sass
- Setting up Vue.js if you only require it on some pages, rather than creating a full SPA.

## STEP BY STEP GUIDE

1. *If required, create a folder of choice for storing projects that contain your virtual environment projects.*
I use a folder called 'dev'. 
Go into your folder of virtual environment projects.

`mkdir Dev`
`cd Dev`

(All commands are shown using Linux/ Mac - these initial setup commands will be different for Windows.  Wagtail or Django specific commands shown later will be the same on all systems eg. 'python manage.py runserver' etc.)

2. *Check that you have python3 installed on your machine with this command.*

`python3 --version`

If this doesn't return a version number or specifies a version lower than 3.5 - download a newer version of Python.

3. *Create a virtual environment in your chosen projects folder.*

You can set this up by using 'virtualenv' or 'venv'. I use 'virtualenv'.
You might already have either or both of the above installed on your machine.

A) VIRTUALENV
- Check if you have 'virtualenv' installed on your machine by checking the version number.

`virtualenv --version`

- If you have this installed, you can create a virtual environment (specifying the use of Python3 because some machines use Python2 as default!)

`virtualenv projectfolder -p python3`

B) VENV
- You can try to create a virtual environment by typing: 

`python3 -m venv projectfolder`

- NOTE: 'venv' should come with Python3 but on some systems such as Debian/ Ubuntu you will need to run 'apt-get install python3-venv' to install the 'python3-venv' package.

4. *A folder called 'projectfolder' should have been created inside your 'Dev' folder or whatever folder you have created to store your virtual environment projects from step 1. Go into this folder and activate your virtual environment.*

`cd projectfolder`
`source bin/activate`

On Windows the command to activate your virtual environment will be different, something similar to:

`mysite\env\Scripts\activate.bat`

