import pandas as pd
import pyperclip
from PIL import Image
import io

global csvPath
name = "name"
device = "device"
subject = "FINAL NOTICE: Local Admin Account Remediation"
def copyToClipboard(name, device):
    pyperclip.copy(name)
    print(f"Name {name} has been copied to clipboard.")
    bool = input("Machine (x/z): ")
    if bool == "x":
        pyperclip.copy(device)
        print(f"Device {device} has been copied to clipboard.")  
    else:
        print("Skipping device...")
    bool2 = input("Subject (x/z): ")
    if bool2 == "x":
        pyperclip.copy(subject)
        print("Subject has been copied to clipboard.")
    else:
        print("Skipping subject...")
        
def loadCSV(csv1):
    # Read CSV's -> DataFrames
    df = pd.read_csv(csv1)
    parseDf(df)
    return df

def parseDf(df):
    for index, row in df.iterrows():
        name = row['USERNAME']
        device = row['DEVICE']
        copyToClipboard(name, device)
        #print(f"Email for {name} has been copied to clipboard.")
        bool = input("Would you like to continue? (x/z): ")
        if bool == "x":
            print("Continuing...")
        else:
            return
        
def main():
    print("Welcome to CSV Email. A tool to build emails in the clipboard from CSV's.")
    # Get Path Input
    csvPath = input("Enter the path of the first CSV: ")
    loadCSV(csvPath)
if __name__ == "__main__":
    main()