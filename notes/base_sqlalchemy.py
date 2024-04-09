# base_model.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///yourdatabase.db')
SessionLocal = sessionmaker(bind=engine)

class CRUDMixin(Base):
    __abstract__ = True  # This makes sure SQLAlchemy doesn't try to create a table for this model

    @classmethod
    def create(cls, db_session: Session, **kwargs):
        instance = cls(**kwargs)
        db_session.add(instance)
        db_session.commit()
        db_session.refresh(instance)
        return instance

    @classmethod
    def read(cls, db_session: Session, id):
        return db_session.query(cls).filter_by(id=id).first()

    @classmethod
    def update(cls, db_session: Session, id, **kwargs):
        instance = db_session.query(cls).filter_by(id=id).first()
        for attr, value in kwargs.items():
            setattr(instance, attr, value)
        db_session.commit()
        return instance

    @classmethod
    def delete(cls, db_session: Session, id):
        instance = db_session.query(cls).filter_by(id=id).first()
        db_session.delete(instance)
        db_session.commit()

# Don't forget to create the tables in your database
Base.metadata.create_all(engine)
