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
    def __init__(self, labelValue: str, columnValue: int, rowValue: int, root) -> None:
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
    def __init__(self, buttonValue: str, columnValue: int, rowValue: int, root) -> None:
        """
        Defines the style and action of buttons
        """
        submitButton = ttk.Button(root, text=buttonValue, width = 150, command=self.submitInput)
        submitButton.grid(row=rowValue, column=columnValue, columnspan=1, padx=10, pady=10, sticky="s")

    def submitInput(self) -> None:
        """
        Defines how the submit button works
        """
        data = {entry.label.cget("text"): entry.getInputLabel() for entry in self.dynamicEntries}
        saveToJSON(data, self.directoryFolder, self.fileName)

        self.root.destroy()

class UserInputWindow:
    def __init__(self, fieldListValue: list, directoryFolderValue: str, fileNameValue: str, sourceNameValue: str) -> None:
        """
        Build the user input window with all required fields and submit button
        """
        self.root = tk.Tk()
        self.root.title(f"{sourceNameValue} Credentials Input")
        self.root.geometry("400x200")
        self.root.configure(bg="#f0f0f0")

        self.fields = 0
        self.fieldList = fieldListValue
        self.directoryFolder = directoryFolderValue
        self.fileName = fileNameValue
        self.buttonList = [("Yes",1),("No",1),("Nsdfsfsdfsdfsdfsfsdfsdfsdfsdfsdfsdfsdfo",2),("No",2),("No",3),("No",3),("No",3)]

        #handles no fields
        if self.fieldList:
            self.fields = self.createDynamicInputFields()

        self.createDynamicButtons()
        #submitButton = ttk.Button(self.root, text="Submit", command=self.submitInput)
        #submitButton.grid(row=self.fields + 1, column=0, columnspan=2, pady=10, sticky="s")

        #Ensure that the columns and rows in the grid are configured to expand or shrink when the window is resized.
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
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
            dynamicEntry = DynamicInputEntry(labelValue, 0, y, self.root)
            self.dynamicEntries.append(dynamicEntry)

        return len(self.fieldList)

    def createDynamicButtons(self) -> int:
        """
        Purpose:
        - Create buttons based off the input list

        Returns:
        - array that was passed with the buttons to determine x, y
        """
        self.dynamicButtons = []
        lasty = 0
        x = 1
        for (buttonValue, y) in self.buttonList:
            #reset the columns for a new row
            if lasty < y:
                x = 1
            dynamicButton = DynamicButtonEntry(buttonValue, x, y, self.root)
            self.dynamicButtons.append(dynamicButton)
            #center the button in the column
            self.root.grid_columnconfigure(x, weight=1)

            x += 1
            lasty = y

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    labels = None# [""]  # Customize your list of labels
    directoryFolder = "credentials"
    outputFilename = "creds.json"  # Customize your output filename
    sourceName = "Octopus"
    userInputWindow = UserInputWindow(labels, directoryFolder, outputFilename, sourceName)
    userInputWindow.run()