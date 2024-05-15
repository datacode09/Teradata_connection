#!/usr/bin/env python

import sys
import pyodbc

sys.path.insert(0, '/users/prieappatom/')
from secureconfig import *

def find_teradata_driver():
    """Find a Teradata driver installed on the system."""
    drivers = pyodbc.drivers()
    teradata_drivers = [driver for driver in drivers if 'teradata' in driver.lower()]
    if not teradata_drivers:
        raise ValueError("No Teradata driver found on this system.")
    return teradata_drivers[0]  # Returns the first matching Teradata driver

def connect_to_teradata():
    uid, pwd = decrypt_credential('SecureConfig_PREU.ini'.format(src))

    driver = find_teradata_driver()  # Find the appropriate Teradata driver
    TERADATA_CON = pyodbc.connect(
        f'DRIVER={{{driver}}};DBCNAME=dsn-sysa.rg.rbc.com;UID={uid};PWD={pwd};QUIETMODE=YES;',
        autocommit=True
    )
    TERADATA_CON.setencoding(pyodbc.SQL_CHAR, encoding='latin-1')
    TERADATA_CON.setencoding(pyodbc.SQL_WCHAR, encoding='latin-1')
    TERADATA_CON.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-16le')

    return TERADATA_CON
