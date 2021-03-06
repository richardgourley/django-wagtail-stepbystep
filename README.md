# Django and Wagtail step by step

A step by step reference guide with all of the steps and command line prompts required for setting up a wagtail site with the following:

- Customizing the wagtail admin with a custom logo, custom welcome message and custom login page message.

- A virtual environment.
- Setting up python-decouple in order to avoid having secret keys and database passwords displayed in your settings files when using Github.

- Working with Django models
- Adding django models to the admin page
- Adding a root admin menu for a group of django models - eg. a folder named 'Properties' with models inside such as 'Commercial, Residential' etc.

- Setting up a MySQL database (can be left as SQLlite or adapted to Postgres as required) using InnoDB tables instead of ISAM tables.
- Setting up Bootstrap scss variables using django compress and django sass
- Setting up Vue.js if you only require it on some pages, rather than creating a full SPA.

- Creating a menu of existing pages marked 'show in menu'

- Setting up image fields for a home page hero image.
- Using wagtail images and the django 'as' template tag to display image fields as a background.
- Looping context variables in the home page.

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

You should currently be in 'projectfolder'.  Navigate to 'projectfolder/mysite' - in this directory you should see the 'manage.py' file and the 'home' and 'search' app directories.

`cd mysite`

9. **Wagtail automatically adds a requirements.txt file. Just locate this file and take a look at it. The use of a requirements.txt file is explained more in the'PIP LIST, PIP FREEZE AND REQUIREMENTS.TXT section.**

10. **Install python decouple**

Python decouple allows you to keep all sensitive project information in 1 file that you can ask github to ignore (ie. never display sensitive information in a repository).

`pip install python-decouple`

11. **Install mysqlclient**

This connects our wagtail project to a MySQL database.
(Instead, you can use sqllite which comes automatically with Django, no changes required, or you can set up any other SQL database, such as Postgres)

`pip install mysqlclient`

12. **OPTIONAL - Check dependencies are installed**

To check the above have installed and to see all other packages installed in our virtual environment, along with their version numbers, enter this:

`pip list`

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

NOTE!!! It's highly recommended to create and run tests on your projects.

If you run tests later, you will also need to grant priveliges for the testing database. 

Tests aren't covered in this step by step guide but the Django documentation and the Mozilla Django tutorial cover testing in detail.

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

NOTE!! The db host and port number might be different on your machine.

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

NOTE!!: Above we set 'INNNODB' instead of 'MYISAM' in the 'OPTIONS' key.

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

**SETTING UP BOOTSTRAP .SCSS FILES**

You need to install 2 dependencies to get bootstrap up and running with .scss variables that make changing basic bootstrap settings much easier and more managable.

21. **Install django_compressor and django-libsass**

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

26. **Open up the scss directory in your Bootstrap download**

NOTE! For demonstration purposes, I haven't included all files from the 'scss' directory.  

I have ommited the 'utilities', 'mixins' and 'vendor' directories from the 'scss' directory.
You may require these in your project.

27. **Create folders inside 'mysite/static' to add bootstrap files**

Create directories inside the 'css' directory of 'projectname/mysite/mysite/static' as follows:

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
          mysite.js
```

28. **Inside the 'css/bootstrap/scss' directory copy over the scss files from your bootstrap download.**

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
          mysite.js
        theme.scss
```

30. **Open up the 'theme.scss' created above and modify a few bootstrap variables to test and import the bootstrap.scss variables**

```
$primary: purple;
$secondary: orange;

@import 'css/bootstrap/scss/bootstrap.scss';
```

=================================================

**'PIP LIST', 'PIP FREEZE' AND 'REQUIREMENTS.TXT'**

- A few notes about why you should use a 'requirements.txt' file.

At this stage we have installed all of the packages we will require.

You can enter 'pip list' which will display every package and its' version.

```
pip list
```

## Development vs. Production

It's useful to create a 'requirements.txt.' file during development which contains all of the packages and versions you have because when you deploy your project (in production) you can simply run one command:

```
pip install requirements.txt
```

The above command will make sure that the versions of the packages you have installed up to now in your development virtual environment are exactly the same versions as when you deploy your project to the cloud - AWS, heroku, PythonAnywhere etc.

That saves time AND saves you problems if you are using different versions of software which can cause your lovely development app to behave differently in production.

## Pip Freeze and requirements.txt

Wagtail already comes with a 'requirements.txt' file.  IF it doesn't exist (as in a normal Django project), navigate to the same directory as 'manage.py' and create a 'requirements.txt' file

```
touch requirements.txt
```

Now we can use pip freeze to create a requirements file conataining all packages and version ready to install in production:

```
pip freeze > requirements.txt
```

=================================================

**BASE.HTML**

In django and wagtail projects, the base.html file is the html page that calls content from other templates inside {% block content%} and is used as the base of every page.

It contains headers, and you can include a navbar, footer and a sidebar if required.

31. **Check that wagtail automatically created and added a general site css and js file**

You should see this in the base.html file located at 'projectfolder/mysite/mysite/templates':

```
...
{# Global stylesheets #}
<link rel="stylesheet" type="text/css" href="{% static 'css/mysite.css' %}">

.....

{# Global javascript #}
<script type="text/javascript" src="{% static 'js/mysite.js' %}"></script>

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

33. **Load Bootstrap JS files**

You could use the downloaded Bootstrap Javascript files (as we did with the SCSS files) but you can also use a CDN as shown below.

In this guide, we are only using a little Bootstrap JS for the navbar and we don't need to modify any other JS files so we'll add the Bootstrap JS via a CDN:

In 'base.html', under {# Global javascript #}

```
{# Bootstrap javascript #}
<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ho+j7jyWK8fNQe+A12Hb8AhRq26LrZ/JpcUGGOn+Y7RsweNrtN/tE3MoK7ZeZDyx" crossorigin="anonymous"></script>
```

=================================================

**VUE JS**

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

**HOME / HOME PAGE**

35. **Remove links to welcome page from home page**

In 'projectfolder/mysite/home/templates/home/home_page.html' you can delete the default welcome page css link and 'include' welcome page, and all comments..

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

**CUSTOMIZE THE WAGTAIL ADMIN DASHBOARD**

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

**DJANGO MODELS -**
**MODEL ADMIN** allows you to add django models to the admin page.

You can use normal django fields AND wagtail fields on your models. 

Wagtail has many fields that you can use in a CMS such as 'RichTextField'. It is similar to the Wordpress text editor.

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


NOTE: Extra methods (doctors_list in 'Surgery' and specializations_list in 'Doctor') created to display the ManyToMany and ForeignKey fields in the admin dashboard list_display.


```
from django.db import models
from wagtail.core.fields import RichTextField

# Create your models here.
class MedicalSpecialization(models.Model):
    name = models.CharField(max_length=255)
    description = RichTextField(help_text='Add a short description about the specialization. (It will be displayed on the home page.) ')

    def __str__(self):
        return self.name

class City(models.Model):
    class Meta:
        verbose_name = 'city'
        verbose_name_plural = 'cities'
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Surgery(models.Model):
    class Meta:
        verbose_name = 'surgery'
        verbose_name_plural = 'surgeries'
    surgery_name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.surgery_name
    
    def doctors_list(self):
        return ', '.join(f'{doctor.first_name} {doctor.surname}' for doctor in self.doctor_set.all())

class Doctor(models.Model):
    first_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    specializations = models.ManyToManyField(MedicalSpecialization, help_text='Select 1 or more specializations. Hold CTRL to click on more than 1.')
    bio = RichTextField(help_text='Add a very short bio.')
    surgery = models.ForeignKey(Surgery, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.surname

    def specializations_list(self):
        return ', '.join(specialization.name for specialization in self.specializations.all())

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
    menu_label = 'Medical Specializations'
    menu_icon = 'user'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name')

class CityAdmin(ModelAdmin):
    model = City
    menu_label = 'Cites'
    menu_icon = 'user'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name')

class DoctorAdmin(ModelAdmin):
    model = Doctor
    menu_label = 'Doctors'
    menu_icon = 'user'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('first_name', 'surname', 'specializations_list', 'surgery')
    list_filter = ('surname',)
    search_fields = ('surname')

class SurgeryAdmin(ModelAdmin):
    model = Surgery
    menu_label = 'Surgeries'
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

**INTEGRATING DJANGO MODELS INTO THE WAGTAIL 'PAGE' ECOSYSTEM**

You can use URLs and Views as you would normally with Django, but if you are using Wagtail, you can create 'Wagtail Pages'.

Wagtail pages are hierarchical.  You can create a template and as a page instance as a child page of any other page eg.Home. 

Here, we are going to create a surgery index page and a template, with all surgeries returned in the pages context variable.

Then, we will create a page instance of our surgery index page as a child page of 'Home'.

55. **Add necessary Page and FieldPanel wagtail imports**

In 'projectfolder/mysite/surgeries/models.py', add these imports at the top.

```
from wagtail.core.models import Page
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
{% if surgeries %}
<div class="container my-4">
  <div class="row">
    {% for surgery in surgeries %}
    <div class="col-sm-6 p-3">
      <div class="card h-100 shadow p-3">
        <div class="card-body">
          <h2 class="text-primary card-title">{{ surgery.surgery_name }}</h2>
          <h3 class="text-secondary lead">ADDRESS:</h3>
          <br>
          <p class="card-text">{{ surgery.address }}</p>
          <p class="card-text">{{ surgery.city }}</p>
          <div class="card-body">
            <h3 class="text-secondary lead">DOCTORS:</h3>
            <ul>
            {% for doctor in surgery.doctor_set.all %}
              <li><strong>{{ doctor.first_name }} {{ doctor.surname}}</strong></li>
              {% for specialization in doctor.specializations.all %}
                <p>{{ specialization.name }}</p>
              {% endfor %}
            {% endfor %}
            </ul>
          </div>
        </div>
      </div>
    </div>
    {% endfor %}
  </div>
</div>
{% endif %}

{% endblock content %}
```

58. **Create a 'child page' of 'Surgery Index Page' type**

a) In the wagtail admin menu, click 'Pages'. (In some versions of Wagtail, this could be called 'Explorer')

b) Click on the 'Home' folder.

c) Click on 'Add child page'

d) Click on 'Surgery Index page'

e) Give your page a name and write an intro.

In this case, your new template will appear as the page title you gave the page, eg. url/surgeries

Wagtail is hierarchical so you could create a subpage of 'Home' called doctors and then create a subpage of doctors called 'search doctors' which would give you this url:

`eg. url/doctors/search-doctors`

=================================================

**CREATING A MENU OF WAGTAIL PAGES DYNAMICALLY**

You can create your own template tags in django and wagtail to retrieve pages and display them with a link in a navigation menu.

When you create a page in Wagtail, you have the option to show a page in menus or not.

59. **Set our surgeries page to be shown in menus**

In the admin menu, select 'Pages/Home' and click edit on our 'Surgeries' page.

On the tab 'Promote', select true for the option 'Show in Menus'.

60. **Create a templatetags folder**

Template tags must be created in an app that is registered in 'INSTALLED_APPS' in our settings file.  It seems more logical to use our 'home' app rather than 'surgeries' so create a template tags directory inside with a structure like this:

```
projectfolder/
  mysite/
    home/
      static/
      templates/
      templatetags/
```

61. **Create an '__init__.py' file**

In the 'templatetags' directory, create a new blank file called '__init__.py'.
We need to do this so Django will know it is a module and will read the python files inside this directory.

62. **Create a templatetags file called 'pages_menu.py'**

In the 'templatetags' directory create a file called 'pages_menu.py'.

We register the template tag, then with an inclusion tag, instruct django to pass the returned results from the function to 'home/templates/tags/pages_menu.html'.

In the function, we first get the site root page (our home page) and then we get all child pages of our home page which are live and marked as 'show in menu'.

```
from django import template
from wagtail.core.models import Site

register = template.Library()

@register.inclusion_tag("tags/pages_menu.html")
def get_pages_menu():
  site = Site.objects.get(is_default_site=True)
  home_page = site.root_page
  pages = home_page.get_children().live().in_menu()
  return {
      "home_page":home_page,
      "pages":pages,
  }
```

63.  **Create a 'tag' directory**

Within the 'home' app, open up 'templates' and create a directory called 'tags'.

```
projectfolder/
  mysite/
    home/
      static/
      templates/
        home/
        tags/
      templatetags
```

64. **Create a 'pages_menu.html' file inside the 'tags' directory**

Inside 'home/templates/tags', create this 'pages_menu.html' file which will be passed the 'home_page' and 'pages' variables from our template tag.  You can see how you can loop the pages in our pages menu:

```
{% load wagtailcore_tags static %}

<header>
  <div class="container-fluid outer-nav">
    <div class="container">
      <nav class="navbar navbar-expand-md navbar-light">
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav mr-auto ml-auto">
            <li class="nav-item active">
              <a class="nav-link text-primary" href="{% pageurl home_page %}">Home <span class="sr-only">(current)</span></a>
            </li>
            {% for page in pages %}
            <li class="nav-item">
              <a class="nav-link text-primary" href="{% pageurl page %}">{{ page.title }}</a>
            </li>
            {% endfor %}
          </ul>
        </div>
      </nav>
    </div>
  </div>
</header>
```

We have added an 'outer-nav' class above allowing us to add some css styling to our bootstrap navbar.

In our main css file located at 'mysite/mysite/static/css/mysite.css' and add some styling for our 'pages_menu.html' file created above:

```
.outer-nav {
  box-shadow: 0px 0 11px 0 rgba(0, 0, 0, 0.1);
}

.nav-link {
    font-weight: bold;
}
```

65. **In 'base.html', load the template tag, and call the function**

Open up our 'base.html' file located in 'projectfolder/mysite/mysite/templates'.

Load the tag at the top and then call the function (get_pages_menu) located in 'pages_menu.py' like this:

```
<--- Load the pages_menu tag --->
{% load pages_menu %}

...
<body class="{% block body_class %}{% endblock %}">
        {% wagtailuserbar %}

        <!-- Display pages menu before content --->
        {% get_pages_menu %}

        {% block content %}{% endblock %}
```

=================================================

**CREATING A HOME PAGE -**
CREATING TEXT AND IMAGE FIELDS AND PASSING MODEL INSTANCES

Under our menu, on the home page, we will create a demo hero image with intro text, and then display our 'specializations' and 'doctors' instances.

66. **Create 'intro' and 'main_image' fields**

In the 'home' app, open 'models.py'.  We are first importing 'ImageChooserPanel' and then creating a simple 'intro' field, and a 'main_image' field which will be displayed as a hero image:

NOTE! In wagtail, images are saved as a foreign key and then related to this page.

```
from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel


class HomePage(Page):
    intro = models.CharField(blank=False, null=True, max_length=255)
    main_image = models.ForeignKey(
      'wagtailimages.Image',
       null=True,
         on_delete=models.SET_NULL, 
         related_name="+", 
         help_text='This image will appear in a full width image behind your intro text.'
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        ImageChooserPanel('main_image')
    ]
```

67. **Import models from surgeries and add to context variable**

Here, we are importing 'Doctor' and 'MedicalSpecialization' from our 'surgeries' app.  Then, we query those models and pass them to the context variable of our home page for displaying in the template.

```
...
from surgeries.models import MedicalSpecialization, Doctor
...

class HomePage(Page):
    intro = models.CharField(blank=False, null=True, max_length=255)
    main_image = models.ForeignKey(
      'wagtailimages.Image',
       null=True, 
       blank=True, 
         on_delete=models.SET_NULL, 
         related_name="+", 
         help_text='This image will appear in a full width image behind your intro text.'
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        ImageChooserPanel('main_image')
    ]

    def get_context(self, request):
        context = super().get_context(request)
        
        medical_specializations = MedicalSpecialization.objects.all()
        doctors = Doctor.objects.all()
        context['medical_specializations'] = medical_specializations
        context['doctors'] = doctors
        return context
```

68. **Update the database with our new 'home/models.py' changes**

```
python manage.py makemigrations
```

```
python manage.py migrate
```

69. **Add 'wagtailimages_tags'**

In order to access our home page 'main_image', load 'wagtailimages_tags' by adding this below the 'load static' line in 'home/templates/home/home_page.html':

```
{% extends "base.html" %}
{% load static %}

{% load wagtailcore_tags wagtailimages_tags %}
```

70. **Give the image an alias using 'as'**

Wagtail has a really useful way of displaying image fields.  

Normally, we can display a wagtail image field with the dimensions we require, like this: 

```
{% image page.main_image fill-320x240 %}
```

In this case, we are going to use our wagtail image as a background, so we have to use the Django 'as' alias. So just below {% block content %} add:

```
<!-- Set the main image (original size) for this page as an accessible 'tmp_image' -->
{% image page.main_image original as tmp_image %}
```

71. **Add a css file, create a hero image and loop our context variable objects**

Create a css file to add some styling to our home page.

Inside your 'home' app add a 'home.css' file inside a static folder like this:

```
home/
  static/
    home/
      css/ 
        home.css
```

Add to 'home.css' these styling classes for the hero and section areas:

```
.section{
  padding-top: 50px;
  padding-bottom: 25px;
  border-bottom: 1px solid #f2f2f2;
}

.hero {
  padding: 90px;
  background-size: cover;
  background-position: center;
}

@media (max-width: 800px) {
  .hero {
    padding: 60px;
  }
}

@media (max-width: 460px) {
  .hero {
    padding: 25px;
  }
}
```

Now in 'home/templates/home/home_page.html' add a hero image, and then divs for looping and displaying our doctors and medical specializations.

NOTE: Rich text fields are displayed differently:

```
{% block content %}

<!-- Set the main image (original size) for this page as an accessible 'tmp_image' -->
{% image page.main_image original as tmp_image %}

<!--- Hero Image --->
<div class="hero container-fluid bg-r" 
style="background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.3)), url({{ tmp_image.url }});">
  <div class="container">
    <div class="row justify-content-start">
      <div class="col-12 col-sm-10 col-md-8 text-center text-sm-left">
        <h1 class="text-white">{{ page.intro }}</h1>
        <p class="lead text-white">Get your appointment booked with us today!</p>
        <p class="mt-4">
          <a class="border border-white btn btn-secondary mr-4 mt-2" href="">Find a surgery</a>
          <a class="border border-white btn btn-primary mr-4 mt-2" href="">Meet our doctors</a>
        </p>
      </div>
    </div>
  </div>
</div>


<!--- Specializations --->
<div class="section">
  <div class="container text-center">
    <h1>Our Specializations</h1>
      <div class="row">
        {% for medical_specialization in medical_specializations %}
          <div class="col-sm-10 col-md-6 col-lg-4 py-3">
            <h4>{{ medical_specialization.name }}</h4>
            {{ medical_specialization.description|richtext }}
          </div>
        {% endfor %}
      </div>
  </div>
</div>

<!--- Doctors --->
<div class="section">
  <div class="container text-center">
    <h1>Our Doctors</h1>
      <div class="row">
        {% for doctor in doctors %}
          <div class="col-sm-10 col-md-6 col-lg-4 py-3">
            <h4>{{ doctor }}</h4>
            <a href="{% url 'surgeries:doctor_detail' doctor.slug %}">
              <p class="text-primary"><strong>Learn more >></strong></p>
            </a>
            {{ doctor.bio|richtext }}
          </div>
        {% endfor %}
      </div>
  </div>
</div>

{% endblock content %}
```

=================================================

**DJANGO VIEWS - HOW TO USE THEM ALONGSIDE WAGTAIL**

Django models and views (such as generic detail view, list view etc.) work exactly the same alongside Wagtail, so a url such as 'surgeries/doctors/james-blakely' can be created directly from your 'Doctor' instances, without needing to create a wagtail page.

This is important if you are adding Wagtail to an existing Django site, or you wish to use Wagtail for some parts of your site, but prefer to use the traditional Django models, urls, views and templates for other parts.

To test this, here we are going to create a 'view' for each of our doctors displaying information from the 'Doctor' model fields.

71. **Add a 'slug' field to the Doctor model**

Inside 'surgeries/models.py', we need to add a slug field.  This field will be used to display in urls.  (We could use the 'id' but it's better for site security and readability to use slugs in urls).

```
class Doctor(models.Model):
    first_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    specializations = models.ManyToManyField(MedicalSpecialization, help_text='Select 1 or more specializations. Hold CTRL to click on more than 1.')
    bio = RichTextField(help_text='Add a very short bio.')
    surgery = models.ForeignKey(Surgery, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(max_length=150, unique=True, help_text='This field will appear in the url eg doctors/dave-simpson')

    def __str__(self):
        return self.first_name + ' ' + self.surname

    def specializations_list(self):
        return ', '.join(specialization.name for specialization in self.specializations.all())
```

NOTE!  If you have already created instances of the 'Doctor' model, you will need to set the slug field to null=True, then create slugs for each doctor, then remove null=True after each instance has a slug field set.

72. **Create a 'DoctorDetailView' class in the views file.**

In the 'surgeries/views.py' file, here we create a class that inherits from 'generic.DetailView'.  This easily allows us to display each doctor individually.

```
from django.shortcuts import render
from django.views import generic
from .models import Doctor

# Create your views here.
class DoctorDetailView(generic.DetailView):
  model = Doctor
  template_name = 'surgeries/doctor_detail.html'

  def get_queryset(self):
    return Doctor.objects.all()
```

73. **Create a 'urls.py' folder inside 'surgeries'**

Directly inside our surgeries app directory, create a file called 'urls.py'.  Here we are going to add this url pattern linked to our 'DoctorDetailView':

```
from django.urls import path
from . import views

app_name = 'surgeries'

urlpatterns = [
    path('doctor/<slug:slug>', views.DoctorDetailView.as_view(), name="doctor_detail"),
]
```

74. **Now create a template to use for each Doctor instance.***

In 'surgeries/templates/surgeries' create a new file called 'doctor_detail.html':

```
{% extends "base.html" %}
{% load static %}

<!-- Loads wagtail template tags -->
{% load wagtailcore_tags %}

{% block body_class %}surgery-index-page{% endblock %}

{% block extra_css %}
{% endblock extra_css %}

{% block content %}

{% if doctor %}
<div class="container py-4">
  <h2>{{ doctor }}</h2>
  <p class="lead">{{ doctor.bio|richtext }}</p>
  <hr>
  <h3>Specialization:</h3>
  <ul>
  {% for specialization in doctor.specializations.all %}
     <li>{{ specialization.name }}</li>
  {% endfor %}
  </ul>
  <h3>Surgery:</h3>
  <h4>{{ doctor.surgery }}</h4>
  <p>{{ doctor.surgery.address }}</p>
</div>

{% endif %}

{% endblock content %}
```

75. **Register our 'surgeries/urls.py' globally in the 'mysite/urls.py' file**

In order for Django to recognize the url patterns you have created in an app, we need to add them to the global url file. Open 'projectfolder/mysite/mysite/urls.py' and add in our surgeries urls like this:

```
# Make sure 'include is imported'...
from django.urls import include, path
...

urlpatterns = [
    path('django-admin/', admin.site.urls),

    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),

    path('search/', search_views.search, name='search'),

    path('surgeries/', include('surgeries.urls')),

]
```

76. **Add a link for each doctor on our home page**

We already loop through each doctor and display basic info on the home page. We can now also add a url link for each doctor taking the visitor to a page such as 'mysite/surgeries/doctors/james-blakely'.

In 'home/templates/home/home_page.html' add a link to our doctors loop like this:

```
<div class="container py-5 text-center">
  <h1>Our Doctors</h1>
    <div class="row">
      {% for doctor in doctors %}
        <div class="col-sm-10 col-md-6 col-lg-4 py-3">
          <h4>{{ doctor }}</h4>
          <a href="{% url 'surgeries:doctor_detail' doctor.slug %}" >
            Learn more >>
          </a>
          {{ doctor.bio|richtext }}
        </div>
      {% endfor %}
    </div>
</div>
```

If you create 2 or 3 doctors with a slug field added, you should be able to see all of your doctors listed on the home page with a link for each doctor that takes you to 'site/surgeries/doctors/slug'.

NOTE: This is just an example.

We could take our doctor model further and it might make more sense to have a short_bio field for the home page and a long_bio field for the individual doctors page.

We would probably add an image field to display an image of the doctor.

For our 'Surgery' model, we could add more fields such as a transport directions field, and an image gallery (this can be created fairly easily - see the wagtail first site documentation).

You could also make use of Wagtail by adding a blog and some other pages such as an 'About' page, 'contact' page.  This could then be combined with the power of Django's user system, where a patient, doctor log in system could be created.

Hope this helps in getting Wagtail up and running and shows how it works very nicely alongside Django!











