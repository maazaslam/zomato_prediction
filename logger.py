import datetime


class Logging:

    def __init__(self, file_name):
        self.date = datetime.datetime.now().date()
        self.time = datetime.datetime.now().strftime("%H:%M:%S")
        self.file_name = f'Logs/{file_name}.txt'
        open(f'{self.file_name}', 'a+')

    def log(self, log_message):
        with open(rf'{self.file_name}', 'a+') as file:
                file.write(f'{self.date}--{self.time}--{log_message} \n')

