import datetime
from sqlalchemy import Column, Integer, String, Sequence, DateTime
from .database import Base

class Tip(Base):
    __tablename__ = "tips"

    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    body = Column(String(1024))
    datetime = Column(DateTime, default=datetime.datetime.now)
    # votes = Column(Integer)

    def as_dictionary(self):
        tip = {
            "id": self.id,
            "title": self.title,
            "body": self.body
            # "timestamp": self.timestamp
        }
        return tip
  #   date: {type: Date, default: Date.now()},
  # location:{ type: [Number], index: '2dsphere',},
  # tags: Array,
  # points: {type: Array, default: []}

Base.metadata.create_all(engine)
