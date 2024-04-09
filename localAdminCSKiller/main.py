from falconpy import RealTimeResponse, RealTimeResponseAdmin, Hosts
import os
import pandas as pd
import re

def readCsv(lCsv):
    """Read's input csv"""
    try:
        df = pd.read_csv(lCsv)
        return df
    except Exception as e:
        print(f"Error reading CSV!\n{e}")
        return False
# Crowdstrike RTR API Code
def createRtrApiSession():
    """Create a session with the Crowdstrike RTR API."""
    try: 
        print("Initializing API RTR Session...")
        cid = os.environ["FALCON_CLIENT_ID"]
        csec = os.environ["FALCON_CLIENT_SECRET"]
        rtr = RealTimeResponse(client_id=cid, client_secret=csec)
        print("API Session created successfully")
        return rtr
    except:
        print("Error creating RTR API session!")
        return False 
def createHostApiSession():
    """Create a session with the Crowdstrike HOST API."""
    try: 
        print("Initializing API Host Session...")
        cid = os.environ["FALCON_CLIENT_ID"]
        csec = os.environ["FALCON_CLIENT_SECRET"]
        host = Hosts(client_id=cid, client_secret=csec)
        print("API Session created successfully")
        return host
    except:
        print("Error creating RTR API session!")
        return False       
def loadAid(host, lDevice):
    """
    Retrieves the AID for a given hostname
    """
    print("Retrieving AID for target host...")
    result = host.QueryDevicesByFilter(                     
        filter=f"hostname:'{lDevice}*'"                                
        )
    if result["status_code"] == 200:
        if len(result["body"]["resources"]) == 0:                   
            print("ERROR getting aid skipping!")
        else:
            returned = result["body"]["resources"][0]
            print(f"AID Retrival Succesful: {returned}")
    else:
        returned = False

    return returned
def initSession(lRtr, lDevice, lDeviceID):
    try:
        print(f"Connecting to: {lDeviceID}")
        session_init = lRtr.init_session(device_id=lDeviceID, queue_offline=False)
        if session_init["status_code"] != 201:
            # RTR session connection failure.
            print(f"Unable to open RTR session with {lDevice} [{lDeviceID}]")
            return False
        else:
            session_id = session_init["body"]["resources"][0]["session_id"]
            print("Connection Successful!")
            return session_id
    except Exception as e:
        print("Error Connecting to Device!")
        print(e)
        return False
def delete_session(lRtr, lSession):
    """
    Deletes the RTR session as specified by session ID
    """
    print("Deleting session...")
    lRtr.delete_session(session_id=lSession)
    print("Cleanup complete!")   
def removeAdmin(lRtr, lUser, lDevice, lSession):
    """Removes Local Admin Account Using Crowdstrike RTR Command: Args: RTR Admin API Key, User to Disable, Device to Access"""
    try:
        print(f"Removing {lUser} from Local Admin on {lDevice}")
        command_string=f'runscript -CloudFile="Remove-LocalAdmin" -CommandLine="-user {lUser}"'
        result = lRtr.RTR_ExecuteActiveResponderCommand(base_command='runscript', command_string=command_string, persist=True, session_id=lSession)
        if result["status_code"] != 201:
            # RTR session connection failure.
            print(f"Unable to remove {lUser} from Local Admin on {lDevice}")
        else:
            print(f"User: {lUser} removed from Local Admin on {lDevice} Successfully")
    except Exception as e:
        print("Error Removing Local Admin!")
        print(e)
        return False
    
def main():
    print("Welcome to the Crowdstrike Local Admin Removal Tool! \nThis tool is designed to take in a list of users and machine names and remove the user's local AD account from Local Admin.")
    csvPath = input("Enter the path of the Targets CSV: ")
    
    rtr = createRtrApiSession()
    host = createHostApiSession()
    df = readCsv(csvPath)
    autocycle = input("Would you like to automatically cycle through the list? (t/n): ")
    if autocycle == "t":
        print("Automating the list...")
        confBool = "t"
    else:
        confBool = "n"
        print("Manual Mode Engaged...")
    for index, row in df.iterrows():
        i = 0
        user = row['USERNAME']
        device = row['DEVICE']
        status = row['STATUS']
        action = row['ACTION']
        takeAct = df['ACTION'].to_string()
        takeAct = re.findall("REMOVE|PASS", takeAct)
        takeAct = takeAct[0]
        if takeAct == "REMOVE":
            try:
                aid = loadAid(host, device)
            except Exception as e:
                print("ERROR loading AID!")
                df['STATUS']= 'ERROR1'
            try:
                session = initSession(rtr, device, aid)
            except Exception as e:
                print("ERROR init session!")
                df['STATUS']= 'ERROR2'
                
            if autocycle == "t":
                print(f"Auto-processing Account #{i}")
            else:
                confBool = input(f"Would you like to remove {user} from LocalAdmin on {device}? (t/n): ")
                
            if confBool == "t":
                try:
                    removeAdmin(rtr, user, device, session)
                    df['STATUS'] = 'SUCCESS'
                except:
                    print("ERROR!")
                    df['STATUS']= 'ERROR'
                
                delete_session(rtr, session)
                if autocycle == "t":
                    confBool = "t"
                else:
                    confBool = "n"
            else:
                print("Error not confirmed. Exiting Program")
        elif takeAct == "PASS":
            print(f"Passing on User: {user} Device: {device}")
            return
        else:
            print(f"Passing on User: {user} Device: {device} due to empty ACTION field! Please fill in csv with either REMOVE or PASS.")
            print("Continuing...")
        i =+ i
    print("Program Complete... Outputting Results!")
    df.to_csv("./result.csv")
if __name__ == "__main__":
    main()