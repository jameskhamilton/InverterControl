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
octopusFile = 'octopus_config1.json'
inverterLabels = ['Key Id', 'Secret Key', 'Username', 'Password', 'Inverter SN', 'Inverter Id', 'Station Id']
octopusLabels = ['API Key', 'Account Number']
submitList = [('Submit',1)]
choiceList = [('Yes',1),('No',1)]

#check for inverter credentials
if credentialFile(directoryFolder, inverterFile):
    sourceName = 'Inverter'
    buttonValue = choiceList
    userInputWindow = UserInputWindow(None, buttonValue, directoryFolder, inverterFile, sourceName)
    result = userInputWindow.run()
elif not credentialFile(directoryFolder, inverterFile):
    sourceName = 'Inverter'
    buttonValue = submitList
    userInputWindow = UserInputWindow(inverterLabels, buttonValue, directoryFolder, inverterFile, sourceName)
    result = userInputWindow.run()

    print(result)

#check for octopus credentials
if not credentialFile(directoryFolder, octopusFile):
    sourceName = 'Octopus'
    buttonValue = submitList
    userInputWindow = UserInputWindow(octopusLabels, buttonValue, directoryFolder, octopusFile, sourceName)
    result = userInputWindow.run()

    print(result)