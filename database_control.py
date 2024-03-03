import pyodbc
import json
import inverter_functions as sf

def inverterInsert(inverterDatasetValue: list) -> None:
    """
    Parameters:
    - list from the inverter dataset call

    Purpose:
    - insert the values into the database
    """

    password = sf.secrets()[3]

    # Establish a connection to SQL Server
    try:
        connection_string = f'DRIVER={{SQL Server}};SERVER=tinyserver.database.windows.net;DATABASE=marvin;UID=inverterWriter;PWD={password}'
        connection = pyodbc.connect(connection_string)

    except Exception as e:
        print(f"Database connection failed: {str(e)}")    

    # Construct SQL INSERT statement
    sqlInsert = "INSERT INTO INVERTER_STATE VALUES (GETDATE(), ?, ?, ?, ?, ?, ?)"

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
        print(f"Database insert failed: {str(e)}")  

    # Close cursor and connection
    cursor.close()
    connection.close()