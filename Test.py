#!/usr/bin/env python

import sys
import pyodbc
import configparser
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Assuming the configuration and credentials are stored in config.ini
def load_config(section):
    """Load configuration settings from a .ini file."""
    config = configparser.ConfigParser()
    config.read('/path/to/config.ini')  # Adjust the path to your config file
    return {key: value for key, value in config.items(section)}

def find_appropriate_driver():
    """Return the first available ODBC driver."""
    drivers = pyodbc.drivers()
    if not drivers:
        logging.error("No ODBC drivers found on this system.")
        raise ValueError("No ODBC drivers found on this system.")
    logging.info("Using ODBC driver: %s", drivers[0])
    return drivers[0]

def connect_to_database():
    """Establish a connection to a database."""
    try:
        config = load_config('Database')
        driver = find_appropriate_driver()
        connect_str = (
            f"DRIVER={{{driver}}};DBCNAME={config['dbcname']};UID={config['uid']};"
            f"PWD={config['pwd']};QUIETMODE=YES;"
        )
        db_connection = pyodbc.connect(connect_str, autocommit=True)
        db_connection.setencoding(pyodbc.SQL_CHAR, encoding='latin-1')
        db_connection.setencoding(pyodbc.SQL_WCHAR, encoding='latin-1')
        db_connection.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-16le')
        logging.info("Connected to the database successfully.")
        return db_connection
    except Exception as e:
        logging.error("Failed to connect to the database: %s", e)
        raise

# Usage example
if __name__ == "__main__":
    db_connection = connect_to_database()
    # Your database operations here
    # Ensure that you close the connection if not using with statement
    db_connection.close()
