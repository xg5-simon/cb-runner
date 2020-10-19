# pb_autoupdate

This playbook can be used to modify the AutoUpdate paramater in cfg.ini. It is useful in the scenario where the AutoUpdate=0 parameter was applied during installation and if you want to revert it to default (AutoUpdate=1) and permit sensor upgrades from the Carbon Black Cloud console.

## Pre-requisites

1. The sensor must be in bypass mode when the actions are run.
2. Modfy the UploadFile directory paths in actions.csv to reflect the directory the files are being uploaded from (typically the cb-runner root directory).
    - If running cb-runner from a Windows Operating System, double escape the backslash in the directory path, i.e. `C:\\myuser\\Set-AutoUpdate.ps1`
3. Modify runautoupdate.bat to execute PowerShell in accordance with your organisations policy. `-NoProfile -ExecutionPolicy Bypass` should not be used in production.

### Actions Summary

1. Deletes runautoupdate.bat and Set-AutoUpdate.ps1 if they already exist.
2. Uploads runautoupdate.bat and Set-AutoUpdate.ps1
3. Executes runautoupdate.bat which invokes PowerShell to run Set-AutoUpdate.ps1.  Set-AutoUpdate.ps1 will search the contents of cfg.ini and replace AutoUpdate=0 with AutoUpdate=1
4. Run RepCLI.exe to update the sensor config with the new cfg.ini.

### How to Run

1. Copy actions.csv, runautoupdate.bat and Set-AutoUpdate.ps1 to the cb-runner root directory.
2. To run against a single device
    - `python3 cb-runner.py --profile cbrunner -LR liveresponse -D MYDEVICENAME -P actions.csv`
3. To run against multiple devices
    - If running against a list of systems, update devices.csv with a list of Device IDs.
    - `python3 cb-runner.py --profile cbrunner -LR liveresponse -F devices.csv -P actions.csv`
