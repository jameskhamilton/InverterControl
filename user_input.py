import tkinter as tk
from tkinter import ttk
import json
import os

def saveToJSON(data: json, directoryFolder: str, filename: str) -> None:
    """
    Parameters:
    - json result from the user input
    - directory folder name
    - filename for the save file

    Result:
    - save / overwrite file
    """
    os.makedirs(directoryFolder, exist_ok=True)

    filepath = os.path.join(directoryFolder, filename)

    with open(filepath, 'w') as jsonFile:
        json.dump(data, jsonFile, indent=2)

class DynamicInputEntry:
    def __init__(self, labelValue: str, row: int, column: int, root) -> None:
        """
        Defines the style for the user input fields
        """
        self.style = ttk.Style()
        self.style.configure("InputLabel.TLabel")
        self.label = ttk.Label(root, text=labelValue, style="InputLabel.TLabel", background="#f0f0f0", anchor="n")
        self.label.grid(row=row, column=column, padx=2, pady=2, sticky="n")

        self.style.configure("InputEntry.TEntry")
        self.entry = ttk.Entry(root, style="InputEntry.TEntry")
        self.entry.grid(row=row, column=column + 1, padx=2, pady=2, sticky="n")

    def getInputLabel(self):
        return self.entry.get()

class UserInputWindow:
    def __init__(self, labelList: str, directoryFolder: str, fileName: str, sourceName: str) -> None:
        """
        Build the user input window with all required fields and submit button
        """
        self.root = tk.Tk()
        self.root.title(f"{sourceName} Credentials Input")
        self.root.geometry("400x200")
        self.root.configure(bg="#f0f0f0")

        self.labelList = labelList
        self.directoryFolder = directoryFolder
        self.fileName = fileName
        self.createDynamicInputFields()

        submitButton = ttk.Button(self.root, text="Submit", command=self.submitInput)
        submitButton.grid(row=len(labelList) + 1, column=0, columnspan=2, pady=10, sticky="s")

        #Ensure that the columns and rows in the grid are configured to expand or shrink when the window is resized.
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        for i in range(len(labelList) + 1):
            self.root.rowconfigure(i, weight=1)

    def createDynamicInputFields(self) -> None:
        """
        Create a fields based off the input list
        """
        self.dynamicEntries = []

        for i, labelValue in enumerate(self.labelList, start=1):
            dynamicEntry = DynamicInputEntry(labelValue, i, 0, self.root)
            self.dynamicEntries.append(dynamicEntry)

    def submitInput(self) -> None:
        """
        Defines how the submit button works
        """
        data = {entry.label.cget("text"): entry.getInputLabel() for entry in self.dynamicEntries}
        saveToJSON(data, self.directoryFolder, self.fileName)

        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    labels = ["Test", "Test", "Test", "Test"]  # Customize your list of labels
    directoryFolder = "credentials"
    outputFilename = "creds.json"  # Customize your output filename
    sourceName = "Octopus"
    userInputWindow = UserInputWindow(labels, directoryFolder, outputFilename, sourceName)
    userInputWindow.run()
