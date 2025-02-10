#from send import send_sms_via_email
import argparse
import json

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

def main():
    parser = argparse.ArgumentParser(description='Script with two optional flags')
    parser.add_argument('--print', action='store_true', help='print chores and roommates')
    parser.add_argument('--rotate', action='store_true', help='rotate chores')
    
    args = parser.parse_args()
    
    if args.print:
        data = read_json('roomate_to_chore.json')
        print(data)
    if args.rotate:
        rotate_chores()
    if not (args.print or args.rotate):
        print("No functions specified. Use --print or --rotate to run functions.")

if __name__ == "__main__":
    
    main()