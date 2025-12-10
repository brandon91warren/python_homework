import logging

logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log", "a"))

def logger_decorator(func):
    def wrapper(*args, **kwargs):
     
        pos_params = list(args) if args else "none"
        kw_params = kwargs if kwargs else "none"

        
        result = func(*args, **kwargs)

        
        logger.log(logging.INFO, f"function: {func.__name__}")
        logger.log(logging.INFO, f"positional parameters: {pos_params}")
        logger.log(logging.INFO, f"keyword parameters: {kw_params}")
        logger.log(logging.INFO, f"return: {result}")
        logger.log(logging.INFO, "-----------------------")

        return result
    return wrapper


# Function 1 
@logger_decorator
def hello_world():
    print("Hello, World!")


# Function 2
@logger_decorator
def many_positional(*args):
    return True


# Function 3 
@logger_decorator
def many_keyword(**kwargs):
    return logger_decorator


# MAINLINE CALLS
if __name__ == "__main__":
    hello_world()
    many_positional(1, 2, 3, 4)
    many_keyword(a=10, b=20, c="hello")
