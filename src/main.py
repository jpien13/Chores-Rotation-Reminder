from send import send_sms_via_email
import argparse
import json
from datetime import datetime, time
import pytz
import os
import logging

chore_list = [
    "Floor Duty. (Kitchen, Livingroom & Stairs going upstairs)",    # 0
    "Kitchen Duty. (Island, Stove & Sink Dishes if any)",           # 1
    "Trash Duty. (Kitchen & Bathrooms)",                            # 2
    "Upstairs Bathroom Duty. (Sink & Shower Floors)",               # 3
    "Fridge Purge. (Remove old food, ask ppl if you are unsure)",   # 4
    "Living Room Duty. (Couch & Table)",                            # 5
    "Downstairs Bathroom Duty. (Sink & Shower Floors)"              # 6
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
    print("Rotating Chores...")
    data = read_json('roommate_to_chore.json')
    num_chores = len(data)
    
    current_chores = []
    for roommate in data:
        current_chores.append(data[roommate]['chore_id'])
    
    for i, roommate in enumerate(data):
        prev_chore_index = (i + 1) % num_chores
        data[roommate]['chore_id'] = current_chores[prev_chore_index]
        print(f"{roommate} is now assigned to {chore_list[data[roommate]['chore_id']]}")

    write_json('roommate_to_chore.json', data)
    print("updated json...")

def test_rotate_chores():
    print("Rotating Chores...")
    data = read_json('test_roommate_to_chore.json')
    num_chores = len(data)
    
    current_chores = []
    for roommate in data:
        current_chores.append(data[roommate]['chore_id'])
    
    for i, roommate in enumerate(data):
        prev_chore_index = (i + 1) % num_chores
        data[roommate]['chore_id'] = current_chores[prev_chore_index]
        print(f"{roommate} is now assigned to {chore_list[data[roommate]['chore_id']]}")

    write_json('test_roommate_to_chore.json', data)
    print("updated json...")

def check_days():
    est = pytz.timezone('US/Eastern')
    now = datetime.now(est)
    
    # Get current weekday (0 = Monday, 6 = Sunday)
    weekday = now.weekday()
    
    is_sunday = weekday == 6
    is_monday = weekday == 0
    
    return is_sunday, is_monday

def main():
    parser = argparse.ArgumentParser(description='Script with two optional flags')
    parser.add_argument('--testmode', action='store_true', help='test mode')
    parser.add_argument('--prod', action='store_true', help='prod run')
    
    args = parser.parse_args()
    if not (args.testmode or args.prod):
        print("No functions specified. Use --print or --rotate to run functions.")

    email_address = os.getenv('EMAIL_ADDRESS')
    email_password = os.getenv('EMAIL_PASSWORD')
    smtp_server = 'smtp.gmail.com'  
    smtp_port = 587  
    
    if args.testmode:

        sim_day = input('Enter what day you are simulating. Enter anything if you just want to print the chore map: ').lower()
        if sim_day == 'sunday':
            is_sunday = True
            is_monday = False
        elif sim_day == 'monday':
            is_sunday = False
            is_monday = True
        else:
            data = read_json('test_roommate_to_chore.json')
            print(data)
            return
        
        if is_sunday:
            data = read_json('test_roommate_to_chore.json')
            print(data)
            for person in data:
                message_body = f"Hello {person}, you have {chore_list[data[person]['chore_id']]} today."
                recipient_phone_number = data[person]['phone_num']
                carrier_gateway = data[person]['carrier']
                print(f"{person} would have received a text saying: Hello {person}, {message_body}")
                print(f"Phone number: {recipient_phone_number}")
                print(f"Carrier: {carrier_gateway}")
        
        if is_monday:
            test_rotate_chores()
            data = read_json('test_roommate_to_chore.json')
            for person in data:
                message_body = f"Hello {person}, you have {chore_list[data[person]['chore_id']]} today."
                recipient_phone_number = data[person]['phone_num']
                carrier_gateway = data[person]['carrier']
                print(f"{person} would have received a text saying: {message_body}")
                print(f"Phone number: {recipient_phone_number}")
                print(f"Carrier: {carrier_gateway}")
        

    if args.prod:
        is_sunday, is_monday = check_days()
        print("prod run")

        if is_sunday:
            print("is sunday")
            data = read_json('roommate_to_chore.json')
            print(data)
            for person in data:
                message_body = f"Hello {person}, you have {chore_list[data[person]['chore_id']]} today."
                if send_sms_via_email(email_address, email_password, smtp_server, smtp_port, data[person]['phone_num'], data[person]['carrier'], message_body):
                    logging.info("SMS sent successfully!")
                else:
                    logging.error("Failed to send SMS.")
        
        if is_monday:
            print("is Monday")
            rotate_chores()
            print("Reading Json")
            data = read_json('roommate_to_chore.json')
            print("attempting to send...")
            for person in data:
                message_body = f"Hello {person}, your new chore this week is: {chore_list[data[person]['chore_id']]}."
                if send_sms_via_email(email_address, email_password, smtp_server, smtp_port, data[person]['phone_num'], data[person]['carrier'], message_body):
                    logging.info("SMS sent successfully!")
                else:
                    logging.error("Failed to send SMS.")
    

if __name__ == "__main__":
    
    main()