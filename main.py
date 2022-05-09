from stat import FILE_ATTRIBUTE_SPARSE_FILE
import console_number_input
import json
from time import sleep
from difflib import SequenceMatcher
import statistics

data = {}
try:
    f = open("data.json")
    data = json.load(f)
    f.close()
except:
    print("Error: Unable to open data.json")


# load in the json file data
def refresh_data():

    f = open("data.json")
    new_data = json.load(f)
    f.close()
    return new_data

def save_data_to_file():
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

refresh_data()

print("")
print("")
print("--------------------------------------------")
print("")
print("The Computer Science Club's All In One (AIO)")
print("             By: Jonathan Lin               ")
print("")
print("--------------------------------------------")
print("")

obj = console_number_input.console_number_input()

questions = ["Check and update everything (full diagnosis)", "Add an event's points - add an event to the list of events in data.json", "Delete an event's data - remove a given event from the data.json file", "Output members' names in order of points", "Output members' names in alphabetical order", "Check for similar member names and combine points", "Update members' points - collects all the points from the events and updates points", "Output Eligible Members - outputs a list of eligble members that meet a certain point count (typically used to check for extra credit eligbility)", "Statistics - output statistics", "Backup data.json to backup_data.json", "Exit"]
user_input = obj.num_input(questions, "What would you like to do")

user_input = int(user_input)

# exit function
if user_input == len(questions) + 1:
    exit()

# check everything and update verything
if user_input == 1:

    # match all the events with the members names
    print("--------------------------------------------------")
    print("Updating the members")

    all_members = []
    new_dict = {}
    for key in list(data["point_data"].keys()):
        list_of_members = data["point_data"][key]["members"]
        for y in range(0, len(list_of_members)):
            if list_of_members[y] not in all_members:
                all_members.append(list_of_members[y])
                new_dict[list_of_members[y]] = data["point_data"][key]["points"]
            else:
                new_dict[list_of_members[y]] += data["point_data"][key]["points"]
    

    # compensate for different forms of the same name
    for x in range(0, len(all_members)):
        original_name = all_members[x]
        all_members[x].strip()
        if "," in all_members[x]:
            temp = all_members[x][0:all_members[x].find(",")] + all_members[x][all_members[x].find(",")+1:len(all_members)]
            if " " in temp:
                temp = temp[temp.find(" ")+1:len(temp)] + " " + temp[0:temp.find(" ")]
            all_members[x] = temp

        if "  " in all_members[x]:
            all_members[x] = all_members[x][0:all_members.find("  ")] + all_members[x][all_members.find("  ")+1:len(all_members)]
        
        modified_name = all_members[x]
        if modified_name != original_name:
            if modified_name in list(new_dict.keys()):
                new_dict[modified_name] = new_dict[modified_name] + new_dict[original_name]
            else:
                new_dict[modified_name] = new_dict[original_name]
            new_dict.pop(original_name)

    save_data_to_file()
    sleep(0.5)
    print("")
    sleep(0.5)
    print("Successfully updated the members' points")
    sleep(0.5)

    # put the members' list in numerical order
    print("--------------------------------------------------")
    print("Putting the names in alphabetical order")
    
    data = refresh_data()
    unsorted_names = list(data["member_data"].keys())
    unsorted_values = list(data["member_data"].values())

    sorted_values = []
    sorted_indexes = []
    for x in range(0, len(unsorted_values)):
        cur_val = unsorted_values[x]
        placed = False
        for i in range(0, len(sorted_values)):
            if cur_val <= sorted_values[i]:
                sorted_values.insert(i, cur_val)
                sorted_indexes.insert(i, x)
                placed = True
                break
        if placed == False:
            sorted_values.append(cur_val)
            sorted_indexes.append(x)
    
    # originally is low to high. so reverse to make it high to low
    sorted_values.reverse()
    sorted_indexes.reverse()

    # take the indexes from sorting the values and use it to sort/match the names in order
    sorted_names = []
    for i in range(0, len(sorted_indexes)):
        sorted_names.append(unsorted_names[sorted_indexes[i]])
    
    new_dict = {}
    for i in range(0, len(sorted_values)):
        new_dict[sorted_names[i]] = sorted_values[i]

    data["member_data"] = {}
    data["member_data"] = new_dict

    save_data_to_file()
    sleep(0.5)
    print("")
    sleep(0.5)
    print("Successfully placed the names in alphabetical order.")
    sleep(0.5)

    # check for similar names
    # --------------------------------------------
    print("\n--------------------------------------------------")
    print("Checking for similar names")
    sleep(0.5)
    data = refresh_data()

    # get all the similar pairs that are not the exact same and that are above the similarity threshold of 75%
    checked_pairs = []
    for name in list(data["member_data"].keys()):
        for other_name in list(data["member_data"].keys()):
            if SequenceMatcher(None, name, other_name).ratio() < 1 and SequenceMatcher(None, name, other_name).ratio() > 0.75:
                checked = False
                for pair in checked_pairs:
                    if pair[0] == name and pair[1] == other_name:
                        checked = True
                    if pair[0] == other_name and pair[1] == name:
                        checked = True
                if checked == False:
                    checked_pairs.append((name, other_name))

    print("")
    print(str(len(checked_pairs)) + " total similarities")

    for i in range(0, len(checked_pairs)):
        pair = checked_pairs[i]
        correct_spelling = ""
        incorrect_spelling = ""
        print("-----------------------------------------")
        print("Pair #" + str(i+1))
        number_input = obj.num_input([str(checked_pairs[i][0]) , str(checked_pairs[i][1]), "SKIP"], "Which spelling is correct")
        sleep(0.5)
        if number_input == 3:
            print("Skipped")
        else:
            if number_input == 1:
                correct_spelling = pair[0]
                incorrect_spelling = pair[1]
            elif number_input == 2:
                correct_spelling = pair[1]
                incorrect_spelling = pair[0]
            data["member_data"][correct_spelling] = data["member_data"][correct_spelling] + data["member_data"][incorrect_spelling]
            data["member_data"].pop(incorrect_spelling)
            print("Successfully combined the points of " + correct_spelling + " and " + incorrect_spelling)
            sleep(0.5)

            # go through the events and delete all instances of the incorrect spelling
            for x in range(0, len(list(data["point_data"].keys()))):
                event_name = list(data["point_data"].keys())[x]
                list_of_members = data["point_data"][event_name]["members"]
                for y in range(0, len(list_of_members)):
                    if list_of_members[y] == incorrect_spelling:
                        data["point_data"][event_name]["members"].remove(incorrect_spelling)
                        data["point_data"][event_name]["members"].append(correct_spelling)

            print(correct_spelling + " now has " + str(data["member_data"][correct_spelling]) + " points")
        sleep(0.5)
    print("")
    sleep(0.5)
    print("Successfully updated all potential similar names.")
    sleep(0.5)
    save_data_to_file()
    
# adding an event's points
if user_input == 2:

    data = refresh_data()

    # receive the event's name
    print("")
    event_name = input("Please enter the event's name: ")

    # get how much the event is worth
    print("")
    event_points = input("How many points should be assigned to this event: ")
    valid_input = False
    while valid_input == False:
        try:
            event_points = int(event_points)
            valid_input = True
        except:
            event_points = input("Please input an integer: ")
    
    # receive the member's list
    print("")
    print("Please input the list of the members")
    print("Place the members' names separated by commas. Example input:")
    print("")
    print("John Doe,Jane Doe,Dr. Suess")
    print("")
    print("Click enter twice when you are done")
    print("")
    names = []
    while True:
        line = input()
        if line:
            names.append(line)
        else:
            break
    str_names = ""
    for name in names:
        str_names = str_names + name + ", "
    str_names = str_names[0:len(str_names)-2]
    
    # confirm
    print("-----------------------")
    print(event_name)
    print(str(event_points) + " points")
    print("\nAll Members: " + str_names + "\n")
    print("To confirm, is this the correct information for the event?")
    confirmation = input("(Y/N): ")
    confirmation = confirmation.lower()
    if confirmation == "y" or confirmation == "yes":
        new_dict = {
            "points":event_points,
            "members":names
        }
        data["point_data"][event_name] = new_dict
        save_data_to_file()

# remove an event's points
if user_input == 3:
    data = refresh_data()

    # receive event name
    event_name = input("What event would you like to remove: ")

    # logic for removing event data
    if event_name not in list(data["point_data"].keys()):
        print("Error: Event not found.")
    else:
        data["point_data"].pop(event_name)
        save_data_to_file()
        print("Successfully removed the data for "+ event_name) 

# output members' names in order of points
if user_input == 4:
    data = refresh_data()
    unsorted_names = list(data["member_data"].keys())
    unsorted_values = list(data["member_data"].values())

    sorted_values = []
    sorted_indexes = []
    for x in range(0, len(unsorted_values)):
        cur_val = unsorted_values[x]
        placed = False
        for i in range(0, len(sorted_values)):
            if cur_val <= sorted_values[i]:
                sorted_values.insert(i, cur_val)
                sorted_indexes.insert(i, x)
                placed = True
                break
        if placed == False:
            sorted_values.append(cur_val)
            sorted_indexes.append(x)
    
    # originally is low to high. so reverse to make it high to low
    sorted_values.reverse()
    sorted_indexes.reverse()

    # take the indexes from sorting the values and use it to sort/match the names in order
    sorted_names = []
    for i in range(0, len(sorted_indexes)):
        sorted_names.append(unsorted_names[sorted_indexes[i]])

    # print out everything
    print("")
    for i in range(0, len(sorted_names)):
        print(sorted_names[i] + " - " + str(sorted_values[i]) + " points")

# output members' names in alphabetical order
if user_input == 5:
    data = refresh_data()

    names = list(data["member_data"].keys())
    names.sort()
    

    new_dict = {}
    for name in names:
        new_dict[name] = data["member_data"][name]
    
    # print out everything
    # could do this in the previous loop, but separating them for clarity reasons
    for name in names:
        print(name + " - " + str(new_dict[name]) + " points")

# check for similar names
if user_input == 6:
    data = refresh_data()

    # get all the similar pairs that are not the exact same and that are above the similarity threshold of 75%
    checked_pairs = []
    for name in list(data["member_data"].keys()):
        for other_name in list(data["member_data"].keys()):
            if SequenceMatcher(None, name, other_name).ratio() < 1 and SequenceMatcher(None, name, other_name).ratio() > 0.75:
                checked = False
                for pair in checked_pairs:
                    if pair[0] == name and pair[1] == other_name:
                        checked = True
                    if pair[0] == other_name and pair[1] == name:
                        checked = True
                if checked == False:
                    checked_pairs.append((name, other_name))

    print("")
    print(str(len(checked_pairs)) + " total similarities")

    for i in range(0, len(checked_pairs)):
        pair = checked_pairs[i]
        correct_spelling = ""
        incorrect_spelling = ""
        print("-----------------------------------------")
        print("Pair #" + str(i+1))
        number_input = obj.num_input([str(checked_pairs[i][0]) , str(checked_pairs[i][1]), "SKIP"], "Which spelling is correct")
        sleep(0.5)
        if number_input == 3:
            print("Skipped")
        else:
            if number_input == 1:
                correct_spelling = pair[0]
                incorrect_spelling = pair[1]
            elif number_input == 2:
                correct_spelling = pair[1]
                incorrect_spelling = pair[0]
            data["member_data"][correct_spelling] = data["member_data"][correct_spelling] + data["member_data"][incorrect_spelling]
            data["member_data"].pop(incorrect_spelling)
            print("Successfully combined the points of " + correct_spelling + " and " + incorrect_spelling)
            sleep(0.5)

            # go through the events and delete all instances of the incorrect spelling
            for x in range(0, len(list(data["point_data"].keys()))):
                event_name = list(data["point_data"].keys())[x]
                list_of_members = data["point_data"][event_name]["members"]
                for y in range(0, len(list_of_members)):
                    if list_of_members[y] == incorrect_spelling:
                        data["point_data"][event_name]["members"].remove(incorrect_spelling)
                        data["point_data"][event_name]["members"].append(correct_spelling)

            print(correct_spelling + " now has " + str(data["member_data"][correct_spelling]) + " points")
        sleep(0.5)

    save_data_to_file()

# update members' points
if user_input == 7:
    all_members = []
    new_dict = {}
    for key in list(data["point_data"].keys()):
        list_of_members = data["point_data"][key]["members"]
        for y in range(0, len(list_of_members)):
            if list_of_members[y] not in all_members:
                all_members.append(list_of_members[y])
                new_dict[list_of_members[y]] = data["point_data"][key]["points"]
            else:
                new_dict[list_of_members[y]] += data["point_data"][key]["points"]
    

    # compensate for different forms of the same name
    for x in range(0, len(all_members)):
        original_name = all_members[x]
        all_members[x].strip()
        if "," in all_members[x]:
            temp = all_members[x][0:all_members[x].find(",")] + all_members[x][all_members[x].find(",")+1:len(all_members)]
            if " " in temp:
                temp = temp[temp.find(" ")+1:len(temp)] + " " + temp[0:temp.find(" ")]
            all_members[x] = temp

        if "  " in all_members[x]:
            all_members[x] = all_members[x][0:all_members.find("  ")] + all_members[x][all_members.find("  ")+1:len(all_members)]
        
        modified_name = all_members[x]
        if modified_name != original_name:
            if modified_name in list(new_dict.keys()):
                new_dict[modified_name] = new_dict[modified_name] + new_dict[original_name]
            else:
                new_dict[modified_name] = new_dict[original_name]
            new_dict.pop(original_name)
    
    #print(new_dict)
    # sort the names in order
    data = refresh_data()
    data["member_data"] = new_dict
    unsorted_names = list(data["member_data"].keys())
    unsorted_values = list(data["member_data"].values())

    sorted_values = []
    sorted_indexes = []
    for x in range(0, len(unsorted_values)):
        cur_val = unsorted_values[x]
        placed = False
        for i in range(0, len(sorted_values)):
            if cur_val <= sorted_values[i]:
                sorted_values.insert(i, cur_val)
                sorted_indexes.insert(i, x)
                placed = True
                break
        if placed == False:
            sorted_values.append(cur_val)
            sorted_indexes.append(x)
    
    # originally is low to high. so reverse to make it high to low
    sorted_values.reverse()
    sorted_indexes.reverse()

    # take the indexes from sorting the values and use it to sort/match the names in order
    sorted_names = []
    for i in range(0, len(sorted_indexes)):
        sorted_names.append(unsorted_names[sorted_indexes[i]])
    
    new_dict = {}
    for i in range(0, len(sorted_values)):
        new_dict[sorted_names[i]] = sorted_values[i]

    data["member_data"] = {}
    data["member_data"] = new_dict

    print("Successfully updated the members' points from the given events.")
    save_data_to_file()

# output eligble members for a given number of points
if user_input == 8:
    print("")

    # get given points
    user_in = input("What do you want to set your point treshhold to (inclusive): ")
    valid_input = False
    while valid_input == False:
        try:
            user_in = int(user_in)
            valid_input = True
        except:
            user_in = input("Please input an integer: ")
    point_treshold = int(user_in)
    out = []
    for member in list(data["member_data"].keys()):
        if data["member_data"][member] >= point_treshold:
            out.append(member)

    # print out all the members that qualify
    print("")
    sleep(0.5)
    print("Here is the list of members that have at least " + str(point_treshold) + " points:")
    sleep(0.5)
    print("")
    for member in out:
        print(member)

# output statistics
if user_input == 9:
    data = refresh_data()

    total_points = 0
    for val in list(data["member_data"].values()):
        total_points += val

    average_points = round((sum(list(data["member_data"].values()))/len(list(data["member_data"].keys()))))

    sorted_points = list(data["member_data"].values())
    sorted_points.sort()
    sorted_points.reverse()

    print("-----------------------------------\n")
    print("Total Members: " + str(len(list(data["member_data"].keys()))))
    print("")
    print("Total Points Accumilated: " + str(total_points))
    print("")
    print("Average Points per Member: " + str(average_points))
    print("")
    print("Median Number of Points: " + str(statistics.median(list(data["member_data"].values()))))
    print("")
    print("Highest Number of Points: " + str(sorted_points[0]))
    print("")
    print("Lowest Number of Points: " + str(sorted_points[len(sorted_points)-1]))
    

# backup data.json to backup_data.json
if user_input == 10:
    data = refresh_data()

    print("")
    print("Are you sure you want to transfer the data from data.json to backup_data.json? This action is not reversible.")
    user_in = input("(Y/N): ")
    user_in.lower()
    if user_in == "y" or user_in == "yes":
        with open('backup_data.json', 'w') as f:
            json.dump(data, f, indent=4)
        print("Successfully backed up data.")
    else:
        print("Cancelled backup.")

# this is used to keep the window or terminal open after completion of the specified task
print("\n\n")
print("Please enter any key to exit")
temp = input("")
exit()