import os

def log_error(city: str, error_message, error_logs_directory: str ='results/error_logs'):
    error_log_path = f'{error_logs_directory}/{city}_error.txt'
    os.makedirs(error_logs_directory, exist_ok=True)
    with open(error_log_path, 'w') as error_file:
        error_file.write(f'Error processing {city}: {error_message}\n')