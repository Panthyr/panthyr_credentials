===============================
Credentials example code
===============================


Creating an empty credentials file
===================================

.. code:: python

    >>> from panthyr_credentials.p_credentials import pCredentials
    # add cred_location for non-default location
    >>> cred = pCredentials(cred_location = './credentials_file')
    >>> cred.create_empty()


Reading from an existing credentials file
==========================================

.. code:: python

    >>> from panthyr_credentials.p_credentials import pCredentials
    >>> cred = pCredentials(cred_location = './credentials_file')
    >>> cred.get_all()
    {'ftp_server': 'ftp.server.com', 'ftp_user': 'ftp_username'}
    >>> cred.get('ftp_user')
    'ftp_username'
