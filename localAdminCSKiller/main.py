from falconpy import RealTimeResponse, RealTimeResponseAdmin
import os
import pandas as pd

global rtrAdmin
global rtr
global device
global user
global aid
global df
#CSV Processing Code
def loadCSV(csv1):
    # Read CSV's -> DataFrames
    df = pd.read_csv(csv1)
    return df
       
# Crowdstrike RTR Admin API Code
def createRtrAdminApiSession():
    """Create a session with the Crowdstrike RTR Admin API."""
    try: 
        cid = os.environ["FALCON_CLIENT_ID"]
        csec = os.environ["FALCON_CLIENT_SECRET"]
        rtrAdmin = RealTimeResponseAdmin(client_id=cid, client_secret=csec)
        rtr = RealTimeResponse(client_id=cid, client_secret=csec)
        print("API Session created successfully")
        return rtrAdmin
    except:
        print("Error creating RTR Admin API session!")
        return False
def getScripts(lRtrAdmin, id):
    try:
        script = lRtrAdmin.RTR_GetScriptsV2(id)
        print(script)
        return script
    except Exception as e:
        print("Error getting scripts!")
        print(e)
        return False        
def listScripts(lRtrAdmin):
    try:
        response = lRtrAdmin.RTR_ListScripts(limit=10)
        print(response)
        return response
    except Exception as e:
        print("Error listing scripts!")
        print(e)
        return False    
def loadScripts(lRtrAdmin):
    """Load scripts from the Crowdstrike API."""
    print("Loading scripts...")
    try:
        idList = "ID1,ID2,ID3"
        scripts = lRtrAdmin.RTR_GetScriptsV2(ids=idList)
        print(scripts)
        return scripts
    except Exception as e:
        print("Error loading scripts!")
        print(e)
        return False
# Crowdstrike RTR API Code
def createRtrApiSession():
    """Create a session with the Crowdstrike RTR API."""
    try: 
        print("Initializing API Admin Session...")
        cid = os.environ["FALCON_CLIENT_ID"]
        csec = os.environ["FALCON_CLIENT_SECRET"]
        rtr = RealTimeResponse(client_id=cid, client_secret=csec)
        print("API Session created successfully")
        return rtr
    except:
        print("Error creating RTR API session!")
        return False    
def loadAid(lRtr):
    try:
        aid = lRtr.query_devices_by_filter(filter=f"hostname:'{device}*'")["body"]["resources"][0]
        return aid["aid"]
    except:
        print(f"Error loading Machine AID for machine: {device}")
        return False    
def initSession(lRtr, lDeviceID):
    try:
        print(f"Connecting to {lDeviceID}")
        lRtr.RTR_InitSession(lDeviceID)
    except Exception as e:
        print("Error Connecting to Device!")
        print(e)
        return False
def removeAdmin(lRtr, lUser, lDevice):
    """Removes Local Admin Account Using Crowdstrike RTR Command: Args: RTR Admin API Key, User to Disable, Device to Access"""
    try:
        print(f"Removing {lUser} from Local Admin on {lDevice}")
        lRtr.RTR_ExecuteCommand(base_command=f'runscript -CloudFile="Remove-LocalAdmin" -CommandLine="-user {lUser}"')
        print(f"User: {lUser} removed from Local Admin on {lDevice} Successfully")
    except Exception as e:
        print("Error Removing Local Admin!")
        print(e)
        return False
    
def main():
    print("Welcome to the Crowdstrike Local Admin Removal Tool")
    csvPath = input("Enter the path of the first CSV: ")
    loadCSV(csvPath)
    rtr = createRtrApiSession()
    #rtrAdmin = createRtrAdminApiSession()
    #listScripts(rtrAdmin)
    #loadScripts(rtr)
    #getScripts(rtrAdmin)
    for index, row in df.iterrows():
        user = row['USERNAME']
        device = row['DEVICE']
        status = row['STATUS']
        action = row['ACTION']
        loadAid(device)
        initSession(rtr, aid)
        confBool = input("Would you like to remove? (t/n): ")
        if confBool == "t":
            removeAdmin(rtr, user, device)
            confBool = "n"
        else:
            return
        bool = input("Would you like to continue? (t/n): ")
        if bool == "t":
            print("Continuing...")
        else:
            return
    
    
    

if __name__ == "__main__":
    main()