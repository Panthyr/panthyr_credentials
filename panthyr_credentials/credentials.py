#! /usr/bin/python3
# coding: utf-8

# Module: panthyr_credentials
# Authors: Dieter Vansteenwegen
# Institution: VLIZ (Vlaams Institute voor de Zee)

__author__ = 'Dieter Vansteenwegen'
__version__ = '0.1b'
__credits__ = 'Dieter Vansteenwegen'
__email__ = 'dieter.vansteenwegen@vliz.be'
__status__ = 'Development'
__project__ = 'Panthyr'
__project_link__ = 'https://waterhypernet.org/equipment/'

from typing import Dict, Union
import logging
from os import path
from configparser import ConfigParser

CRED_LOCATION_DEFAULT = '/home/hypermaq/data/credentials'
CREDENTIALS_DEFAULT = ('email_user', 'email_password', 'email_server_port', 'ftp_server',
                       'ftp_user', 'ftp_password', 'cam_user', 'cam_password'
                       )  # Used when creating an empty credentials file


def initialize_logger() -> logging.Logger:
    """Set up logger
    If the module is ran as a module, name logger accordingly as a sublogger.
    Returns:
        logging.Logger: logger instance
    """
    if __name__ == '__main__':
        return logging.getLogger('{}'.format(__name__))
    else:
        return logging.getLogger('__main__.{}'.format(__name__))


class CredentialsDontExistError(Exception):
    pass


class CredentialsFileExistError(Exception):
    pass


class Credentials:
    """Variable abbreviations: c = credential, v = value"""
    def __init__(self, cred_location: str = CRED_LOCATION_DEFAULT):
        self.cred_location = cred_location
        self._init_logging()
        self.credentials: Dict[str, str] = {}

        self._parser = ConfigParser()
        if self._file_exists():
            self.parse()

    def _file_exists(self) -> bool:
        return path.isfile(self.cred_location)

    def _init_logging(self):
        self.log = initialize_logger()

    def parse(self):
        if not self._file_exists:
            self.log.info(f'Credentials file {self.cred_location} does not exist.')
            raise CredentialsDontExistError
        self._parser.read(self.cred_location)
        for c, v in self._parser.items('credentials'):
            self.credentials[c] = v

    def get_cred(self, cred: str) -> Union[str, None]:
        return self.credentials.get(cred, None)

    def get_all(self) -> Dict[str, str]:
        return self.credentials

    def create_empty(self):
        if self._file_exists():
            raise CredentialsFileExistError

        self._parser.add_section('credentials')
        for cred in CREDENTIALS_DEFAULT:
            self._parser.set('credentials', cred, '')
        self._parser.write(open(self.cred_location, 'x'))