from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

def upsert(session: Session, model, data: dict, overwrite=False):
    instance = session.query(model).get(data['UID'])
    if instance:
        if overwrite:
            # Update the existing instance with new data
            for key, value in data.items():
                setattr(instance, key, value)
            session.commit()
        else:
            # The record exists and we do not want to overwrite it
            # Handle this case as needed, e.g., raise an error or skip
            pass
    else:
        # The record does not exist, so insert a new one
        instance = model(**data)
        session.add(instance)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            # Handle the integrity error, e.g., a duplicate UID that was added since we checked
