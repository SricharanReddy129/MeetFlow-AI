# validate_jwt.py

import os
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt import PyJWKClient

security = HTTPBearer()

CLERK_JWKS_URL = os.getenv("CLERK_JWKS_URL")
if not CLERK_JWKS_URL:
    raise ValueError("CLERK_JWKS_URL environment variable is missing")

jwks_client = PyJWKClient(CLERK_JWKS_URL)


def decode_clerk_token(token: str) -> str:
    """
    Core verification logic. Used by both the middleware and the
    legacy per-route dependency below.
    """
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            options={"verify_aud": False},
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token valid, but lacks user identity (sub).",
            )
        return user_id

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session has expired.",
        )
    except jwt.PyJWKClientError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to reach the token issuer for validation.",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
        )


def verify_clerk_session(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Kept for backward compatibility; no longer used by routes after this change."""
    return decode_clerk_token(credentials.credentials)


def get_current_user(request: Request) -> str:
    """
    New dependency: reads the clerk_user_id that ClerkAuthMiddleware
    already verified and attached to request.state.
    """
    user_id = getattr(request.state, "clerk_user_id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated.")
    return user_id