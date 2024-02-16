import pandas as pd
import os
import logging
import re as regex
import configparser

class PyRenameDirs:

    def initialize_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(str(self.__str__))
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler('output.log')
        c_handler.setLevel(logging.WARNING)
        f_handler.setLevel(logging.INFO)
        c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        f_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        self.logger.addHandler(c_handler)
        self.logger.addHandler(f_handler)

    def __init__(self):
        self.initialize_logging()
        self.df = pd.read_csv('./data/examples.csv')
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.outputs_dir = config['DIRS']['output_dir']
        self.logger.info('initialized PyRenameDirs...')


    def __str__(self) -> str:
        return "PyRenameDirs"

    def validator(self, directory) -> bool:
        self.logger.info('validating of directory: {}'.format(directory))
        if regex.search(r'\d', directory):
            return True
        else:
            return False

    def getCurrentDirs(self) -> list:
        self.logger.info('fetching fasta file directories')
        return os.listdir(self.outputs_dir)

    def run(self):
        directories = self.getCurrentDirs()
        for dir in range(0, len(directories)):
            if self.validator(directories[dir]):
                self.logger.info('validated directory: {}'.format(directories[dir]))
                dir_new = self.df.iloc[dir]['specimen_id']
                os.rename(f'{self.outputs_dir}/{directories[dir]}', f'{self.outputs_dir}/{dir_new}')
            else:
                self.logger.error('failed to validate directory: {}'.format(directories[dir]))

if __name__ == '__main__':
    pyRenameDirs = PyRenameDirs()
    pyRenameDirs.run()
