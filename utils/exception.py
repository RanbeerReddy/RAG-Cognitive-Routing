from logger import logger
import sys

class RAGException(Exception):
    """Base class for exceptions in RAG."""
    def __init__(self, error_message, error_details=None):
        super().__init__(str(error_message))

        self.error_message = error_message

        if error_details:
            _,_,exc_tb = error_details.exc_info()

            if exc_tb:
                self.lineno = exc_tb.tb_lineno
                self.filename = exc_tb.tb_frame.f_code.co_filename
            else:
                self.lineno = None
                self.filename = None
        else:
            self.lineno = None
            self.filename = None

    def __str__(self):
        logger.error(f"Error occurred in script: {self.filename} at line number: {self.lineno} with error message: {self.error_message}")
        return f"Error occurred in script: {self.filename} at line number: {self