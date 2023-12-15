import inverter_functions as inf
import octopus_functions as of
from user_input import UserInputWindow
import os

def credentialFile(directoryFolder: str, filename: str) -> bool:
    """
    Check that the credential file exists
    """
    scriptDirectory = os.path.dirname(os.path.abspath(__file__))
    filePath = os.path.join(scriptDirectory,directoryFolder, filename)
    return os.path.exists(filePath)

directoryFolder = 'credentials'
inverterFile = 'inverter_config.json'
octopusFile = 'octopus_config.json'
inverterLabels = ['Key Id', 'Secret Key', 'Username', 'Password', 'Inverter SN', 'Inverter Id', 'Station Id']
octopusLabels = ['API Key', 'Account Number']

#check for inverter credentials
if not credentialFile(directoryFolder, inverterFile):
    sourceName = 'Inverter'
    userInputWindow = UserInputWindow(inverterLabels, directoryFolder, inverterFile, sourceName)
    userInputWindow.run()

#check for octopus credentials
if not credentialFile(directoryFolder, octopusFile):
    sourceName = 'Octopus'
    userInputWindow = UserInputWindow(octopusLabels, directoryFolder, octopusFile, sourceName)
    userInputWindow.run()