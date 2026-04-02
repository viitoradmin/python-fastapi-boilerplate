from log_service import LOG_CONFIG

class LoggingConfig:
    def __init__(self):
        self.config = LOG_CONFIG
        
    def get_config(self):
        return self.config
    
    
LOGGING_CONFIG = LoggingConfig()