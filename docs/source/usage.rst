===============================
Credentials example code
===============================


Creating an empty credentials file
===================================

.. code:: python

    >>> from panthyr_credentials.credentials import Credentials
    >>> cred = Credentials(cred_location = './credentials_file')
    >>> cred.create_empty()


Reading from an existing credentials file
==========================================

.. code:: python

    >>> from panthyr_credentials.credentials import Credentials
    >>> cred = Credentials(cred_location = './credentials_file')
    >>> cred.get_all()
    {'ftp_server': 'ftp.server.com', 'ftp_user': 'ftp_username'}
    >>> cred.get('ftp_user')
    'ftp_username'
