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

- Customizing the wagtail admin with a custom logo, custom welcome message and custom login page message.

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

==============================================================

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

- 'projectfolder/mysite' (contains 'manage.py' file.)

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

We also want to add any other files such as auto generated folders such as migrations/

Add this to your .gitignore file:

```
.env
DockerFile
.dockerignore
__pycache__/
migrations/
```

==============================================================

14. **Set up a MySQL database for the project and assign user priveliges.**

Download MySQL if you don't already have it.  Open up MySQL and create a user, with a username of your choice IF you don't have a user to connect this project to:

`
CREATE USER newusername@localhost IDENTIFIED BY 'password'
`

Now, create the database and grant all priveliges to the user created above.

```
CREATE DATABASE mysite CHARACTER SET UTF8;
GRANT ALL ON mysite.* TO newusername@localhost;
```

NOTE!!! You will also need to grant priveliges for the testing database which will be created if you run tests.

15. **Create a file called '.env' inside 'projectfolder/mysite/' and add your site settings**

You can find your SECRET KEY inside 'projectfolder/mysite/mysite/settings/dev.py'.  
Add your secret key and your database details as shown below.

```
SECRET_KEY=12345etc.
DEBUG=True
DB_NAME=mysite
DB_USER=newusername
DB_PASSWORD=password
DB_HOST=127.0.0.1
PORT=3306
```

The db host and port number might be different with different setups.

16. **Import python decouple to read our '.env' file**

**Open 'projectfolder/mysite/mysite/settings/base.py' and add at the top after 'import os'**

`
from decouple import config
`

17. **Replace Secret key, debug info and database info from our '.env file'**

In 'projectfolder/mysite/mysite/settings/dev.py' replace the SECRET KEY and DEBUG with:

```
DEBUG = config('DEBUG', cast=bool)
SECRET_KEY = config('SECRET_KEY')
```

In 'projectfolder/mysite/mysite/settings/base.py' replace the database with this information to setup your MySQL database:

```
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
```

NOTE: 

18. **Perform first migration**

This will set up our database tables connected to the database table we created above:

`
python manage.py migrate
`

NOTE! Subsequent migrations require 'python manage.py makemigrations' to be run before.

==============================================================

19. **Create a super user account for the admin**

A superuser account will grant you all priveliges inside the Wagtail admin.

Enter this and create a username and password

`python manage.py createsuperuser`

20. **Test server is up and running**

`python manage.py runserver`

You should see a message giving you the URL of your site to visit.

=================================================

SETTING UP BOOTSTRAP .SCSS FILES

You need to install 2 dependencies to get bootstrap up and running with .scss variables that make changing basic bootstrap settings much easier and more managable.

21. **Install django_compressor**

`pip install django_compressor`

`pip install django-libsass`

22. **Add 'compressor' to installed apps to use it**

Go to 'projectfolder/mysite/mysite/settings/base.py' and add 'compressor' to installed apps as shown here:

```
INSTALLED_APPS = [
    'home',
    'search',
    'compressor',
    ....
    ....
]
```

23. **You also need to modify STATICFILES_FINDERS by adding compressor.finders.CompressorFinder as follows.**

```
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]
```

24. **At the bottom of your 'settings/base.py', activate compress precompilers as follows:**

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

25. **Download bootstrap from getbootstrap.com**

26. **Add bootstrap scss and js files**

27. **Create folders inside 'mysite/static' to add bootstrap files**

Create directories inside the 'css' and 'js' directories of 'projectname/mysite/mysite/static' as follows:

```
projectfolder/
  mysite/
    mysite/
      static/
        css/
          bootstrap/
            scss/
        mysite.css
        js/
          bootstrap/
            js/
        mysite.js
```

28. **Inside the 'css/bootstrap/scss' directory and the 'js/bootstrap/js' directory copy over the scss files and js files from your bootstrap download.**

29. **Create a 'theme.scss' file where we can import and override bootstrap.scss variables easily.**

Directly inside 'projectfolder/mysite/mysite/static' create a 'theme.scss' file so your directory structure looks like this:

```
projectfolder/
  mysite/
    mysite/
      static/
        css/
          bootstrap/
            scss/
        mysite.css
        js/
          bootstrap/
            js/
        mysite.js
      theme.scss
```

30. **Open up the 'theme.scss' created above and modify a few bootstrap variables to test , and import the bootstrap.scss variables**

```
$primary: purple;
$secondary: orange;

@import 'css/bootstrap/scss/bootstrap.scss';
```

=================================================

BASE.HTML

In django and wagtail projects, the base.html file is the html page that calls content from other templates inside {% block content%} and is used as the base of every page.

It contains headers, and you can include a navbar, footer and a sidebar if required.

31. **Check that wagtail automatically created and added a general site css and js file**

You should see this in the base.html file located at 'projectfolder/mysite/mysite/templates':

```
...
{# Global stylesheets #}
<link rel="stylesheet" type="text/css" href="{% static 'css/languageschoolmanager.css' %}">

.....

{# Global javascript #}
<script type="text/javascript" src="{% static 'js/languageschoolmanager.js' %}"></script>

<body>
```

32. **Load compress and add our 'theme.scss' file**

In 'base.html' add this at the top under '{% load static wagtailuserbar %}':

`{% load compress %}`

Then after our {# Global stylesheets #} add our compressed scss file:

```
{% compress css %}
<link type="text/x-scss" href="{% static 'theme.scss' %}" rel="stylesheet" media="screen">
{% endcompress %}
```

33. **Load any Bootstrap JS files as you require them as shown below. Remove ones you don't need.**

In 'base.html', under {# Global javascript #}

```
{# Bootstrap javascript #}
<script type="text/javascript" src="{% static 'js/bootstrap/js/src/dropdown.js' %}"></script>
<script type="text/javascript" src="{% static 'js/bootstrap/js/src/carousel.js' %}"></script>
```

=================================================

34. **Vue.JS - If you only want to use Vue on some pages you can use the {% block extra js%} tags**

In 'base.html' you will see this:

```
{% block extra_js %}
   {# Override this in templates to add extra javascript #}
{% endblock %}
```

You can add the code below to any template files you create where you want to add Vue.js, and load Vue via a DNS like this:

```
{% block extra_js %}
  <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
{% endblock %}
```

=================================================

HOME / HOME PAGE

35. **Remove links to welcome page from home page**

In 'projectfolder/mysite/home/templates/home/home_page.html' you can delete the welcome page css link and 'include' welcome page, and all comments..

```
...
{% comment %}
Delete the line below if you're just getting started and want to remove the welcome screen!
{% endcomment %}
<link rel="stylesheet" href="{% static 'css/welcome_page.css' %}">
...
{% comment %}
Delete the line below if you're just getting started and want to remove the welcome screen!
{% endcomment %}
{% include 'home/welcome_page.html' %}
``` 

36. **Delete unrequired welcome_page.html and welcome_page.css**

Delete the 'welcome_page.css' file from 'projectname/mysite/home/static/css/'

Delete the 'welcome_page.html' file from 'projectname/mysite/home/templates/home/'

37. **Test our bootstrap setup is working**

In 'home/templates/home/home_page.html' add some html with bootstrap classes, within block content tags, similar to below to test our 'themes.scss' file has loaded correctly.

```
{% block content %}
<h1 class="text-secondary">Hello world!</h1>
<h2 class="text-primary">How are you?</h2>
{% endblock %}
```

================================================

CUSTOMIZE THE WAGTAIL ADMIN DASHBOARD

Run the server if not running and log in to your wagtail dashboard - url/admin

You can easily modify the logo, the site title and the login page title by creating a dashboard app and extending soem admin templates.

38. **Start a new app called dashboard**

In the command line, with our virtual environment running, enter

`python manage.py startapp dashboard`


39. **Delete unneeded files from our dashboard app**

Here, we only need to keep '__init__.py' and 'apps.py', so you can delete 'views.py', 'models.py', 'admin.py', 'tests.py'

40. **Register our new 'dashboard' app**

In 'projectfolder/mysite/mysite/settings/base.py' add dashboard to installed apps:

```
INSTALLED_APPS = [
    'home',
    'search',
    'compressor',

    'dashboard',
]
```

41. **Create an images folder in our site static folder and add a custom logo**

```
projectfolder/
  mysite/
    static/
      images/
        custom-logo.jpg
```

42. **In the dashboard app directory, create a new directory called templates and inside templates, create a directory called wagtailadmin***

```
projectfolder/
  mysite/
    dashboard/
      templates/
        wagtailadmin/
```

43. **In 'dashboard/templates/wagtailadmin/' create a file called 'base.html'**

This extends the admin base html file and we override the branding logo with our own custom one.

```
{% extends "wagtailadmin/base.html" %}

{% load static %}

{% block branding_logo %}
  <img src="{% static 'images/custom-logo.jpg' %}" alt="My Site" width="80" />
{% endblock %}
```

44. **In 'dashboard/templates/wagtailadmin/' create a file called 'home.html'**

This overrides the welcome message in our admin page:

```
{% extends "wagtailadmin/home.html" %}

{% block branding_welcome %}Welcome to My Site{% endblock %}
```

45. **In 'dashboard/templates/wagtailadmin/' create a file called 'login.html'**

This overrides the message you see when you go to log in at the admin page:

```
{% extends "wagtailadmin/login.html" %}

{% block branding_login %}Sign in to My Site{% endblock %}
```

=================================================

DJANGO MODELS -
MODEL ADMIN allows you to add django models to the admin page.

You can use django fields AND wagtail fields on your models, so you can enhance the best parts of Django with more fields and you can then integrate your models into Wagtail pages.

Let's create a new app called 'surgeries' and it's models, and create and add models to the admin dashboard under a menu heading called 'MANAGE SURGERIES'

46. **Start new app**

`python manage.py startapp surgeries`

47. **Add 'surgeries' to installed apps**

In 'projectfolder/mysite/mysite/settings/base.py' add 'surgeries' to installed apps

```
INSTALLED_APPS = [
    'home',
    'search',
    'compressor',
    'dashboard',
    'surgeries',
```

48. **Add model admin to installed apps**

In order to access modeladmin, we also need to add it to installed apps:

```
INSTALLED_APPS = [
    'home',
    'search',
    'compressor',
    'dashboard',
    'surgeries',

    'wagtail.contrib.modeladmin',
```

49. **Create the models**

In this simple example we can add ForeignKeys and ManyToManyFields to link all of the models together making a scalable application.  Add these models to 'surgeries/models.py'

NOTE: Verbose plural names added to 'city' and 'surgery' models to correctly display the plural name of each in the admin.


NOTE: Extra methods created in 'Doctor' and 'Surgery' to display the ManyToMany fields in the admin dashboard list_display.

```
from django.db import models

# Create your models here.
class MedicalSpecialization(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class City(models.Model):
    class Meta:
        verbose_name = 'city'
        verbose_name_plural = 'cities'
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    first_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    specializations = models.ManyToManyField(MedicalSpecialization, help_text='Select 1 or more specializations.')

    def __str__(self):
        return self.first_name + ' ' + self.surname

    def specializations_list(self):
        return ', '.join(specialization.name for specialization in self.specializations.all())

class Surgery(models.Model):
    class Meta:
        verbose_name = 'surgery'
        verbose_name_plural = 'surgeries'
    surgery_name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    doctors = models.ManyToManyField(Doctor, help_text='Select which doctors are based at this surgery.')

    def __str__(self):
        return self.surgery_name

    def doctors_list(self):
        return ', '.join(doctor.surname for doctor in self.doctors.all())

```

50. **Make migrations and migrate**

To set up the new models in the database, run these commands one after the other:

`python manage.py makemigrations`

`python manage.py migrate`

51. **Create 'wagtail_hooks.py'**

To connect our new models to the wagtail admin dashboard, create a new file called 'wagtail_hooks.py' directly inside our 'surgeries' directory.

52. **Set up wagtail hooks imports and import surgery models**

Add these imports to the top of 'surgeries/wagtail_hooks.py'

```
from wagtail.contrib.modeladmin.options import (
        ModelAdmin, ModelAdminGroup, modeladmin_register)
from . models import MedicalSpecialization, City, Doctor, Surgery
```

53. **Create OBJECTADMIN for each model**

Add an instance of ModelAdmin for each model to 'surgeries/wagtail_hooks.py'.

NOTE! In 'DoctorAdmin' and 'SurgeryAdmin' list_display, we add in methods from the models in 'surgeries/models.py' in order to display ManyToMany Fields as a string in the admin page. 

```
from wagtail.contrib.modeladmin.options import (
        ModelAdmin, ModelAdminGroup, modeladmin_register)
from . models import MedicalSpecialization, City, Doctor, Surgery

class MedicalSpecializationAdmin(ModelAdmin):
    model = MedicalSpecialization
    menu_label = 'Medical Specialization'
    menu_icon = 'user'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name')

class CityAdmin(ModelAdmin):
    model = City
    menu_label = 'City'
    menu_icon = 'user'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name')

class DoctorAdmin(ModelAdmin):
    model = Doctor
    menu_label = 'Doctor'
    menu_icon = 'user'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('first_name', 'surname', 'specializations_list')
    list_filter = ('surname',)
    search_fields = ('surname')

class SurgeryAdmin(ModelAdmin):
    model = Surgery
    menu_label = 'Surgery'
    menu_icon = 'user'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('surgery_name', 'address', 'city', 'doctors_list')
    list_filter = ('surgery_name',)
    search_fields = ('surgery_name', 'address', 'city')
```

54. Create a GROUP for all OBJECTADMINS created above 

Now we can create a ModelAdminGroup where we group the objects created above into one directory in the admin.

Add this to the bottom of 'surgeries/wagtail_hooks.py'.

```
class SurgeryGroup(ModelAdminGroup):
    menu_label = 'Manage Surgeries'
    menu_icon = 'folder-open-inverse'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (MedicalSpecializationAdmin, CityAdmin, DoctorAdmin, SurgeryAdmin)

modeladmin_register(SurgeryGroup)
```

This will show the group in the admin menu, when we click it, all of the models in the group appear in a sub menu.

NOTE!! - You can register single objects in the admin (not neccesarily in a group):

`modeladmin_register(DoctorAdmin)`

=================================================

INTEGRATING DJANGO MODELS INTO THE WAGTAIL 'PAGE' ECOSYSTEM

You can use URLs and Views as you would normally with Django, but if you are using Wagtail, you can create 'Wagtail Pages'.

Wagtail pages are hierarchical.  You can create a template, and then create a page instance of that template as a child page of any other page. 

Here, we are going to create a surgery index page, with all surgeries returned in the pages context variable.

Then, we will create a page instance of our surgery index page as a child page of 'Home'.

55. **Add necessary Page, RichTextField and FieldPanel wagtail imports**

In 'projectfolder/mysite/surgeries/models.py', add these imports at the top.

```
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
```

56. **Create a 'SurgeryIndexPage' class that inherits from Page**

We create a 'page' class and then return a context variable containing a list of our surgery models.

In 'surgeries/models.py'

```
class SurgeryIndexPage(Page):
    intro = RichTextField(blank=True, help_text='Write a short intro to the surgery index page')

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request):
        context = super().get_context(request)
        
        surgeries = Surgery.objects.all()
        context['surgeries'] = surgeries
        return context
```

56. **Create a template folder and template**

Set up your structure and add your template like this so that Django's templating lookup will find your template:

```
surgeries/
  templates/
    surgeries/
      surgery_index_page.html
```

NOTE!: The naming convention is crucial when working with Wagtail. The template name must match the name of the Class in our models page as shown above.

57. **Loop through all surgeries in the surgery index page.**

```
{% block content %}

<div class="container">
{% if surgeries %}
  {% for surgery in surgeries %}
    <h2>{{ surgery.surgery_name }}</h2>
    <h4>ADDRESS:</h4>
    <p>{{ surgery.address}}</p>
    <p>{{ surgery.city }}</p>
    <h4>DOCTORS:</h4>
    <ul>
      {% for doctor in surgery.doctors.all %}
        <li><strong>{{ doctor.first_name }} {{ doctor.surname}}</strong></li>
        {% for specialization in doctor.specializations.all %}
          <p>{{ specialization.name }}</p>
        {% endfor %}
      {% endfor %}
    </ul>
  {% endfor %}
{% endif %}
</div>

{% endblock content %}
```

58. **Create a 'child page' of 'Surgery Index Page' type**

a) In the wagtail admin menu, click 'Pages'. (In some versions of Wagtail, this could be called 'Explorer')

b) Click on the 'Home' folder.

c) Click on 'Add child page'

d) Click on 'Surgery Index page'

e) Give your page a name and write an intro.

In this case, your new template will appear as the page title you gave the page, eg. url/surgeries

Wagtail is hierarchical so you could create a subfolder of 'Home' called doctors and then create and add a doctors search page type giving this url:

`eg. url/doctors/search-doctors`

You could also retrieve 'counts' from the database and add that to any page template you create eg. 6 doctors, 7 medical specializations etc. and display this data on your homepage for example.



