#! /usr/bin/python3
# -*- coding: utf-8 -*-
# Authors: Dieter Vansteenwegen
# Institution: VLIZ (Vlaams Instituut voor de Zee)

__author__ = 'Dieter Vansteenwegen'
__email__ = 'dieter.vansteenwegen@vliz.be'
__project__ = 'Panthyr'
__project_link__ = 'https://waterhypernet.org/equipment/'

from typing import Dict, Union
import logging
from os import path
import configparser

CRED_LOCATION_DEFAULT = '/home/panthyr/data/credentials'
CREDENTIALS_DEFAULT = (
    'email_user',
    'email_password',
    'email_server_port',
    'ftp_server',
    'ftp_user',
    'ftp_password',
)  # Used when creating an empty credentials file


def initialize_logger() -> logging.Logger:
    """Set up logger
    If the module is ran as a module, name logger accordingly as a sublogger.
    Returns:
        logging.Logger: logger instance
    """
    if __name__ == '__main__':
        return logging.getLogger(f'{__name__}')
    else:
        return logging.getLogger(f'__main__.{__name__}')


class CredentialsDontExistError(Exception):
    """The credentials file does not exist on the host system."""
    pass


class CredentialsInvalidFormat(Exception):
    """The credentials file does not exist on the host system."""
    pass


class CredentialsFileExistError(Exception):
    """The credentials file already exists on the host system."""
    pass


class pCredentials:
    """ Provide access and functions for credentials file.

    Credentials file contains credentials for specific Panthyr station.
    This class allows creation of a blank credentials file,
    as well as getting the data from an existing one.
    """

    def __init__(self, cred_location: str = CRED_LOCATION_DEFAULT):
        self.cred_location = cred_location
        self._init_logging()
        self.credentials: Dict[str, str] = {}

        self._parser = configparser.ConfigParser()
        if self._file_exists():
            self.parse()

    def _file_exists(self) -> bool:
        """Check if the file exists on the host system.

        Returns:
            bool: True if self.cred_location is an existing file.
        """
        return path.isfile(self.cred_location)

    def _init_logging(self):
        """Initialize logging (self.log)"""
        self.log = initialize_logger()

    def parse(self):
        """Populate self.credentials dict from the credentials file.

        Raises:
            CredentialsDontExistError: If the file doesn't exist on disk.
        """
        if not self._file_exists:
            self.log.error(
                f'Credentials file {self.cred_location} does not exist. ',
                f'Creating a blank one at {CRED_LOCATION_DEFAULT}.',
                ' Please fill in all fields.',
            )
            self.create_empty()
            raise CredentialsDontExistError
        try:
            self._parser.read(self.cred_location)
        except configparser.MissingSectionHeaderError as e:
            self.log.exception(
                f'Header info missing in file {self.cred_location}.\n'
                'Add [credentials] section in file.', )
            raise CredentialsInvalidFormat from e
        else:
            for c, v in self._parser.items('credentials'):
                self.credentials[c] = v

    def get_cred(self, cred: str) -> Union[str, None]:
        """Return one specific credential if it exists in the dict.

        Args:
            cred (str): The credential to return.

        Returns:
            Union[str, None]: The value of the requested credential or None if it doesn't exist.
        """
        return self.credentials.get(cred, None)

    def get_all(self) -> Dict[str, str]:
        """Return a dict with all credentials.

        Returns:
            Dict[str, str]: Dict with all the credential,value pairs.
        """
        return self.credentials

    def create_empty(self):
        """Create an empty credentials file/template.

        Raises:
            CredentialsFileExistError: if the file already exists on the host system.
        """
        if self._file_exists():
            raise CredentialsFileExistError

        self._parser.add_section('credentials')
        for cred in CREDENTIALS_DEFAULT:
            self._parser.set('credentials', cred, '')
        self._parser.write(open(self.cred_location, 'x'))
