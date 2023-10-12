from passlib.context import CryptContext

class PasswordUtils():
    """This class is used to manage password management"""
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
    
    def hash_password(self, password: str):
        """
        This function is used to hash password
        Arguments: 
            password(str) : password argument of string format.
        
        Returns: 
            Hash of the password
        """
        return self.pwd_context.hash(password)       