from fastapi import Depends
from config import database
from apps.constant import constant
from sqlalchemy.orm import Session

getdb = database.get_db

class BaseMethods():
    """This class provides basic DB methods"""
    
    def __init__(self, model):
        self.model = model
    
    def save(self, validate_data, db: Session = Depends(getdb)):
        """this function saves the object to the database for the given model
        Args:
            validate_data (dict): validate data
            db (Session): database session.
        Returns:
            returns the created object
        """
        try:
            db.add(validate_data)
            db.commit()
            db.refresh(validate_data)
            return constant.STATUS_TRUE
        except Exception as err:
            print(err)
            db.rollback()
            db.close()
            return constant.STATUS_FALSE
    
    def find_by_uuid(self, db: Session = Depends(getdb)):
        """This function is used to find users."""
        return db.query(self.model).filter(self.model.deleted_at == None).all()
    