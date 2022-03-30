# Write your awesome code here
import json
from collections import defaultdict
import re


def display(err_list):  # used for printing
    for key, value in err_list.items():
        if value != 2 and value != 0:
            print(f'There is no start or end stop for the line: {key}.')
            exit()


def main():  # calculates type errors and empty lines
    data = json.loads(input())
    total_error_count = 0
    err_list = {"bus_error": 0, "stop_id_error": 0, "stop_name_error": 0, "next_stop_error": 0, "stop_type_error": 0, "a_time_error": 0}
    for item in data:
        if not isinstance(item['bus_id'], int) or item['bus_id'] == '':
            err_list['bus_error'] += 1
            total_error_count += 1
        if not isinstance(item['stop_id'], int) or item['stop_id'] == '':
            err_list["stop_id_error"] += 1
            total_error_count += 1
        if not isinstance(item['stop_name'], str) or item['stop_name'] == '':
            err_list["stop_name_error"] += 1
            total_error_count += 1
        if not isinstance(item['next_stop'], int) or item['next_stop'] == '':
            err_list["next_stop_error"] += 1
            total_error_count += 1
        if not isinstance(item['stop_type'], str) or len(str(item['stop_type'])) > 1:
            err_list["stop_type_error"] += 1
            total_error_count += 1
        if not isinstance(item['a_time'], str) or item['a_time'] == '':
            err_list["a_time_error"] += 1
            total_error_count += 1
    display(err_list, total_error_count)


def format_errors():  # counts formating errors
    data = json.loads(input())
    total_error_count = 0
    err_list = {"stop_name_error": 0, "stop_type_error": 0, "a_time_error": 0}
    for item in data:
        if not re.match('[A-Z].+ (Road|Avenue|Boulevard|Street)$', item['stop_name']) or item['stop_name'] == '':
            err_list["stop_name_error"] += 1
            total_error_count += 1
        if not re.match(r'(S$|O$|F$|^$)', item['stop_type']):
            err_list["stop_type_error"] += 1
            total_error_count += 1
        if not re.match('^[012][0-9]:[0-6][0-9]$', str(item['a_time'])) or item['a_time'] == '':
            err_list["a_time_error"] += 1
            total_error_count += 1
    display(err_list, total_error_count)


def count_stops(data):  # checks if stops have an end and beginning
    err_list = {"128": 0, "256": 0, "512": 0, "1024": 0}
    for item in data:
        if re.match('128', str(item['bus_id'])) and re.match('F|S', str(item['stop_type'])):
            err_list["128"] += 1
        if re.match(r'256', str(item['bus_id'])) and re.match('F|S', str(item['stop_type'])):
            err_list["256"] += 1
        if re.match('512', str(item['bus_id'])) and re.match('F|S', str(item['stop_type'])):
            err_list["512"] += 1
        if re.match('1024', str(item['bus_id'])) and re.match('F|S', str(item['stop_type'])):
            err_list["1024"] += 1
    display(err_list)


def find_stops(data):  # checks the number of start, transfer and end stops
    start_stops = []
    end_stops = []
    all_stops = []
    transfer_stops = []
    for item in data:
        if re.match('S', str(item['stop_type'])) and item['stop_name'] not in start_stops:
            start_stops.append(item['stop_name'])
        if re.match('F', str(item['stop_type'])) and item['stop_name'] not in end_stops:
            end_stops.append(item['stop_name'])
        if item:
            all_stops.append(item['stop_name'])
    start_stops.sort(reverse=False)
    end_stops.sort(reverse=False)
    print(f'Start stops {len(start_stops)} {start_stops}')
    for stop in all_stops:
        if all_stops.count(stop) >= 2 and stop not in transfer_stops:
            transfer_stops.append(stop)
            all_stops.remove(stop)
    transfer_stops.sort(reverse=False)
    print(f'Transfer stops {len(transfer_stops)} {transfer_stops}')
    print(f'Finish stops {len(end_stops)} {end_stops}')


def start_end():
    data = json.loads(input())
    count_stops(data)
    find_stops(data)


def stop_times():  # checks arrival time order
    stops = defaultdict(int)
    wrong_lines = {}
    data_dict = json.loads(input())

    for x in data_dict:
        if x["bus_id"] in wrong_lines:
            continue
        if int(x["a_time"][:2] + x["a_time"][3:]) < stops[x["bus_id"]]:
            wrong_lines[x["bus_id"]] = x["stop_name"]
        else:
            stops[x["bus_id"]] = int(x["a_time"][:2] + x["a_time"][3:])
    print('Arrival time test:')
    if len(wrong_lines) == 0:
        print('OK')
    else:
        for x in wrong_lines:
            print(f"bus_id line {x}: wrong time on station {wrong_lines[x]}")


def on_demand():  # checks on demand stops
    data = json.loads(input())
    on_stops = []
    wrong_type = []
    for item in data:
        if re.match('O', str(item['stop_type'])):
            on_stops.append(item['stop_name'])
    for item in data:
        if item['stop_type'] != 'O' and item['stop_name'] in on_stops:
            wrong_type.append(item['stop_name'])
    print('On demand stops test:')
    if len(wrong_type) == 0:
        print('OK')
    else:
        wrong_type.sort(reverse=False)
        print(f'Wrong stop type: {wrong_type}')


on_demand()
