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

STEP BY STEP GUIDE

1. If required, create a folder of choice for storing projects with virtual environments. 
Go into this folder (commands shown using Linux/ Mac, follow equivalent windows command line instructions.)

cd Dev

2. Check your default version of Python in the command line.

python3 --version

If this doesn't return a version number or specifies a version lower than 3.5 - download a newer version of Python.