# validate_jwt.py

import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt import PyJWKClient

# 1. Initialize the HTTP Bearer security scheme
security = HTTPBearer()

# 2. Point to Clerk's central JWKS endpoint (the issuer)
# Example format: https://clerk.your-domain.com/.well-known/jwks.json
CLERK_JWKS_URL = os.getenv("CLERK_JWKS_URL") 
if not CLERK_JWKS_URL:
    raise ValueError("CLERK_JWKS_URL environment variable is missing")

# Initialize the JWKS client to fetch keys directly from Clerk
jwks_client = PyJWKClient(CLERK_JWKS_URL)

def verify_clerk_session(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Validates the JWT against the issuer's public keys.
    Returns the Clerk user_id (sub) if valid.
    """
    token = credentials.credentials
    
    try:
        # Fetch the exact public key Clerk used to sign this specific token
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        
        # Validate the token mathematically using the issuer's key
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            # If you configured a specific audience in Clerk, verify it here
            options={"verify_aud": False} 
        )
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Token valid, but lacks user identity (sub)."
            )
            
        return user_id
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Session has expired."
        )
    except jwt.PyJWKClientError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Unable to reach the token issuer for validation."
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid authentication token."
        )