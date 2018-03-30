from .models import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

def init_db():
    engine = create_engine('sqlite:///journals.db')
    session = Session(engine)
    Base.metadata.create_all(engine)
    session.commit()
    session.close()

if __name__ == '__main__':
    init_db()
