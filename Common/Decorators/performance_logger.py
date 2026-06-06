import time
import pymssql

def performance_logger_decorator(main_function):
    def wrapper(*args, **kwargs):

        function_name = main_function.__name__
        start_time = time.time()
        result = main_function(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time

        with pymssql.connect(host="KIMYA_LAPTOP\SQLSERVERTEST", database="CoreBankingDB") as connection:
            cursor = connection.cursor()
            cursor.execute("""
            Insert  PerformanceLogger(FunctionName, ExecutionTime)
            Values  (%s,%d)""", (function_name, execution_time))
            connection.commit()
            
        return result
    return wrapper