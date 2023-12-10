import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SESSION_TYPE = 'filesystem'
    RESULTS_PER_PAGE = 5
    debug = True
    TEMPLATES_AUTO_RELOAD = True
    SECRET_KEY = 'SECRET_KEY'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
        or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False