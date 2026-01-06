"""
Security utilities module.

This module provides password hashing and verification functions using Argon2.
"""
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, HashingError

# Argon2 password hasher with optimized parameters
# time_cost=3: Number of iterations (higher = more secure but slower)
# memory_cost=65536: Memory usage in KiB (64MB, good balance for production)
# parallelism=1: Number of parallel threads (1 is sufficient for most cases)
# hash_len=32: Length of the hash in bytes
# salt_len=16: Length of the salt in bytes
password_hasher = PasswordHasher(
    time_cost=3,
    memory_cost=65536,  # 64MB
    parallelism=1,
    hash_len=32,
    salt_len=16
)


def hash_password(password: str) -> str:
    """
    Hash a password using Argon2id.
    
    Args:
        password: Plain text password
        
    Returns:
        str: Hashed password using Argon2id
        
    Raises:
        HashingError: If password hashing fails
    """
    try:
        return password_hasher.hash(password)
    except Exception as e:
        raise HashingError(f"Failed to hash password: {str(e)}") from e


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its Argon2 hash.
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Argon2 hashed password to compare against
        
    Returns:
        bool: True if password matches, False otherwise
    """
    try:
        password_hasher.verify(hashed_password, plain_password)
        return True
    except VerifyMismatchError:
        return False
    except Exception:
        # Log the exception in production, but don't expose details
        return False


def check_needs_rehash(hashed_password: str) -> bool:
    """
    Check if a password hash needs to be rehashed with current parameters.
    
    Args:
        hashed_password: Existing Argon2 hash
        
    Returns:
        bool: True if hash should be updated, False otherwise
    """
    try:
        return password_hasher.check_needs_rehash(hashed_password)
    except Exception:
        # If we can't check, assume it needs rehashing
        return True

