import tkinter as tk
from tkinter import ttk
import json
import os

def saveToJSON(dataValue: json, directoryFolderValue: str, filenameValue: str) -> None:
    """
    Parameters:
    - json result from the user input
    - directory folder name
    - filename for the save file

    Result:
    - save / overwrite file
    """
    os.makedirs(directoryFolderValue, exist_ok=True)

    filepath = os.path.join(directoryFolderValue, filenameValue)

    with open(filepath, 'w') as jsonFile:
        json.dump(dataValue, jsonFile, indent=2)

class DynamicInputEntry:
    def __init__(self, root, labelValue: str, columnValue: int, rowValue: int) -> None:
        """
        Defines the style for the user input fields
        """
        self.style = ttk.Style()
        self.style.configure("InputLabel.TLabel")
        self.label = ttk.Label(root, text=labelValue, style="InputLabel.TLabel", background="#f0f0f0", anchor="n")
        self.label.grid(row=rowValue, column=columnValue, padx=2, pady=2, sticky="n")

        self.style.configure("InputEntry.TEntry")
        self.entry = ttk.Entry(root, style="InputEntry.TEntry")
        self.entry.grid(row=rowValue, column=columnValue + 1, padx=2, pady=2, sticky="n")

    def getInputLabel(self):
        return self.entry.get()
    
class DynamicButtonEntry:
    def __init__(self, root, window, buttonValue: str, columnValue: int, rowValue: int, callbackValue=None) -> None:
        """
        Defines the style and action of buttons
        """
        self.root = root
        self.window = window
        self.callback = callbackValue
        self.buttonValue = buttonValue

        if buttonValue == 'Submit':
            self.button = ttk.Button(root, text=buttonValue, width = 15, command=self.submitInput)
        else:
            self.button = ttk.Button(root, text=buttonValue, width = 15, command=self.defaultInput)
<<<<<<< HEAD

        self.button.grid(row=rowValue, column=columnValue, columnspan=1, padx=10, pady=10, sticky="s")

    def submitInput(self) -> str:
        """
        Bundles the data points to be saved to file, returns a string to confirm Submitted, then closes the window
        """
=======
        self.button.grid(row=rowValue, column=columnValue, columnspan=1, padx=10, pady=10, sticky="s")

    def submitInput(self) -> None:
>>>>>>> f76ac54b76717a50c47ceb68e836175f1323d7bb
        data = {entry.label.cget("text"): entry.getInputLabel() for entry in self.window.dynamicEntries}
        saveToJSON(data, self.window.directoryFolder, self.window.fileName)
        self.window.result = 'Submitted'
        self.root.destroy()

<<<<<<< HEAD
    def defaultInput(self) -> str:
        """
        Returns a string with the button text, then closes the window
        """        
=======
    def defaultInput(self) -> None:
>>>>>>> f76ac54b76717a50c47ceb68e836175f1323d7bb
        self.window.result = self.buttonValue
        self.root.destroy()

class UserInputWindow:
    def __init__(self, fieldListValue: list, buttonListValue: list, directoryFolderValue: str, fileNameValue: str, sourceNameValue: str, textValue: str = None) -> None:
        """
        Build the user input window with all required text, fields and buttons
        """
        self.root = tk.Tk()
        self.root.title(f"{sourceNameValue} Credentials Input")
        self.root.geometry("400x200")
        self.root.configure(bg="#f0f0f0")

        self.fields = 0
        self.width = 0
        self.fieldList = fieldListValue
        self.buttonList = buttonListValue
        self.directoryFolder = directoryFolderValue
        self.fileName = fileNameValue
        self.text = textValue

        self.result = None
        
        #handles no values passed
        if self.text:
            self.addText(self.text, 1, 0)
        if self.fieldList:
            self.fields = self.createDynamicInputFields()
        if self.buttonList:
            self.width = self.createDynamicButtons()

        #Ensure that the columns and rows in the grid are configured to expand or shrink when the window is resized.
        self.root.columnconfigure(0, weight=1)
        for i in (range (self.width + 1)):
            self.root.columnconfigure(i, weight=1)
        self.root.rowconfigure(0, weight=1)
        for i in range(self.fields + 1):
            self.root.rowconfigure(i, weight=1)

    def createDynamicInputFields(self) -> int:
        """
        Purpose:
        - Create fields based off the input list

        Returns:
        - number of fields in the list
        """
        self.dynamicEntries = []

        for y, labelValue in enumerate(self.fieldList, start=1):
            dynamicEntry = DynamicInputEntry(self.root, labelValue, 1, y)
            self.dynamicEntries.append(dynamicEntry)

        return len(self.fieldList)

    def createDynamicButtons(self) -> int:
        """
        Purpose:
        - Create buttons based off the input list
<<<<<<< HEAD
=======

        Returns:
        - the width of the button list
        """
        self.dynamicButtons = []
        lasty = 0
        x = 1

        for (buttonValue, y) in self.buttonList:

            #reset the columns for a new row
            if lasty < y:
                x = 1
            
            dynamicButton = DynamicButtonEntry(self.root, self, buttonValue, x, y + self.fields)
            self.dynamicButtons.append(dynamicButton)
            #center the button in the column
            self.root.grid_columnconfigure(x, weight=1)

            x += 1
            lasty = y

        return x
    
    def addText(self, textValue, columnValue, rowValue):
        """
        Add text to the window.
        """
        label = ttk.Label(self.root, text=textValue, background="#f0f0f0")
        label.grid(row=rowValue, column=columnValue, columnspan=2, padx=10, pady=10)    
>>>>>>> f76ac54b76717a50c47ceb68e836175f1323d7bb

        Returns:
        - the width of the button list
        """
        self.dynamicButtons = []
        lasty = 0
        x = 1

        for (buttonValue, y) in self.buttonList:

            #reset the columns for a new row
            if lasty < y:
                x = 1
            
            dynamicButton = DynamicButtonEntry(self.root, self, buttonValue, x, y + self.fields)
            self.dynamicButtons.append(dynamicButton)
            #center the button in the column
            self.root.grid_columnconfigure(x, weight=1)

            x += 1
            lasty = y

        return x
    
    def addText(self, textValue, columnValue, rowValue):
        """
        Add text in the first lines of the window
        """
        label = ttk.Label(self.root, text=textValue, background="#f0f0f0")
        label.grid(row=rowValue, column=columnValue, columnspan=2, padx=10, pady=10)    

    def run(self) -> str:
        """
        Initiate the window, returns the result from button clicks in DynamicButtonEntry class
        """        
        self.root.mainloop()
        return self.result

if __name__ == "__main__":
    labels = ["Password", "Username"]  # Customize your list of labels
    buttons = [("Submit",1),("Cancel",1)]
    directoryFolder = "credentials"
    outputFilename = "creds2.json"  # Customize your output filename
    sourceName = "Octopus"
    textValue = 'Do you want to overwrite the existing credentials?'
    userInputWindow = UserInputWindow(labels, buttons, directoryFolder, outputFilename, sourceName, textValue)
    result = userInputWindow.run()

    print(result)