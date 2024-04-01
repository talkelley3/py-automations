from falconpy import RealTimeResponse, RealTimeResponseAdmin, Hosts
import os
import pandas as pd

#global rtrAdmin
#global rtr
#global device
#global user
#global aid

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
            raise SystemExit(
                    "%80s" % f"{' ' * 80}\nUnable to retrieve "
                    "AID for target.\n"                 
                    "Check target hostname value."
                )
        returned = result["body"]["resources"][0]
        print(f"Retrieving AID for target host ({returned})")
    else:
        returned = False

    return returned
def initSession(lRtr, lDevice, lDeviceID):
    try:
        print(f"Connecting to {lDeviceID}")
        session_init = lRtr.init_session(device_id=lDeviceID, queue_offline=False)
        if session_init["status_code"] != 201:
            # RTR session connection failure.
            print(f"Unable to open RTR session with {lDevice} [{lDeviceID}]")
        else:
            session_id = session_init["body"]["resources"][0]["session_id"]
    except Exception as e:
        print("Error Connecting to Device!")
        print(e)
        return False
    return session_id
def delete_session(lRtr, lSession):
    """
    Deletes the RTR session as specified by session ID
    """
    print("Deleting session...")
    lRtr.delete_session(session_id=lSession)                    # Delete our current RTR session
    print("Cleanup complete!")                                # Inform the user, we're done
def checkAdmin(lRtr, lSession, lDeviceID):
    """Checks to make sure the user exists as local admin on the machine using Crowdstrike RTR AC Command: RTR Admin API Key, User to Disable, Device to Access"""
    command_string = 'runscript -CloudFile="Get-LocalAdmin"'
    result = lRtr.RTR_ExecuteActiveResponderCommand(device_id=lDeviceID, session_id=lSession, base_command=f'runscript', command_string=command_string, persist=True)
    print(result)
def removeAdmin(lRtr, lUser, lDevice, lSession):
    """Removes Local Admin Account Using Crowdstrike RTR Command: Args: RTR Admin API Key, User to Disable, Device to Access"""
    try:
        print(f"Removing {lUser} from Local Admin on {lDevice}")
        command_string=f'runscript -CloudFile="Remove-LocalAdmin" -CommandLine="-user {lUser}"'
        result = lRtr.RTR_ExecuteActiveResponderCommand(base_command='runscript', command_string=command_string, persist=True, session_id=lSession)
        print(result)
        #write code to handle http status codes and throw error
        print(f"User: {lUser} removed from Local Admin on {lDevice} Successfully")
    except Exception as e:
        print("Error Removing Local Admin!")
        print(e)
        return False
    
def main():
    print("Welcome to the Crowdstrike Local Admin Removal Tool! \nThis tool is designed to take in a list of users and machine names and remove the user's local AD account from Local Admin.")
    csvPath = input("Enter the path of the first CSV: ")
    rtr = createRtrApiSession()
    host = createHostApiSession()
    df = pd.read_csv(csvPath)
    for index, row in df.iterrows():
        i = 1
        user = row['USERNAME']
        device = row['DEVICE']
        status = row['STATUS']
        action = row['ACTION']
        aid = loadAid(host, device)
        session = initSession(rtr, device, aid)
        confBool = input("Would you like to remove? (t/n): ")
        if confBool == "t":
            #checkAdmin(rtr, session, aid)
            try:
                removeAdmin(rtr, user, device, session)
                df['STATUS'] = 'SUCCESS'
            except:
                print("ERROR!")
                df['STATUS']= 'ERROR'
                
            delete_session(rtr, session)
            confBool = "n"
        else:
            return
        bool = input("Would you like to continue? (t/n): ")
        if bool == "t":
            print("Continuing...")
        else:
            df.to_csv("./result.csv")
            return
        i =+ i
if __name__ == "__main__":
    main()