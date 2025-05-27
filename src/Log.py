LOG_PATH = "./log.txt"

class Log:
    def __init__(self):
        self.path = LOG_PATH

    def message(self, message, level='INFO'):
        f_message = f"[{level}] - {message}"
        print(f_message)
        with open(self.path, 'a') as f:
            f.write(f_message + '\n')