from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config import db_config
from core.utils import constant_variable

getdb = db_config.session_factory()


class DataBaseMethod:
    """This class is provide the database methods"""

    def __init__(self, model):
        self.model = model

    async def save(self, validate_data, db: AsyncSession = Depends(getdb)):
        """This function creates a new object asynchronously.

        Arguments:
            self(db): database session
            validate_data (dict): validated data to be saved

        Returns:
            Returns the status of the operation (True/False).
        """
        try:
            async with db.begin():  # Start a transaction asynchronously
                db.add(validate_data)  # Add the object to the session
                await db.commit()
                await db.flush()  # Asynchronously flush the changes to the database
            return constant_variable.STATUS_TRUE
        except Exception as err:
            print(err)
            # Rollback is handled automatically when the transaction is not committed.
            return constant_variable.STATUS_FALSE

    async def save_all(self, validate_data: list, db: AsyncSession = Depends(getdb)):
        """Saves bulk data in the database."""
        try:
            db.add_all(validate_data)
            await db.commit()
            await db.flush()
            return constant_variable.STATUS_TRUE
        except Exception as err:
            print(err)
            db.rollback()
            db.close()
            return constant_variable.STATUS_FALSE

    async def bulk_insert_mapping(
        self, validate_data: dict, db: AsyncSession = Depends(getdb)
    ):
        """Saves bulk data in the database with its mapping"""
        try:
            db.bulk_insert_mappings(self.model, validate_data)
            await db.commit()
            await db.flush()
            return constant_variable.STATUS_TRUE
        except Exception as err:
            print(err)
            db.rollback()
            db.close()
            return constant_variable.STATUS_FALSE

    async def destroy(self, instance: object, db: AsyncSession = Depends(getdb)):
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
            await db.commit()
            await db.flush()
            return constant_variable.STATUS_TRUE
        except Exception as e:
            return constant_variable.STATUS_FALSE
