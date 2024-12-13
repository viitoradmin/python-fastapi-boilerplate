"""This module contains database operations methods."""
from sqlalchemy.orm import Session


class UserAuthMethod():
    """This class defines methods to authenticate users."""

    def __init__(self, model) -> None:
        self.model = model

    def find_by_email(self, db: Session, email: str):
        """This funtion will return the email object"""
        return db.query(self.model).filter(
            self.model.email == email
            ).first()

    def find_by_username(self, db: Session, username: str):
        """This function will return the username object"""
        return db.query(self.model).filter(
            self.model.username == username
            ).first()
