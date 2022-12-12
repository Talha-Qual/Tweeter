# TweeterGetting Started:
  Please create a virtaul env and activate it:
    Windows:
      python3 -m venv venv
      venv/scripts/activate
    MacOS:
      python3 -m venv venv
      source venv/bin/activate
  Please download and install the requirements.txt
    pip install -r requirements.txt
  Please do migrations:
    python manage.py makemigrations network
    python manage.py migrate network
  For seeding data, please run the following command:
    python manage.py runscript loaddata
  Note: The way this script is set up, please only run it once, or you will get duplicate data into the database

For logging in and registring:
It's important to login and register through the website because it will get all of the necessary credentials. If you create an account using the django admin and create a superuser, you will have to make sure that you fill out all of the fields or else you won't be able to see some of the content.

For profile stuff:
I wanted to create a 'twitter handle' that people could use to tag other users but I wasn't able to. That's why you will the see your handle in some places, but you won't be able to use it.

Also, I wanted users to be able to edit their profile, add images, but I ran out time for both.

