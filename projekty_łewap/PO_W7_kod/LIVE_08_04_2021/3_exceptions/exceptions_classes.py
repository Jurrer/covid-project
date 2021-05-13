class InvalidStudentParamsException(Exception):
    def __init__(self, arg_name):
        msg = f"Error! InvalidStudentParamsException (arg name: {arg_name})"
        super().__init__(msg)


class StudentNotExistsException(Exception):
    def __init__(self, message):
        super().__init__(message)


class StudentCurrentlyExistsException(Exception):
    def __init__(self, message):
        super().__init__(message)
