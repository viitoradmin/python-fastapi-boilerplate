import hashlib

from fastapi import Header, Request
from itsdangerous import TimestampSigner

from config import redis_config, session_config
from core.utils import EnrytionDecrytionUtils, SessionUtils, constant_variable


class SessionService:
    # Signer for secure cookies
    signer = TimestampSigner(session_config.SECRET_KEY)

    def generate_session_functionality(
        self,
        request: Request,
        user_agent: str = Header(default=constant_variable.STATUS_NULL),
    ):
        # Generate session ID
        client_ip = SessionUtils().get_client_ip(request)
        session_key = self.generate_session_id(user_agent=user_agent, ip=client_ip)

        # Encrypt and store session in Redis
        session_data = EnrytionDecrytionUtils().encrypt_data("user_data_here")
        # Set redis context
        self.set_session_context(session_key=session_key, session_data=session_data)

        # Set signed cookie
        signed_session = self.signer.sign(session_key)
        session_cookie = {
            "key": "session",
            "value": signed_session,
            "httponly": constant_variable.STATUS_TRUE,
            "secure": constant_variable.STATUS_TRUE,
            "samesite": "Strict",
            "max_age": session_config.SESSION_TIMEOUT,  # Expires time
        }

        return session_cookie

    # Utility functions
    def generate_session_id(self, user_agent: str, ip: str) -> str:
        """Generates a session ID bound to user-agent and IP."""
        return hashlib.sha256(
            f"{session_config.SECRET_KEY}{user_agent}{ip}".encode()
        ).hexdigest()

    # Redis-based session context functions
    async def get_session_context(self, session_key: str) -> str:
        """Retrieve session context from Redis."""
        return await redis_config.redis_client.get(session_key)

    def set_session_context(self, session_key: str, session_data: str):
        return redis_config.redis_client.set(
            session_key, session_data, ex=session_config.SESSION_TIMEOUT
        )

    async def reset_session_context(self, session_key: str) -> None:
        """Delete session context in Redis."""
        await redis_config.redis_client.delete(session_key)
