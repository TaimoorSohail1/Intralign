from typing import Annotated

from fastapi import Header, HTTPException, status


def require_access_token(
    authorization: Annotated[str | None, Header()] = None,
) -> str:
    scheme, separator, token = (authorization or "").partition(" ")
    if separator != " " or scheme.lower() != "bearer" or not token.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )
    return token.strip()
