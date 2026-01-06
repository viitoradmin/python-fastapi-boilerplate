"""
API Key utilities module.

This module provides functions for generating, hashing, and validating API keys.
"""
import secrets
import hashlib
import hmac
from typing import Tuple
from datetime import datetime, timedelta

from app.utils.security import password_hasher


def generate_api_key() -> Tuple[str, str, str]:
    """
    Generate a new API key with prefix and hash.
    
    Returns:
        Tuple[str, str, str]: (full_api_key, key_prefix, key_hash)
            - full_api_key: The complete API key to return to user
            - key_prefix: First 8 characters for identification
            - key_hash: Hashed version for database storage
    """
    # Generate a secure random key (32 bytes = 256 bits)
    key_bytes = secrets.token_bytes(32)
    
    # Convert to base64-like string but URL-safe
    key_b64 = secrets.token_urlsafe(32)
    
    # Create the full API key with prefix
    prefix = "ak_"  # API Key prefix
    timestamp = datetime.utcnow().strftime("%Y%m%d")
    full_key = f"{prefix}{timestamp}_{key_b64}"
    
    # Extract prefix for identification (first 8 chars after ak_)
    key_prefix = full_key[:12]  # ak_YYYYMMDD
    
    # Hash the full key for secure storage
    key_hash = hash_api_key(full_key)
    
    return full_key, key_prefix, key_hash


def hash_api_key(api_key: str) -> str:
    """
    Hash an API key using Argon2id for secure storage.
    
    Args:
        api_key: The API key to hash
        
    Returns:
        str: Hashed API key
    """
    return password_hasher.hash(api_key)


def verify_api_key(api_key: str, hashed_key: str) -> bool:
    """
    Verify an API key against its hash.
    
    Args:
        api_key: The plain API key to verify
        hashed_key: The hashed API key from database
        
    Returns:
        bool: True if key matches, False otherwise
    """
    try:
        password_hasher.verify(hashed_key, api_key)
        return True
    except Exception:
        return False


def extract_key_prefix(api_key: str) -> str:
    """
    Extract the prefix from an API key for identification.
    
    Args:
        api_key: The full API key
        
    Returns:
        str: The key prefix
    """
    if not api_key.startswith("ak_"):
        return ""
    
    # Extract first 12 characters (ak_YYYYMMDD)
    return api_key[:12] if len(api_key) >= 12 else api_key


def is_valid_api_key_format(api_key: str) -> bool:
    """
    Check if an API key has the correct format.
    
    Args:
        api_key: The API key to validate
        
    Returns:
        bool: True if format is valid, False otherwise
    """
    if not isinstance(api_key, str):
        return False
    
    # Check prefix
    if not api_key.startswith("ak_"):
        return False
    
    # Check minimum length (ak_ + YYYYMMDD + _ + at least 20 chars)
    if len(api_key) < 35:
        return False
    
    # Check date format in prefix
    try:
        date_part = api_key[3:11]  # YYYYMMDD
        datetime.strptime(date_part, "%Y%m%d")
    except ValueError:
        return False
    
    # Check underscore separator
    if api_key[11] != "_":
        return False
    
    return True


def generate_api_key_with_expiry(days: int = 365) -> Tuple[str, str, str, datetime]:
    """
    Generate an API key with expiration date.
    
    Args:
        days: Number of days until expiration
        
    Returns:
        Tuple[str, str, str, datetime]: (full_api_key, key_prefix, key_hash, expires_at)
    """
    full_key, key_prefix, key_hash = generate_api_key()
    expires_at = datetime.utcnow() + timedelta(days=days)
    
    return full_key, key_prefix, key_hash, expires_at


def mask_api_key(api_key: str) -> str:
    """
    Mask an API key for safe display.
    
    Args:
        api_key: The API key to mask
        
    Returns:
        str: Masked API key showing only prefix and last 4 characters
    """
    if not api_key or len(api_key) < 8:
        return "***"
    
    prefix = api_key[:12] if api_key.startswith("ak_") else api_key[:4]
    suffix = api_key[-4:]
    
    return f"{prefix}...{suffix}"


def validate_api_key_strength(api_key: str) -> dict:
    """
    Validate the strength and format of an API key.
    
    Args:
        api_key: The API key to validate
        
    Returns:
        dict: Validation results with is_valid and issues
    """
    issues = []
    
    # Check format
    if not is_valid_api_key_format(api_key):
        issues.append("Invalid API key format")
    
    # Check length
    if len(api_key) < 40:
        issues.append("API key too short")
    
    # Check for common patterns that might indicate weak generation
    if api_key.count("a") > len(api_key) * 0.3:
        issues.append("API key may be weakly generated")
    
    return {
        "is_valid": len(issues) == 0,
        "issues": issues,
        "strength": "strong" if len(issues) == 0 else "weak"
    }


def get_rate_limit_key(api_key_id: int, window: str = "hour") -> str:
    """
    Generate a rate limiting key for an API key.
    
    Args:
        api_key_id: The API key ID
        window: Time window (hour, day, etc.)
        
    Returns:
        str: Rate limiting key
    """
    timestamp = datetime.utcnow()
    
    if window == "hour":
        time_key = timestamp.strftime("%Y%m%d%H")
    elif window == "day":
        time_key = timestamp.strftime("%Y%m%d")
    else:
        time_key = timestamp.strftime("%Y%m%d%H%M")
    
    return f"api_key_rate_limit:{api_key_id}:{window}:{time_key}"