import re

class ValidationMethods:
    
    def not_null_validator(self, v, field):
        if v == '':
            raise ValueError(f'{field} must be required')
        return v
    
    def password_validator(self, v):
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        pattern = re.compile(reg)
        
        if not(match := re.search(pattern, v)):
            """Length should be at least 6
            Length should be not be greater than 20
            Password should have at least one numeral
            Password should have at least one uppercase letter
            Password should have at least one lowercase letter
            Password should have at least one of the symbols $@#
            """
            return False
        return True
    
    def email_validator(self, v):
        # regular expression for email validation
        reg = "([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])"
        
        pattern = re.compile(reg)
        if not(match := re.search(pattern, v)):
            raise ValueError("Invalid Email format")  
        return v     