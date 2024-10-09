import sys
from src.logger import logging

def error_message_detail(error, error_detail):
    _, _, exc_tb = error_detail.exc_info()  # Retrieve the traceback object
    file_name = exc_tb.tb_frame.f_code.co_filename  # Get the file name where the error occurred
    line_number = exc_tb.tb_lineno  # Get the line number
    error_message = f"Error occurred in python script name [{file_name}] line number [{line_number}] error message [{str(error)}]"
    return error_message


class CustomException(Exception):
    def __init__(self, error_message: str, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message
        self.error_detail = error_detail
        
    def __str__(self):
        return f"Error occurred: {self.error_message}, Details: {self.error_detail}"
    

if __name__ == "__main__":
    try:
        a = 1 / 0
    except ZeroDivisionError as e:
        logging.error("ZeroDivisionError occurred")
        raise CustomException(e, sys)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        raise CustomException(e, sys)