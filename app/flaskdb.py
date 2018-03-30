from flask_sqlalchemy import SQLAlchemy
from ..database.models import metadata

db = SQLAlchemy(metadata=metadata)
