"""
Maksim Popov
- Used https://www.pythontutorial.net/python-basics/python-check-if-file-exists/ to see how to check a files existence.
- Went back to ZyBooks for info on some file stuff 
- Had help from Prof Studebaker on some weird for loop stuff 
"""

from pathlib import Path
import os

def num_to_month(num): #returns month to display to user 
    num_month = int(num) #change input to integer to use for indexing

    MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")

    return MONTHS[num_month - 1] #returns string with month 

def unsupported_format(digits): #just used to print error message
    print(f"Uh oh! Looks like you entered an unsupported format. Enter {digits} digits.")

def get_input(type, format): #returns date entered that fits entered format 
    while True:
        date_type = input(f"Enter a {type} [{format}]: ")

        try: #will try to int the input, throws error if string entered and prompts user again
            int(date_type)

            if int(date_type) == 0: #catch 0 input, dates can't be zeros 
                print("You can't enter zeros!")
                continue #return to top of while loop to prompt user again

            if len(format) == 4: #if looking for year (only four digit format)
                if len(date_type) != 4: #if not in 4 digit format 
                    unsupported_format(len(format)) #remind user to enter that number of digits
                    continue #go back to top of loop

            if type == "month": #if we're taking a month
                if int(date_type) > 12: #if entered number is over 12 
                    print("There's only 12 months! Try again.")
                    continue #go back to top of loop to reenter in acceptable range 

            if type == "day": # if we're taking a day
                if int(date_type) > 31: #if entered number is over 31
                    print("There can't be more than 31 days in a month!")
                    continue #go back to top of loop to reenter in acceptable range 
            
            if len(date_type) > len(format): #if entered info is out of format 
                unsupported_format(len(format)) #prompt user to enter in proper format and go back to top of loop
            else:
                break #if everything is fine, accept input with no problems 
        except: #if cant int input (i.e. its a string)
            unsupported_format(len(format)) #prompt user to enter proper format and run loop again

    return date_type #if all conditions met, return entered string 

def display_cal_contents(file="calendar.csv"): #displays contents of a file, usually calendar 
    print()
    
    print("Entries")
    print("-------------------------")
    with open(file, "r") as cal: #open file for reading 
        for line in cal: #loop through lines in file 
            event_tokens = line.strip("\n").split(",") #list of what we processed from .csv file 

            print(f"{num_to_month(event_tokens[0])} {event_tokens[1]}, {event_tokens[2]} | {event_tokens[3]}") #print in standard format

    print()

def count_cal_lines(file="calendar.csv"): #counts lines in a file, returns number of lines in the file 
    with open(file, "r") as cal: #open to read 
        line_count = 0
        for line in cal:
            line_count += 1

    return line_count #return number of lines 

def populate_dict(file): #populate a dictionary and return that dictionary 
    dictionary = {}

    with open(file, "r") as f:
        for line in f:
            line_tokens = line.strip("\n").split(",")

            dictionary[line_tokens[-1]] = line_tokens[0:-1] #pos -1 is title every time, and everything else is whatever data is paired to that key

    return dictionary #return populated dictionary

#welcome message 
WELCOME = """ 
Welcome to PyCal!

Use me to store any event, chore,
meeting, or any other data that could
be put into a calendar!
"""

#options for user 
MENU = """
To interact with your calendar, select an option:

MENU
-----------------------
[v] - View your calendar
[a] - Add to your calendar
[r] - Remove from your calendar
[e] - Edit a calendar entry
[d] - Delete your calendar
[q] - Quit PyCal
"""

print(WELCOME) #print welcome message 

cal_path = Path("calendar.csv") #create path for file 

if cal_path.is_file(): #if the path is a file 
    print("Looks like you have a calendar with us!") #tell user theyre good to go 
else: #if path is not a file (i.e. doesn't exist)
    print("It doesn't look like you have a file with us. \nLet's get you started!")

    cal_file = open("calendar.csv", "w") #create files needed 
    cal_file.close()

    cal_desc_file = open("calendar_descriptions.csv", "w")
    cal_desc_file.close()

    print("An empty calendar has been created for you. \nLet's populate it!") 

print(MENU) #print menu to user after verifying existence of calendar 

while True: #allow user to continue working with calendar until they are done
    print()
    
    selection = input("How would you like to interact with your calendar today?: ") #get input for what user wants to do from menu 
    
    if selection == "v": #viewing calendar 
        display_cal_contents() #display contents, won't display anything if its empty 
        
        if count_cal_lines() == 0: #if the file is empty 
            print("Uh oh! Looks like your calendar is empty. How about you make another selection?") #put user back to menu selection
        else:
            descriptions_input = input("Would you like to view calendar descriptions? [y/n]: ") #get input for if they want to view descriptions 
            
            if descriptions_input == "y": # if yes 
                event_descriptions = populate_dict("calendar_descriptions.csv") #assign populated dictionary

                if count_cal_lines("calendar_descriptions.csv") == 0: #if nothing in descriptions file
                    print("Oh no! There seem to be no descriptions just yet. Let's try something else.") #prompt user to do something else
                else: #if any dsecriptions present 
                    description_key = input("Which event would you like to view? [Type title as it appears in calendar]: ") #ask which entry to view

                    try: #try to get that from the now populated dictionary 
                        description = event_descriptions[description_key]

                        print()
                        print(f"Description for: {description_key}")
                        print("-------------------------")
                        print(f"{description_key}: {description[0]}") #print key and description back to user, have to index becaause we are getting a list from the populate_dict()
                    except KeyError: #if entry doesn't exist in populated dictionary (i.e. KeyError)
                        print("This entry doesn't seem to have a description. Let's do something else!") #prompt user to do something else
    elif selection == "a": #adding to calendar 
        print("Let's add some events to your calendar.")
        
        continue_add = "y" #start loop so user can add multiple events at a time 

        while continue_add != "x":            
            year = get_input("year", "YYYY") #getting add data using get_input()

            month = get_input("month", "MM") # ""

            day = get_input("day", "DD") # ""

            while True: #loop to check if entered entry already exists
                event_title = input("Enter a title for your event: ") #get title from use r

                events = populate_dict("calendar.csv") #assign populated dictionary to work with
                
                if count_cal_lines() > 0: #if there is anything in the file 
                    if event_title in events.keys(): #if that entry already exists 
                        print("You can't enter the same event twice!") #return user to enter loop
                    else: #if entry doesn't exist 
                        break #continue to rest of add code 
                else: #if nothing in calendar file 
                    break #let user continue 

            with open("calendar.csv", "a") as cal_file: #write entered data above to file 
                event_add = str(month) + "," + str(day) + "," + str(year) + "," + event_title + "\n"

                cal_file.write(event_add)

            event_description_add = input("Would you like to add a description for your event? [y/n]: ") #ask if user wants to enter a description

            if event_description_add == "y": #if yes 
                event_description = input(f"Add a description for {event_title}: ") #prompt for description

                with open("calendar_descriptions.csv", "a") as cd: #write description with key for event 
                    cd.write(f"{event_description},{event_title}\n")

            continue_add = input("Would you like to add another calendar entry? [x to stop, any other key to continue]: ") #keep adding events?
    elif selection == "r": #removing from calendar 
        print("Let's get rid of some of those pesky entries!")

        display_cal_contents()

        events = populate_dict("calendar.csv") #assign populated dictionary

        if count_cal_lines() == 0: #if file is empty 
            print("That's weird... There's nothing to remove!") #return to menu selection
        else: #if file is not empty 
            with open("calendar.csv", "w") as l:
                while True:
                    rm_input = input("Which entry would you like to remove? [Type the entry title as it appears in the calendar.]: ") #prompt user for what they want to remove

                    try:
                        del events[rm_input] #delete entered key from dictionary 

                        for k, v in events.items(): #write remaining dictionary back to file 
                            entry_to_write = str(v[0]) + "," + str(v[1]) + "," + str(v[2]) + "," + k + "\n"
                            l.write(entry_to_write)

                        break 
                    except KeyError: #if that entry doesnt exist 
                        print("Uh oh! This entry doesn't exist.") #run loop again

            event_descriptions = populate_dict("calendar_descriptions.csv") #assign populated dictionary
            
            try:
                del event_descriptions[rm_input] #delete description that matches 

                with open("calendar_descriptions.csv", "w") as i: #write descriptions back to file 
                    for k, v in event_descriptions.items():
                        desc_entry_to_write = v[0] + "," + k + "\n" #have to index because v is a list in our dictionary, and we need to get the string at position 0 to write it back
                        i.write(desc_entry_to_write)
            except KeyError: #if key doesn't exist (i.e. no description to match )
                print("No description to delete!")
    elif selection == "e": #editing calendar 
        print("Mistakes are okay! Let's edit an entry.")

        display_cal_contents()

        events = populate_dict("calendar.csv")

        if count_cal_lines() == 0: #if file is empty 
            print("Hmmm... There's nothing to edit here! Let's do something else.")
        else: #if file has anything in it
            edit_input = input("Enter an entry to edit [Enter entry as it appears in calendar]: ") #get key for entry they want to edit 

            new_year = get_input("year", "YYYY") #get new inputs 
            new_month = get_input("month", "MM") # ""
            new_day = get_input("day", "DD") # ""

            events[edit_input] = [str(new_month), str(new_day), str(new_year)] #change that entry in the dictionary 

            with open("calendar.csv", "w") as z: #write edited back to file 
                for k, v in events.items():
                    edited_entry_to_write = v[0] + "," + v[1] + "," + v[2] + "," + k + "\n"
                    z.write(edited_entry_to_write)

            description_edit = input("Would you like to enter or change the description of this event? [y/n]: ") #does user want to edit or add description

            if description_edit == "y": #if yes 
                edit_descriptions = populate_dict("calendar_descriptions.csv")
                    
                new_description = input("Enter a new description: ") #get new description

                edited_description = [] #populate_dict returns a list as the value for each key

                edited_description.append(new_description) #in order to write a changed description properly, we need to index a list to get a string to pass back into the write function

                edit_descriptions[edit_input] = edited_description #change value in dictionary for entered key, have it set to the list we created above in order for it to be properly formatted

                with open("calendar_descriptions.csv", "w") as o: #write back to descriptions file
                    for k, v in edit_descriptions.items():
                        edited_description_to_write = v[0] + "," + k + "\n" #need to index because we are using a list. position 0 is the only position, but indexing it gives us the string we need to pass back in
                        o.write(edited_description_to_write)
    elif selection == "d": #deleting calendar 
        print("Are you sure? Deleting your calendar is something that cannot be undone.")
        delete_selection = input("Are you sure you want to delete your calendar [y/n]? ") #is user if theyre sure they want to delete

        if delete_selection == "y": #if yes 
            print()
            print("We'll miss you! Come back soon to create a new calendar!")
            os.remove("calendar.csv") #remove the files 
            os.remove("calendar_descriptions.csv")
            break #quit program 
        else:
            print("Phew! We were sure it was just a mistake!")
    elif selection == "q": #quitting calendar 
        print()
        print("Aw, darn. Come back soon to continue working with your calendar!")
        break #quit prorgam 
    else:
        print("Oops! You've made an improper selection. Try again.") #user made improper selection, run loop again

