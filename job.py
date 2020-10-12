import json
import os
import hashlib

class GetJob(object):
    def __init__(self, command):
        self._command = command

    def run(self, session):
        actionType,action = self._command.split(";")
        if actionType == "ReadRegKey":
            return json.dumps(session.list_registry_keys(action),indent=4, sort_keys=True)
        elif actionType == "DeleteRegKey":
            return json.dumps(session.delete_registry_key(action),indent=4, sort_keys=True)
        elif actionType == "DeleteRegValue":
            return json.dumps(session.delete_registry_value(action),indent=4, sort_keys=True)
        elif actionType == "SetRegKey":
            regKey,regValue = action.split("|")
            return json.dumps(session.set_registry_value(regKey,regValue),indent=4, sort_keys=True)
        elif actionType == "CreateRegKey":
            return json.dumps(session.create_registry_key(action),indent=4, sort_keys=True)
        elif actionType == "PrintDir":
            return json.dumps(session.list_directory(action),indent=4, sort_keys=True)
        elif actionType == "CreateProcess":
            return json.dumps(session.create_process(action),indent=4,sort_keys=True)
        elif actionType == "UploadFile":
            filename,location = action.split("|")
            return session.put_file(open(filename,'rb'),os.path.join(location,os.path.basename(filename)))
        elif actionType == "DeleteFile":
            return session.delete_file(action)
        elif actionType == "GetFile":
            bin = bytearray(session.get_file(action))
            if bin:
                readable_hash = hashlib.sha256(bin).hexdigest();
                fptr = open(readable_hash,'w+b')
                fptr.write(bin)
                fptr.close()
                return "File Retrieved Successfully"
            else:
                return "Get File Failed"


def getjob(command):
    return GetJob(command)

