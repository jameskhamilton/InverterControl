import pyodbc
import logging
from libraries import inverter_functions as sf
from libraries import octopus_functions as of
from datetime import datetime

database = 'marvin'
server = 'tinyserver.database.windows.net'

def octopusInsert(octopusDatasetValue: list) -> None:
    """
    Parameters:
    - list from the octopus dataset call

    Purpose:
    - insert the values into the database
    """

    user = 'octopusWriter'
    password = of.secrets()[0]

    try:
        connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={user};PWD={password}'
        connection = pyodbc.connect(connectionString)
    
    except Exception as e:
        print(f"Octopus database connection failed: {e}") 
        logging.error(e)
        return None    

    cursor = connection.cursor()

    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
    sqlInsert = f"INSERT INTO OCTOPUS_PRICES VALUES ('{timestamp}', ?, ?, ?, ?)"

    try:
        for dict in octopusDatasetValue:

            values = [
                    dict['priceExclVAT'],
                    dict['priceInclVAT'],
                    dict['fromDateTime'],
                    dict['toDateTime']
                ]
            
            #make sure the value hasn't already been inserted
            checkQuery = "SELECT 1 FROM OCTOPUS_PRICES WHERE [Datetime From] = ?"
            cursor.execute(checkQuery, (dict['fromDateTime'],))
            result = cursor.fetchone()
            
            if not result:
                cursor.execute(sqlInsert, values)
                connection.commit()

            cursor.close()
            connection.close()

    except Exception as e:
        print(f"Octopus database insert failed: {e}") 
        logging.error(e)

def inverterInsert(inverterDatasetValue: list) -> None:
    """
    Parameters:
    - list from the inverter dataset call

    Purpose:
    - insert the values into the database
    """

    user = 'inverterWriter'
    password = sf.secrets()[3]

    try:
        connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={user};PWD={password}'
        connection = pyodbc.connect(connectionString)
    
    except Exception as e:
        print(f"Inverter database connection failed: {e}") 
        logging.error(e)
        return None

    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
    sqlInsert = f"INSERT INTO INVERTER_STATE VALUES ('{timestamp}', ?, ?, ?, ?, ?, ?)"

    try:
        cursor = connection.cursor()

        for dict in inverterDatasetValue:

            values = [
                    dict['Data Timestamp'],
                    dict['SoC'],
                    dict['Battery Discharge KwH'],
                    dict['PV Yield KwH'],
                    dict['Grid Usage KwH'],
                    dict['House Load KwH']
                ]
            
            #make sure the value hasn't already been inserted
            checkQuery = "SELECT 1 FROM INVERTER_STATE WHERE [Data Timestamp] = ?"
            cursor.execute(checkQuery, (dict['Data Timestamp'],))
            result = cursor.fetchone()

            if not result:
                cursor.execute(sqlInsert, values)
                connection.commit()

            cursor.close()
            connection.close()

    except Exception as e:
        print(f"Inverter database insert failed: {e}")  
        logging.error(e)

