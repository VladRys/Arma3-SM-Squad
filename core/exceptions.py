from logs.setup_logs import setup_logger

class CustomException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.l = setup_logger()
    
    def log(self):
        self.l.info(f"[Custom Exception] {self.message}")
        
class AgeVerifException(CustomException):
    def __init__(self, message: str, user):
        super().__init__(message)
        self.user = user
    def log(self):
        self.l.info(f"[AgeVerifException] {self.user} {self.message}")
            
