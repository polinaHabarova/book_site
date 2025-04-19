from app.data_base import engine, Base
from app import models

if __name__ == '__main__':
    Base.metadata.create_all(bind = engine)