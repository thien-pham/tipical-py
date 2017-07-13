import datetime
from sqlalchemy import Column, Integer, String, Sequence, DateTime
from .database import Base

class Tip(Base):
    __tablename__ = "tips"

    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    body = Column(String(1024))
    datetime = Column(DateTime, default=datetime.datetime.now)
    # TODO: add in location

    def as_dictionary(self):
        tip = {
            "id": self.id,
            "title": self.title,
            "body": self.body
        }
        return tip


Base.metadata.create_all(engine)
