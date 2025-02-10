#from send import send_sms_via_email
import argparse
import json
from datetime import datetime, time
import pytz

chore_list = [
    "Chore 0", # 0
    "Chore 1", # 1
    "Chore 2"  # 2
]

def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def edit_json_data(data, key, new_value):
    if key in data:
        data[key] = new_value
    return data

def write_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def rotate_chores():
    roommates = read_json('roomate_to_chore.json')
    num_chores = len(chore_list)
    
    current_chores = []
    for i in range(num_chores):
        roommate = f"Roommate {i}"
        current_chores.append(roommates[roommate])
    
    for i in range(num_chores):
        roommate = f"Roommate {i}"
        prev_chore_index = (i - 1) % num_chores
        roommates[roommate] = current_chores[prev_chore_index]
        print(f"{roommate} is now assigned to {chore_list[roommates[roommate]]}")

    write_json('roomate_to_chore.json', roommates)

def check_days():
    est = pytz.timezone('US/Eastern')
    now = datetime.now(est)
    
    target_time = time(hour=15, minute=0)  # 15:00 = 3 PM
    
    # Get current weekday (0 = Monday, 6 = Sunday)
    weekday = now.weekday()
    current_time = now.time()
    
    is_sunday = weekday == 6 and current_time.hour == target_time.hour
    is_monday = weekday == 0 and current_time.hour == target_time.hour
    
    return is_sunday, is_monday

def main():
    parser = argparse.ArgumentParser(description='Script with two optional flags')
    parser.add_argument('--testmode', action='store_true', help='test mode')
    parser.add_argument('--prod', action='store_true', help='prod run')
    
    args = parser.parse_args()
    if not (args.testmode or args.prod):
        print("No functions specified. Use --print or --rotate to run functions.")
    
    if args.testmode:

        sim_day = input('Enter what day you are simulating. Enter anything if you just want to print the chore map: ').lower()
        if sim_day == 'sunday':
            is_sunday = True
            is_monday = False
        elif sim_day == 'monday':
            is_sunday = False
            is_monday = True
        else:
            data = read_json('roomate_to_chore.json')
            print(data)
            return
        
        if is_sunday:
            data = read_json('roomate_to_chore.json')
            print(data)
        
        if is_monday:
            rotate_chores()

    if args.prod:
        is_sunday, is_monday = check_days()

        if is_sunday:
            data = read_json('roomate_to_chore.json')
            print(data)
        
        if is_monday:
            rotate_chores()

    

if __name__ == "__main__":
    
    main()