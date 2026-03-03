import base64
import hashlib
import hmac
import json
import os
import time
from dataclasses import dataclass

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me")
TOKEN_TTL_SECONDS = int(os.getenv("TOKEN_TTL_SECONDS", "3600"))
security = HTTPBearer(auto_error=False)


@dataclass
class AuthUser:
    username: str
    role: str
    organization_id: int


# bootstrap users (replace with DB-backed users)
USER_STORE = {
    "admin@bridgaton.ai": {
        "password": "admin123",
        "role": "admin",
        "organization_id": 1,
    },
    "analyst@bridgaton.ai": {
        "password": "analyst123",
        "role": "analyst",
        "organization_id": 1,
    },
    "viewer@bridgaton.ai": {
        "password": "viewer123",
        "role": "viewer",
        "organization_id": 1,
    },
}


def _sign(payload_b64: bytes) -> str:
    return hmac.new(SECRET.encode("utf-8"), payload_b64, hashlib.sha256).hexdigest()


def create_access_token(username: str, role: str, organization_id: int) -> str:
    payload = {
        "sub": username,
        "role": role,
        "org": organization_id,
        "exp": int(time.time()) + TOKEN_TTL_SECONDS,
    }
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode("utf-8")).rstrip(b"=")
    signature = _sign(payload_b64)
    return f"{payload_b64.decode('utf-8')}.{signature}"


def _decode_token(token: str) -> AuthUser:
    try:
        payload_part, signature = token.split(".", 1)
        payload_b64 = payload_part.encode("utf-8")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token format") from exc

    if not hmac.compare_digest(_sign(payload_b64), signature):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token signature")

    padded = payload_b64 + b"=" * (-len(payload_b64) % 4)
    payload = json.loads(base64.urlsafe_b64decode(padded).decode("utf-8"))
    if int(payload.get("exp", 0)) < int(time.time()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")

    return AuthUser(
        username=payload["sub"],
        role=payload["role"],
        organization_id=int(payload["org"]),
    )


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> AuthUser:
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    return _decode_token(credentials.credentials)


def require_roles(*roles: str):
    def _dependency(user: AuthUser = Depends(get_current_user)) -> AuthUser:
        if user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        return user

    return _dependency
