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