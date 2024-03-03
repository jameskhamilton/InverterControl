import pyodbc
import inverter_functions as sf
import octopus_functions as of
from datetime import datetime

database = 'marvin'
server = 'tinyserver.database.windows.net'
timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]

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
        connectionString = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={user};PWD={password}'
        connection = pyodbc.connect(connectionString)
    
    except Exception as e:
        print(f"Octopus database connection failed: {e}") 
        return None    

    cursor = connection.cursor()

    sqlInsert = f"INSERT INTO OCTOPUS_PRICES VALUES ('{timestamp}', ?, ?, ?, ?)"

    try:
        for dict in octopusDatasetValue:

            values = [
                    dict['priceExclVAT'],
                    dict['priceInclVAT'],
                    dict['fromDateTime'],
                    dict['toDateTime']
                ]
            
            cursor.execute(sqlInsert, values)
            connection.commit()

    except Exception as e:
        print(f"Octopus database insert failed: {e}")  

    cursor.close()
    connection.close()

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
        connectionString = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={user};PWD={password}'
        connection = pyodbc.connect(connectionString)
    
    except Exception as e:
        print(f"Inverter database connection failed: {e}") 
        return None

    # Construct SQL INSERT statement
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

            cursor.execute(sqlInsert, values)
            connection.commit()

    except Exception as e:
        print(f"Inverter database insert failed: {e}")  

    cursor.close()
    connection.close()