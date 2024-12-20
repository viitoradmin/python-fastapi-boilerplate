"""This module contains database operations methods."""

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserAuthMethod:
    """This class defines methods to authenticate users."""

    def __init__(self, model) -> None:
        self.model = model

    async def find_by_email(self, db: AsyncSession, email: str):
        """This function will return the user object by email asynchronously."""
        async with db:  # Ensure the session context
            stmt = select(self.model).where(self.model.email == email)
            result = await db.execute(stmt)
            return result.scalars().first()

    async def find_by_username(self, db: AsyncSession, username: str):
        """This function will return the username object"""
        async with db:  # Ensure the session context
            stmt = select(self.model).where(self.model.username == username)
            result = await db.execute(stmt)
            return result.scalars().first()

    async def find_user_by_otp_referenceId(
        self, db: AsyncSession, otp_referenceId: str
    ):
        """This function will return the username object"""
        async with db:  # Ensure the session context
            stmt = select(self.model).where(
                self.model.otp_referenceId == otp_referenceId
            )
            result = await db.execute(stmt)
            return result.scalars().first()

    async def find_verified_phone_user(self, db: AsyncSession, phone: str):
        """This function will return the username object"""
        async with db:  # Ensure the session context
            stmt = select(self.model).where(self.model.phone == phone)
            result = await db.execute(stmt)
            return result.scalars().first()

    async def find_verified_email_user(self, db: AsyncSession, email: str):
        """This function will return the username object"""
        async with db:  # Ensure the session context
            stmt = select(self.model).where(self.model.email == email)
            result = await db.execute(stmt)
            return result.scalars().first()
