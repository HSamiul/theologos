
# Theologos

Theologos is a web app for both viewing other people's commentary on the Bible and sharing your own, built with [Django](https://www.djangoproject.com/).

## Setup

### Install Python
The project uses **Python version 3.11.2**. To install this version of Python: 

1. Visit https://www.python.org/downloads/release/python-3112/
2. Scroll to the bottom of the page and download the appropriate installer for your machine. 
> For example, if you are on a MacBook, you would download the installer labeled "macOS 64-bit universal2 installer"
3. Run the installer
> You can confirm that Python is installed by opening your terminal and running `where python` or `where python3`.

### Install PostgreSQL
The project uses **PostgreSQL version 15.2**. You will install a Postgres.app, a tool that includes both PostgreSQL and a GUI that makes using PostgreSQL easier to use. To install Postgres.app, follow the instructions on their website: https://postgresapp.com/.

> You can confirm that PostgreSQL is installed by opening your terminal and running `where psql`.

> Python and PostgreSQL are the backbone on which the project will run. Now you will set up the project itself.

### Install the project
To download the project from this repository, you should use the latest version of Git. To install Git, follow the instructions on their website: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

Once you have Git, to install the project:
1. Open a terminal
2. Navigate to a directory that you want the project to be in
> I (developer) like to place the project in my `Desktop` directory. However, it really doesn't matter where you place the project. Just remember where you put it!
3. Run the command: `git clone https://github.com/HSamiul/theologos.git`

### Set up the Python virtual environment
You will use a virtual environment (venv) to store the necessary Python dependencies in. This way, when you are running the project within the venv, you are guaranteed to have all the necessary dependencies for the project to work.

1. Open a terminal
2. Run this command to create a new venv:  `python3 -m venv ~/.virtualenvs/djangodev`
3. Run this command to activate the venv: `source ~/.virtualenvs/djangodev/bin/activate`
4. Navigate to the project directory
> After navigating to the project directory, your terminal prompt should look something like `$~/.../theologos`
6. Run this command to install the required packages for this project: `python -m pip install -r requirements.txt`

### Set up the PostgreSQL database

Before we can run the project, we need to set up a database for the project to both draw data from and push data to. Our project is configured to use a PostgreSQL database. You will set up that database now:

#### Create the database admin
1. Open a terminal 
2. Run this command to open the PostgreSQL shell: `psql`
> If you are prompted to enter a role and database name, run the command: `psql postgres -U postgres`.
3.   Run this command to create a new user: `CREATE USER admin WITH PASSWORD 'theologos373' CREATEDB;`
> Why do we need to do this? Because the project is configured to expect an admin user with that specific password and with the privilege to create a database. See the `settings.py` file within the project directory if you want proof!
4. You can confirm that the user was created by running this command: `\du`

#### Create the database
1. Open a terminal
2. Run this command to open the PostgreSQL shell: `psql postgres -U admin`
3. Run this command to create the database: `CREATE DATABASE theologos_db;`
> Why does the database need to be named `theologos_db`? Because the project is configured to look for and use a database with that name. See the `settings.py` file within the project directory if you want proof!

We're almost there. We just need to set up the Django project itself now.

### Set up the Django project
You need to do some initial setup to run the project for the first time. This initial setup is mostly just setting up the database with a few commands:

1. Open a terminal
2. Navigate to the project directory
3. Run this command to activate the venv: `source ~/.virtualenvs/djangodev/bin/activate`

Run the following commands to set up the project:

1. `python manage.py makemigrations`
2. `python manage.py migrate`
3. `python manage.py loaddata books`
4. `python manage.py loaddata chapters`
5. `python manage.py loaddata verses`

### Run the project
Run the project with this command: `python manage.py runserver`. 

You can then open the project with the link outputted to your terminal. It will look something like `http://localhost:8000/`.
