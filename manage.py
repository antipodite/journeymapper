import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.alchemydumps import AlchemyDumps, AlchemyDumpsCommand
from app import app, db

app.config.from_object(os.environ['APP_SETTINGS'])

# Flask-Migrate support
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# AlchemyDumps support
alchemydumps = AlchemyDumps(app, db)
manager.add_command('dump', AlchemyDumpsCommand)

if __name__ == '__main__':
    manager.run()
