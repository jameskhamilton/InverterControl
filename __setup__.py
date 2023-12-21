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
submitList = [('Submit',1),('Cancel',1)]
choiceList = [('Yes',1),('No',1)]

overwritePrompt = lambda text: f'Do you want to overwrite the existing {text} credentials?'

def windowPrompt(labelValue, buttonValue, directoryFolder, inverterFile, sourceName, textValue):
    userInputWindow = UserInputWindow(labelValue, buttonValue, directoryFolder, inverterFile, sourceName, textValue)
    result = userInputWindow.run()

    return result

#check for inverter credentials
sourceName = 'Inverter'
if credentialFile(directoryFolder, inverterFile):
    resultChoice = windowPrompt(None, choiceList, None, None, sourceName, overwritePrompt(sourceName))

if ( not credentialFile(directoryFolder, inverterFile) ) or resultChoice == 'Yes':
    resultInput = windowPrompt(inverterLabels, submitList, directoryFolder, inverterFile, sourceName, None)

#check for octopus credentials
sourceName = 'Octopus'
if credentialFile(directoryFolder, octopusFile):
    resultChoice = windowPrompt(None, choiceList, None, None, sourceName, overwritePrompt(sourceName))
    
if ( not credentialFile(directoryFolder, octopusFile) ) or resultChoice == 'Yes':
    resultInput = windowPrompt(octopusLabels, submitList, directoryFolder, octopusFile, sourceName, None)
