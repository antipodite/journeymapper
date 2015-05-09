"...Of this disgrace it may be easily supposed that he was much ashamed, and shame had its proper effect in producing reformation. He resolved from that time to study eight hours a day, and continued his industry for seven years, with what improvement is sufficiently known. This part of his story well deserves to be remembered; it may afford useful admonition and powerful encouragement to men whose abilities have been made for a time useless by their passions or pleasures, and who having lost one part of life in idleness, are tempted to throw away the remainder in despair. """

copypasta of my notes:

1. Create a virtual environment:

    mkvirtualenv projectdir
    cat "cd $PROJECT_HOME/projectdir" >> $VIRTUAL_ENV/bin/postactivate

2. Install Flask and Gunicorn:

    pip install flask gunicorn

3. Write pip requirements file:

    pip freeze > requirements.txt

4. Create a new git repo and gitignore:

    git init
    cp ~/Projects/gitignore-python ./.gitignore

5. Create Heroku Procfile:

    echo "web: gunicorn app:app" > Procfile

6. Create an app.py with a hello world thingy

7. Commit changes to git:

    git add Procfile app.py requirements.txt

8. Create a Heroku app and push files to it, then check it works:

    heroku create $appname
    git push heroku master
    heroku open

9. Create a todo list to keep me focussed and attempt to overcome the bed of
procrastes:

    vim todo.list
    git add todo.list

10. Create a config.py with settings for development and production, e.g.:

   class Config(object):
        DEBUG = False
        SECRET_KEY = "changeme"

    class DevConfig(Config):
        DEBUG = True

    class ProductionConfig(Config):
        pass

11. Set up config envvar:

    cat "export APP_SETTINGS=\"config.DevConfig\"" >> $VIRTUAL_ENV/bin/
    postactivate

Would need to run this each time I switched into the app folder to work on
the app. Now I can use Flask's config.from_object with the environment
variable to choose either development or production settings.

12. Set the same environment variable to point to the production settings on
Heroku:

    heroku config:set APP_SETTINGS=config.ProductionConfig

13. Install PostgreSQL and SQLAlchemy

    pip install Flask-Migrate Flask-SQLAlchemy psycopg2
    pip freeze > requirements.txt

If Postgres is not installed:

    brew install PostgreSQL

14. Create a local development database:

    $ psql
    create database appname_dev

15. Update dev config to point to database URI and load into app:

    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    export DATABASE_URL="postgresql://localhost/dbname" - to postactivate

This way don't need to change configuration for the URI of the database
when pushing to Heroku, everything will just work.

16. Create some database models, then import them into the app:

    fixme

17. Create a management script for database migrations:

    fixme

18. Initialise Alembic so I can run migrations:

    python manage.py db init

19. Generate a migration, and then apply it:

    python manage.py db migrate
    python manage.py db upgrade