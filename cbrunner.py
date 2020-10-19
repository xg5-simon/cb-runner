#!/usr/bin/env python3

import csv
import datetime
import time
import json
import sys

from cbapi import CbDefenseAPI
from cbapi.example_helpers import build_cli_parser, get_cb_defense_object, get_cb_psc_object
from cbapi.psc import Device
from concurrent.futures import as_completed

"""
TODO:
- Apply DRY
- Add support for YAML formatted playbooks
- Add support for last contact argument
- Add device id validation before list comprehension
- Add option to save output as JSON or CSV
- Split run_playbook function into two separate functions
- Add device name to job runner status
- Add option to download a device list to CSV
"""


def get_utc_time(delta):
    """
    :param delta: timesince delta
    :type delta: int
    :return: delta
    """
    delta = datetime.datetime.utcnow() - datetime.timedelta(minutes=delta)
    return repr(delta.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3])


def run_report():
    return


def run_playbook(device_list, action_list, cb_def, cb_psc, args):
    """
    Run playbook action against it device via Live Response

    :param cb_def:
    :param list device_list: The list of devices to run the playbook against.
    :param list action_list: The list of actions in to run against the devices.
    """

    # import our job object from the jobfile
    job = __import__(args.job)

    completed_sensors = []
    futures = {}

    if len(device_list) == 1:
        print(f'Running playbook against {len(device_list)} live device.')
    else:
        print(f'Running playbook against {len(device_list)} live device(s).')

    for device in device_list:
        print("\n>>> Initiating LiveResponse")
        print(">>> Connecting...")
        print(f">>> Connected to {device.get('device_name')} - "
              f"IP:{device.get('device_last_internal_ip_address')} "
              f"OS:{device.get('device_os')} "
              f"DEVICE ID:{device.get('device_id')}")

        if len(action_list) == 1:
            print(f'\n\tExecuting {len(action_list)} action.\n')
        else:
            print(f'\n\tExecuting {len(action_list)} actions\n')

        for action in action_list:
            action_type, command = action.split(";")
            jobobject = job.getjob(action)
            print("\tProcessing command <{0}> for action <{1}>...".format(action_type, command))

            f = cb_def.live_response.submit_job(jobobject.run,
                                                device.get('device_id'))
            futures[f] = device.get('device_id')

    print("\n>>> All jobs submitted for execution")
    print(">>> ...")
    print(">>> Checking job runner status\n")

    for f in as_completed(futures.keys(), timeout=100):
        if f.exception() is None:
            print(f"\tDevice ID {futures[f]} job completed ({f.result()})")
            completed_sensors.append(futures[f])
            #f.bypass(False)
        else:
            print(f"\tDevice ID {futures[f]} had the following error: {f.exception()}")

    still_to_do = set([device.get('device_id') for device in device_list]) - set(completed_sensors)

    if len(still_to_do) > 1:
        print("\n!!! The following devices were attempted but not completed:")
        for _ in still_to_do:
            print(f"{still_to_do}")

    return


def get_device_ids_from_file(device_file):
    """
    Load a list of device ids from a csv file. Function does not use \
    csv.Sniffer class to deduce csv format and assumes the first row \
    is a header and drops it.

    :param object device_file: device file name passed by the -F argument
    :return: string of device ids
    :rtype: string
    """
    device_list = []
    with open(device_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        next(csv_reader)
        for row in csv_reader:
            device_list.append(row[0])

    return device_list


def get_playbook_actions(playbook):
    """
    Load a playbook csv file that contains a list of commands to be run on the\
    remote system(s). Commands are executed sequentially, i.e. top to bottom

    :return: List of commands to be run on each device
    :rtype: list
    """
    with open(playbook, 'r') as f:
        action_list = []
        row_count = 0
        csv_reader = csv.reader(f, delimiter=',')
        for row in csv_reader:
            if row and row_count > 0:
                action_list.append(row[0] + ";" + row[1])
            row_count += 1
    print(action_list)
    return action_list


def get_offline_devices(online_device_list, device_ids):
    """
    Compares the user submitted device list to the device list returned \
    from search_device.

    :param list online_device_list: List of devices that have status=Live
    :param list device_ids: User submitted device list.
    :return: Print list of offline devices
    :rtype: Print
    """

    online_devices = []
    for d in online_device_list:
        online_devices.append(d.get('device_id'))

    offline = list(set(device_ids).difference(online_devices))

    return print(f"\n>>> Checking for offline devices \
                \n\n\tDevices offline at execution: {offline}")


def search_device(query, device):
    """
    Takes a device name or ip address and returns a \
    list of matches. Can be a single or multiple devices.

    :param object query: PSC Device object
    :param str device: --device argument value
    :return: list of matching devices as a dictionary
    :rtype: list
    """
    query = query.where(device)
    devices = list(query)
    device_info = []
    for device in devices:
        device_dict = {
            "device_id": device.id or "None",
            "device_name": device.name or "Unknown",
            "device_last_internal_ip_address": device.last_internal_ip_address,
            "device_last_contact_time": device.last_contact_time,
            "device_status": device.status,
            "device_os": device.os
        }
        device_info.append(device_dict)

    return device_info


def main():

    parser = build_cli_parser("CB Runner")
    subparsers = parser.add_subparsers(help="Sensor commands", dest="command_name")

    parser.add_argument("-J", "--job",
                        action="store", required=False, default="job",
                        help="Name of the job to run.")
    parser.add_argument("-LR", "--lrprofile",
                        action="store", required=False,
                        help="Live Response profile name configured in your \
                              credentials.psc file.")
    parser.add_argument("-D", "--device",
                        action="store",
                        help="Search for a device or list of devices to run \
                        the playbook against.")
    parser.add_argument("-I", "--device-id",
                        action="store", required=False,
                        help="Device ID(s) of the system to run the playbook \
                        against. Multiple device ids can be provided i CSV   \
                        style format, e.g '12345678,87654321'. If a device   \
                        does not have a status of LIVE, the playbook will not\
                        be run against that device.")
    parser.add_argument("-F", "--device-file-list",
                        action="store",
                        help="A list of device names in a CSV file to run \
                        the playbook against.")
    parser.add_argument("-O", "--os",
                        action="store", required=False, default="WINDOWS",
                        help="Device OS family to run the playbook against. \
                        Valid operating systems are: WINDOWS, MAC, LINUX.")
    parser.add_argument("-P", "--playbook", required=True,
                        help="File with playbook action to run in sequential order")
    args = parser.parse_args()

    cb_psc = get_cb_psc_object(args)
    cb_def = CbDefenseAPI(profile=args.lrprofile)


    if args.device:
        query = cb_psc.select(Device).set_status(["ALL"]) \
            .set_os([args.os])
        device_list = search_device(query, args.device)
        action_list = get_playbook_actions(args.playbook)

        run_playbook(device_list, action_list, cb_def, cb_psc, args)

    if args.device_id:
        device_ids = [int(s) for s in args.device_id.split(',')]
        query = cb_psc.select(Device).set_status(["ALL"]) \
            .set_os([args.os]) \
            .set_device_ids(device_ids)
        device_list = search_device(query, None)
        action_list = get_playbook_actions(args.playbook)

        run_playbook(device_list, action_list, cb_def, cb_psc, args)
        get_offline_devices(device_list, device_ids)

    if args.device_file_list:
        device_ids = get_device_ids_from_file(args.device_file_list)
        device_ids = [int(s) for s in device_ids]
        query = cb_psc.select(Device).set_status(["ALL"]) \
            .set_os([args.os]) \
            .set_device_ids(device_ids)
        device_list = search_device(query, None)
        action_list = get_playbook_actions(args.playbook)

        run_playbook(device_list, action_list, cb_def,cb_psc, args)
        get_offline_devices(device_list, device_ids)


if __name__ == "__main__":
    sys.exit(main())
