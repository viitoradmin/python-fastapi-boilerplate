from fastapi import Depends
from sqlalchemy.orm import Session

from config import db_config
from core.utils import constant_variable

getdb = db_config.session_factory()


class DataBaseMethod:
    """This class is provide the database methods"""

    def __init__(self, model):
        self.model = model

    def save(self, validate_data, db: Session = Depends(getdb)):
        """This function creates new object

        Arguments:
            self(db): database session
            validate_data (dict): validate data

        Returns:
            Returns the creates object
        """
        try:
            db.add(validate_data)
            db.flush()  # Changed this to a flush
            db.refresh(validate_data)
            return constant_variable.STATUS_TRUE
        except Exception as err:
            print(err)
            db.rollback()
            return constant_variable.STATUS_FALSE

    def save_all(self, validate_data: list, db: Session = Depends(getdb)):
        """Saves bulk data in the database."""
        try:
            db.add_all(validate_data)
            db.flush()  # Changed this to a flush
            db.refresh(validate_data)
            return constant_variable.STATUS_TRUE
        except Exception as err:
            print(err)
            db.rollback()
            db.close()
            return constant_variable.STATUS_FALSE

    def bulk_insert_mapping(self, validate_data: dict, db: Session = Depends(getdb)):
        """Saves bulk data in the database with its mapping"""
        try:
            db.bulk_insert_mappings(self.model, validate_data)
            db.flush()  # Changed this to a flush
            db.refresh(validate_data)
            return constant_variable.STATUS_TRUE
        except Exception as err:
            print(err)
            db.rollback()
            db.close()
            return constant_variable.STATUS_FALSE

    def destroy(self, instance: object, db: Session = Depends(getdb)):
        """This function take a ID and destroy the object

        Arguments:
            self(db): database session
            models (object): models
            uuid (str): Object ID

        Returns:
            Returns the successfull API basic response format.
        """
        try:
            db.delete(instance=instance)
            db.flush()  # Changed this to a flush
            db.refresh(instance)
            return constant_variable.STATUS_TRUE
        except Exception as e:
            return constant_variable.STATUS_FALSE
