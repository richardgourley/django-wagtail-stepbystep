# Django and Wagtail step by step

A step by step reference guide with all of the steps and command line prompts required for setting up a wagtail site with the following:
- A virtual environment.
- Setting up python-decouple in order to avoid having secret keys and database passwords displayed in your settings files when using Github.
- Working with Django models
- Adding django models to the admin page
- Adding a root menu for a group of django models - eg. a folder named 'Properties' with models inside such as 'Commercial, Residential' etc.
- Setting up a MySQL database (can be left as SQLlite or adapted to Postgres as required) using InnoDB tables instead of ISAM tables.
- Setting up Bootstrap scss variables using django compress and django sass
- Setting up Vue.js if you only require it on some pages, rather than creating a full SPA.

## STEP BY STEP GUIDE

1. **If required, create a folder of choice for storing projects that contain your virtual environment projects.**
I use a folder called 'dev'. 
Go into your folder of virtual environment projects.

`mkdir Dev`

`cd Dev`

(All commands are shown using Linux/ Mac - these initial setup commands will be different for Windows.  Wagtail or Django specific commands shown later will be the same on all systems eg. 'python manage.py runserver' etc.)

2. **Check that you have python3 installed on your machine with this command.**

`python3 --version`

If this doesn't return a version number or specifies a version lower than 3.5 - download a newer version of Python.

3. **Create a virtual environment in your chosen projects folder.**

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

4. **A folder called 'projectfolder' should have been created inside your 'Dev' folder or whatever folder you have created to store your virtual environment projects from step 1. Go into this folder and activate your virtual environment.**

`cd projectfolder`

`source bin/activate`

On Windows the command to activate your virtual environment will be different, something similar to:

`mysite\env\Scripts\activate.bat`

5. **Install wagtail**

With our virtual environment up and running, the command line should say:

(projectfolder) ...../Dev/projectfolder

Now use the inluded pip installer to install wagtail:

`pip install wagtail`

6. **Start a new website project**

`wagtail start mysite`

7. **Look at the directory structure inside your projectfolder/**

```
projectfolder/
    bin/
    include/
    lib/
    mysite/
        home/
        mysite/
        search/
        .dockerignore
        DockerFile
        manage.py
        requirements.txt
    share/
```

You will see that you have 2 mysite/ directories - later in this guide, I'll refer to them as either:

- 'projectfoler/mysite' (contains 'manage.py' file.)

- 'projectfolder/mysite/mysite/' (contains all settings files.)

8. **Go into the outer mysite directory**

`cd mysite`

9. **Wagtail automatically adds a requirements.txt file. To check any other requirements are installed enter the following command.**

`pip install -r requirements.txt`

10. **Install python decouple**

Python decouple allows you to keep all sensitive project information in 1 file that you can ask github to ignore (ie. never display sensitive information in a repository).

`pip install python-decouple`

11. **Install mysqlclient**

This connects our wagtail project to a MySQL database.
(Instead, you can use sqllite which comes automatically with Django, no changes required, or you can set up any other SQL database, such as Postgres)

`pip install mysqlclient`

12. **OPTIONAL - Check dependencies are installed**

To check the above have installed and to see all other packages installed in our virtual environment, along with their version numbers, enter this:

`pip freeze`

13. **Create a gitignore file**

If you are using github for version control, it's important to create a .gitignore file.

We are going to create a '.env' file in the next steps which will contain sensitive project information.

We also want to add any other files such as auto generated folders such as migrate/

Add this to your .gitignore file:

`
# Ignore .ev file
.ev
# Ignore docker files for this project - using virtualenv
DockerFile
.dockerignore
# Ignore auto generated folders
__pycache__/
migrations/
`

14. **Set up a MySQL database for the project and assign user priveliges.**

Download MySQL if you don't already have it.  Open up MySQL and create a user, with a username of your choice IF you don't have a user to connect this project to:

`
CREATE USER newusername@localhost IDENTIFIED BY 'password'
`

Now, create the database and grant all priveliges to the user created above.

`
CREATE DATABASE mysite CHARACTER SET UTF8;
GRANT ALL ON mysite.* TO newusername@localhost;
`

NOTE!!! You will also need to grant priveliges for the testing database which will be created if you run tests.

15. **Create a file called '.env' inside 'projectfolder/mysite/' and add your site settings**

You can find your SECRET KEY inside 'projectfolder/mysite/mysite/settings/dev.py'.  
Add your secret key and your database details as shown below.

`
SECRET_KEY=12345etc.
DEBUG=True
DB_NAME=mysite
DB_USER=newusername
DB_PASSWORD=password
DB_HOST=127.0.0.1
PORT=3306
`

The db host and port number might be different with different setups.

16. **Import python decouple to read our '.env' file**

**Open 'projectfolder/mysite/mysite/settings/base.py' and add at the top after 'import os'**

`
from decouple import config
`

17. **Replace Secret key, debug info and database info from our '.env file'**

In 'projectfolder/mysite/mysite/settings/dev.py' replace the SECRET KEY and DEBUG with:

`
DEBUG = config('DEBUG', cast=bool)
SECRET_KEY = config('SECRET_KEY')
`

In 'projectfolder/mysite/mysite/settings/base.py' replace the database with this information to setup your MySQL database:

`
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USERNAME':config('DB_USER'),
        'PASSWORD':config('DB_PASSWORD'),
        'HOST':config('DB_HOST'),
        'PORT':config('PORT'),
        'OPTIONS':{
            'init_command':'SET default_storage_engine=INNODB'
        }
    }
} 
`

18. **Perform first migration**

This will set up our database tables connected to the database table we created above:

`
python manage.py migrate
`

NOTE! Subsequent migrations require 'python manage.py makemigrations' to be run before.

19. 