# =======================================================
# Name: Tommy Condon
# Student Number: 20101841
# National Lotto Assignment
# Module: Embedded Systems Scripting Year 3#
# Course: Applied Computing Year 3
# =======================================================

# Note: Random number generation section (60% part) has been commented out and the prizes function has been refactored
# Assignment includes API functionality

import urllib.request
import random
import re
from time import sleep

user_number_list = [] # users quick pick/manual entries
winning_numbers_list = [] # stores winning lotto numbers
bonus_numbers = [0,0] # stores bonus (winning and user one) numbers 
#lotto_plus_1 = []
#lotto_plus_2 = []

# Menu function
# Main function for displaying menu and options
def menu():
    global user_number_list
    global winning_numbers_list
    global bonus_numbers
    #global lotto_plus_2
    #global lotto_plus_1

    print("===================")
    print("==== Main Menu ====")
    print("===================")

    print("1. Do quick pick")
    print("2. Enter numbers manually")

    choice = int(input("--->    "))

    #lotto_plus = input("Do you want to be entered into lotto plus? (Y / N): ")

    match choice:
        case 1:
            print("\n==================================")
            print("======= Quick Pick Mode ==========")
            print("==================================\n")

            user_number_list = quick_pick()

            print("Your quick pick:",user_number_list, "YOUR BONUS NUMBER: ",bonus_numbers[0],"\n")

            sleep(1)

            winning_numbers_list = get_draw_result()
            #winning_numbers_list = random.sample(range(1,47),7)
                
            #if lotto_plus == 'Y' or lotto_plus == 'y':
            #    lotto_plus_1 = random.sample(range(1,47),7)
            #    lotto_plus_2 = random.sample(range(1,47),7)
                
            #bonus_numbers[1] = 7

            print("Latest Lotto Winning Numbers: ", winning_numbers_list, "--> Bonus Num: ", bonus_numbers[1])
            
            #if lotto_plus == "Y" or lotto_plus == "y":
            #    print("Lotto Plus 1 Winning Numbers", lotto_plus_1[:-1], "--> Bonus Num: ", lotto_plus_1[6])
            #    print("Lotto Plus 2 Winning Numbers", lotto_plus_2[:-1], "--> Bonus Num: ", lotto_plus_2[6],"\n")

            print("\n=============================")
            print("====== Prizes won ==========")
            print("============================\n")

            get_prizes(user_number_list,winning_numbers_list)
            print("\n")
            
        case 2:
            print("\n==================================")
            print("========== Manual entry ===========")
            print("==================================\n")

            user_number_list = manual_entry()

            print("Your numbers picked: ",user_number_list, "YOUR BONUS NUMBER: ",bonus_numbers[0],"\n")

            sleep(1)

            winning_numbers_list = get_draw_result()
            #winning_numbers_list = random.sample(range(1,47),7)
                
            #if lotto_plus == 'Y' or lotto_plus == 'y':
            #    lotto_plus_1 = random.sample(range(1,47),7)
            #    lotto_plus_2 = random.sample(range(1,47),7)
                
            #bonus_numbers[1] = 7

            print("Latest Lotto Winning Numbers: ", winning_numbers_list, "--> Bonus Num: ", bonus_numbers[1])
            
            #if lotto_plus == "Y" or lotto_plus == "y":
            #    print("Lotto Plus 1 Winning Numbers", lotto_plus_1[:-1], "--> Bonus Num: ", lotto_plus_1[6])
            #    print("Lotto Plus 2 Winning Numbers", lotto_plus_2[:-1], "--> Bonus Num: ", lotto_plus_2[6],"\n")

            print("\n=============================")
            print("====== Prizes won ==========")
            print("============================\n")

            get_prizes(user_number_list,winning_numbers_list)
            print("\n")

# Print out prizes given the users numbers (e.g. quick pick or manual) and the last draw
def get_prizes(users_list,winning_numbers):
    global bonus_numbers

    matched_numbers = set(users_list) & set(winning_numbers)
    num_of_matches = len(list(matched_numbers)) # converting intersection of sets & returning size (i.e. matched numbers) to a list again
    
    is_bonus_matched = False

    if (bonus_numbers[0] == bonus_numbers[1]):
        is_bonus_matched = True # setting bonus match to true if bonus number is matched
        num_of_matches = num_of_matches + 1
    else:
        is_bonus_matched = False # otherwise, false

    if num_of_matches == 0:
        print("\nSorry, you didn't win anything. Do try again though!")
    else:
        print("--------------------------------")
        print(f"You've matched {num_of_matches} numbers !!!")
        print("--------------------------------\n")

        if (num_of_matches == 6):
            print("you've won the jackpot")
        elif (num_of_matches == 5):
            print("You've won cash prize")
        elif (num_of_matches == 4):
            print("You've won cash prize")
        elif (num_of_matches == 3):
            if (is_bonus_matched):
                print("You've won cash prize")
            else:
                print("You've won a scratch card")
        else:
            print("Sorry, you've won nothing, maybe better luck next time!")

# Grab the last set of draw results from the API
def get_draw_result():
    global bonus_numbers

    n = 1 # pulls last draw
    user_agent='Mozilla 5.0 (Windows; U; Windows NT 5.1; en-Us; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    urlLotto = f"https://resultsservice.lottery.ie/rest/GetResults?drawType=Lotto&lastNumberOfDraws={n}"
    headers={'User-Agent':user_agent,}
    request = urllib.request.Request(urlLotto, None, headers)
    response = urllib.request.urlopen(request)
    data = response.read().decode('utf-8')

    print("\n------- Lotto Draw Results -------\n")
    lottoDrawDate = re.findall("<DrawDate>(.*)</DrawDate>", data, re.DOTALL)
    print("Date %s\n" %(lottoDrawDate[0]))

    lottoResults = re.findall("<Number>(.*?)</Number>", data, re.DOTALL)

    winning_nums = []

    for num in lottoResults:
        if (len(winning_nums) == 6):
            bonus_numbers[1] = int(lottoResults[6])
        else:
            winning_nums.append(int(num))

    print("Winning Draw: ", winning_nums, end=", ")
    print("Bonus No.: ", bonus_numbers[1])

    return winning_nums

def generate_bonus_number():
    return random.randint(1,47)

# Generate a quick pick card and return the numbers generated (1-47)
def quick_pick():
    global bonus_numbers

    qp_numbers = []
    for n in range(6):
        random_num = random.randint(1,47)
        if (random_num not in qp_numbers):
            qp_numbers.append(random_num)
        else:
            qp_numbers.append(random.randint(1,47))
    bonus_numbers[0] = generate_bonus_number()

    return qp_numbers

# Check if the user's entered number for manual mode is between 1-47. Otherwise, return false
def is_valid_lotto_number(chosen_num):
    if (chosen_num <= 47) and (chosen_num >= 1):
        return True
    else:
        return False

# Manual mode for lotto interface
def manual_entry():
    global bonus_numbers
    
    nums_chosen = []
    for n in range(6):
        chosen_num = int(input("Enter a number between 1-47: "))
        if ((chosen_num not in nums_chosen) and (is_valid_lotto_number(chosen_num))):
            nums_chosen.append(chosen_num)
    bonus_numbers[0] = int(input("Enter a bonus number (1-47): "))
    
    return nums_chosen # list of numbers manually entered excluding bonus number


menu() # Calling menu function to start script