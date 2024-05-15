#!/usr/bin/env python

import sys
import pyodbc

sys.path.insert(0, '/users/prieappatom/')
from secureconfig import *

def find_teradata_driver():
    """Find the highest version Teradata driver installed on the system."""
    drivers = pyodbc.drivers()
    teradata_drivers = [driver for driver in drivers if 'teradata' in driver.lower()]
    if not teradata_drivers:
        raise ValueError("No Teradata driver found on this system.")
    
    # Assuming that the driver names include version numbers that can be sorted
    # Example naming: 'Teradata ODBC Driver 16.20', 'Teradata ODBC Driver 16.10'
    teradata_drivers.sort(key=lambda name: [int(x) if x.isdigit() else x for x in name.replace('Teradata ODBC Driver ', '').split('.')], reverse=True)
    return teradata_drivers[0]  # Returns the highest version Teradata driver

def connect_to_teradata():
    uid, pwd = decrypt_credential('SecureConfig_PREU.ini'.format(src))

    driver = find_teradata_driver()  # Find the highest version Teradata driver
    TERADATA_CON = pyodbc.connect(
        f'DRIVER={{{driver}}};DBCNAME=dsn-sysa.rg.rbc.com;UID={uid};PWD={pwd};QUIETMODE=YES;',
        autocommit=True
    )
    TERADATA_CON.setencoding(pyodbc.SQL_CHAR, encoding='latin-1')
    TERADATA_CON.setencoding(pyodbc.SQL_WCHAR, encoding='latin-1')
    TERADATA_CON.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-16le')

    return TERADATA_CON
