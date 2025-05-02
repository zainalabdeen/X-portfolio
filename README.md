# X-Portfolio
#### Video Demo:  https://youtu.be/HHEyefmf4yY
#### Description:
X-Porfolio is Web application that connecting between the skilled people and the people search for skilled person and allow them to contact. it's helping the skilled people to create and publish their portfolio with full of their informations. and facilitate the people looking for skilled person by searche and view the registered portfolios and contact them.skilled people need to create account and they can add their Portfolio Informations.

## Table of Contents
- [Portfolio Information](#Portfolio-Information)
- [Getting Started](#getting-started)
- [How to Use](#how-to-use)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)


## Portfolio Information
1️⃣ Professional Titles\
2️⃣ Basic info and About you\
3️⃣ Skills\
4️⃣ Education And Certifications 🏆\
5️⃣ Professional Experience\
6️⃣ Number of Years Of Experience , Clients and Projects\
7️⃣ Interests\
8️⃣ Social Profile Links (Twitter,Facebook,Instagram,Linkedin) \
9️⃣ Contact me

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

You'll need :
- [Git](https://git-scm.com)
- [python](https://www.python.org/downloads/)
- [FLASK](https://flask.palletsprojects.com/en/stable/installation/)
- [Flask-SQLAlchemy](https://pypi.org/project/Flask-SQLAlchemy/)
- [SQLite](https://www.sqlite.org/download.html)

## How To Use

### 1- From your command line, clone the Project:

```bash
# Clone this repository
git clone -b project git@github.com:me50/Bin9383.git

# Go into the repository
cd project/portfolio

# Setup default environment variables

# For Linux
export FLASK_APP=portfolio.py
# For Windows
SET FLASK_APP=portfolio.py

# opens an interactive Python session to create the database and tables from models
flask shell
```
### 2- In the interactive session execute below Python commands to create the db

```python
# import the db <SQLAlchemy engine>
from app import db
# import the models
from app.models import Users,Skills,Titles,Interests,Educations,Experiences,Contacts
# create the db and tables
db.create_all()
```

### 3- Run tha application
```bash
flask run
```


## Technologies Used
### Front-End
- [Jinja](https://jinja.palletsprojects.com/en/stable/)
- [BootstrapMade Personal Template](https://bootstrapmade.com/personal-free-resume-bootstrap-template/)
### Back-End
- [FLASK](https://flask.palletsprojects.com/en/latest/)
### DataBase
- [SQLite](https://www.sqlite.org/)

## Project Structure
### app folder contains :
    - Static(contains required assets library css and js)
    - Templates(contains the frontend jinja template)
    - Models file(contains the models and their fields that will be created as database tables)
    - Route file (contains the url routes with user authentication)

### config file contains :
    contains environment, session and database configuration.
### instance folder :
    contains the created database file
### flask session folder
    contains the user stored session
