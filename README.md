# cb-runner

## Summary

cb-runner is an experimental Python program to run automated actions via Carbon Black Live Response. The actions are stored in a simple CSV format and can be applied to a single device or list of devices.

### Pre-Requisites

1. Python 3.x
2. A working installation on CBABI (<https://cbapi.readthedocs.io/en/latest/installation.html>) and an understanting of how to configure API Authentication credentials. 

### Getting Started

#### API Access

Two levels of API access are required for cb-runner. One to read device information and job status updates and the other to connect via Live Response and issue the playbook commands. 

**Configure a custom cb-runner Access Level and API Key**

1. Navigate to Settings > API Access > Access Levels and click Add Access Level
    - Name: cb-runner
    - Description: cbrunner access level
2. Apply the following permissions:
    - Background tasks > Status > job.status = READ
    - Device > General information > device = READ
3. Click Save
4. Navigate to Settings > API Access > API Keys and click Add API Key
    - Name: cb-runner
    - Description:
    - Access Level Type: Custom
    - Custom Access Level: cb-runner
5. Click Save
6. Add the API credentials to .carbonblack/credentials.psc
    - Using cbapi run `cbapi-psc configure` or edit `credentials.psc` directly
    - Name the credential **cbrunner**
    - **Tip:** for instructions on how to use Python CBAPI follow the getting started guide (https://cbapi.readthedocs.io/en/latest/getting-started.html)

**Configure a Live Response API Key**

1. Navigate to Settings > API Access > API Keys and click Add API Key
    - Name: liveresponse
    - Description:
    - Access Level Type: Live Response
2. Click Save
3. Add the API credentials to .carbonblack/credentials.psc
    - Using cbapi run `cbapi-psc configure` or edit `credentials.psc` directly
    - Name the credential **liveresponse**
    - **Tip:** for instructions on how to use Python CBAPI follow the getting started guide (https://cbapi.readthedocs.io/en/latest/getting-started.html)


#### Running cb-runner

1. Copy a action files from playbooks to the cb-runner root directory.
2. To run against a single device
    - `python3 cb-runner.py --profile cbrunner -LR liveresponse -D MYDEVICENAME -P actions.csv`
3. To run against multiple devices
    - If running against a list of systems, update devices.csv with a list of Device IDs.
    - `python3 cb-runner.py --profile cbrunner -LR liveresponse -F devices.csv -P actions.csv

```
python3 cbrunner.py --profile simondev -LR liveresponse -h
   __________     ____  __  ___   ___   ____________     ______  
  / ____/ __ )   / __ \/ / / / | / / | / / ____/ __ \    \ \ \ \ 
 / /   / __  |  / /_/ / / / /  |/ /  |/ / __/ / /_/ /     \ \ \ \
/ /___/ /_/ /  / _, _/ /_/ / /|  / /|  / /___/ _, _/      / / / /
\____/_____/  /_/ |_|\____/_/ |_/_/ |_/_____/_/ |_|      /_/_/_/ 
                                                                 

usage: cbrunner.py [-h] [--cburl CBURL] [--apitoken APITOKEN] [--orgkey ORGKEY] [--no-ssl-verify] [--profile PROFILE] [--verbose] [-J JOB] [-LR LRPROFILE] [-D DEVICE]
                   [-I DEVICE_ID] [-F DEVICE_FILE_LIST] [-O OS] -P PLAYBOOK
                   {} ...

CB Runner

positional arguments:
  {}                    Sensor commands

optional arguments:
  -h, --help            show this help message and exit
  --cburl CBURL         CB server's URL. e.g., http://127.0.0.1
  --apitoken APITOKEN   API Token for Carbon Black server
  --orgkey ORGKEY       Organization key value for Carbon Black server
  --no-ssl-verify       Do not verify server SSL certificate.
  --profile PROFILE     profile to connect
  --verbose             enable debug logging
  -J JOB, --job JOB     Name of the job to run.
  -LR LRPROFILE, --lrprofile LRPROFILE
                        Live Response profile name configured in your credentials.psc file.
  -D DEVICE, --device DEVICE
                        Search for a device or list of devices to run the playbook against.
  -I DEVICE_ID, --device-id DEVICE_ID
                        Device ID(s) of the system to run the playbook against. Multiple device ids can be provided i CSV style format, e.g '12345678,87654321'. If a device does
                        not have a status of LIVE, the playbook will not be run against that device.
  -F DEVICE_FILE_LIST, --device-file-list DEVICE_FILE_LIST
                        A list of device names in a CSV file to run the playbook against.
  -O OS, --os OS        Device OS family to run the playbook against. Valid operating systems are: WINDOWS, MAC, LINUX.
  -P PLAYBOOK, --playbook PLAYBOOK
                        File with playbook action to run in sequential order


```

### TODO

[ ] Convert actions.csv to yaml spec
[ ] Add path/directory support for --playbook/-p parameter
[ ] Update documentation examples
