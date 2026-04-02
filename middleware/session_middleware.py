from fastapi import Depends, Header, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from itsdangerous import BadSignature, TimestampSigner

from config import db_config, session_config
from core import SessionService
from core.utils import EnrytionDecrytionUtils, SessionUtils, constant_variable


class SessionMiddleware:

    # Initialize OAuth credentials
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    # Signer for secure cookies
    signer = TimestampSigner(session_config.SECRET_KEY)

    async def validate_session(
        self,
        request: Request,
        user_agent: str = Header(default=constant_variable.STATUS_NULL),
        token: str = Depends(oauth2_scheme),
    ):
        """
        Validates the session cookie and token in the request header.

        Verifies the session cookie is signed with the secret key and is not expired.
        Decrypts the session data and verifies the session ID matches the current user-agent and IP.
        If valid, attaches the session data to the request for use in routes.

        If the session is invalid or expired, raises an HTTPException with a 401 status code.

        Args:
            request (Request): The request object.
            user_agent (str): The user-agent header from the request.
            token (str): The Bearer token from the request header.

        Returns:
            None
        """
        cookie = request.cookies.get("session")
        client_ip = SessionUtils().get_client_ip(request)
        session_id = SessionUtils().generate_session_id(
            user_agent=user_agent, ip=client_ip
        )

        if not cookie:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No session cookie provided.",
            )

        session_key = self.signer.unsign(
            cookie, max_age=session_config.SESSION_TIMEOUT
        ).decode()

        try:
            encrypted_session_data = await SessionService().get_session_context(
                session_key=session_key,
            )

            if not encrypted_session_data:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Session expired or invalid.",
                )

            # Decrypt session data
            session_data = EnrytionDecrytionUtils().decrypt_data(encrypted_session_data)

            # Validate session ID matches the current user-agent and IP
            if session_key != session_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Session does not match the browser and IP.",
                )

            # Attach session data to request for use in routes
            request.state.session = session_data

        except BadSignature:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid session signature.",
            )
        finally:
            await db_config.session.remove()
            await SessionService().reset_session_context(session_key=session_key)
