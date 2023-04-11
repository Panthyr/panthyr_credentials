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
    >>> # Then populate/complete the credentials file

Example credentials file
====================================

Example of a basic credentials file, only containing the default fields.
More field can be added if necessary.

.. code::

    [credentials]
    email_user=panthyr@example.com
    email_password=Very_Secret
    email_server_port=smtp.example.com:587
    ftp_server=ftp.example.com
    ftp_user=panthyr
    ftp_password=AlsoVerySecret

Reading from an existing credentials file
==========================================

.. code:: python

    >>> from panthyr_credentials.p_credentials import pCredentials
    >>> cred = pCredentials(cred_location = './credentials_file')
    >>> cred.get_all()
    {'ftp_server': 'ftp.server.com', 'ftp_user': 'ftp_username'}
    >>> cred.get_cred('ftp_user')
    'ftp_username'
    # Externally changed the credentials file, so first reparse:
    >>> cred.parse()
    >>> cred.get_cred('ftp_user')
    'new_ftp_username'

