import requests

from flask import redirect, render_template, session
from functools import wraps
from datetime import date, datetime

DATE_FORMAT = "%Y-%m-%d"
DATE_LENGTH = len(date.today().strftime(DATE_FORMAT))
class Helper:

    @staticmethod
    def login_required(f):
        """
        Decorate routes to require login.

        https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
        """

        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get("user_id") is None:
                return redirect("/login")
            return f(*args, **kwargs)

        return decorated_function

    @staticmethod
    def from_string(value):
        """ Convert an ORM ``value`` into a :class:`date` value. """
        if not value:
            return None
        value = value[:DATE_LENGTH]
        return datetime.strptime(value, DATE_FORMAT).date()
    
    @staticmethod
    def get_age_by_birthdate(birthdate):
        """Return Age."""
        if not birthdate:
            return 0
        today = date.today()
        try:
            return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        except:
            return 0
