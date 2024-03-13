from falconpy import RealTimeResponse
import os
import pandas as pd

#CSV Processing Code
def loadCSV(csv1):
    # Read CSV's -> DataFrames
    df = pd.read_csv(csv1)
    parseDf(df)
    return df
def parseDf(df):
    for index, row in df.iterrows():
        name = row['USERNAME']
        device = row['DEVICE']
        status = row['STATUS']
        action = row['ACTION']
        bool = input("Would you like to continue? (x/z): ")
        if bool == "x":
            print("Continuing...")
        else:
            return
        
# Crowdstrike API Code
def createApiSession(lFalcon):
    """Create a session with the Crowdstrike API."""
    print("Initializing API Session...")
    try: 
        cid = os.environ["FALCON_CLIENT_ID"]
        csec = os.environ["FALCON_CLIENT_SECRET"]
        lFalcon = RealTimeResponse(client_id=cid, client_secret=csec)
        print("API Session created successfully")
        return lFalcon
    except:
        print("Error creating API session!")
        return False

def loadScripts(lFalcon):
    """Load scripts from the Crowdstrike API."""
    print("Loading scripts...")
    try:
        idList = "ID1,ID2,ID3"
        scripts = lFalcon.RTR_GetScriptsV2(ids=idList)
    except:
        print("Error loading scripts!")
        return False
    
def loadAid():
    try:
        aid = falcon.puery_devices_by_filter(filter=f"hostname:'{device}*'")["body"]["resources"][0]
        return aid["aid"]
    except:
        print(f"Error loading Machine AID for machine: {device}")
        return False
    
def main():
    print("Welcome to the Crowdstrike Local Admin Removal Tool")
    global falcon
    global device
    createApiSession(falcon)
    loadScripts(falcon)

if __name__ == "__main__":
    main()