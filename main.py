# Tommy Condon
# 20101841
# Lotto Assignment
# Embedded Systems Scripting Year 3

import urllib.request
import random
import re

user_number_list = []
winning_numbers_list = []
bonus_numbers = [0,0]

def menu():
    global user_number_list
    global winning_numbers_list
    global bonus_numbers

    print("===================")
    print("==== Main Menu ====")
    print("===================")

    print("1. Do quick pick")
    print("2. Enter numbers manually")

    choice = int(input("--->    "))

    match choice:
        case 1:
            print("==================================")
            print("======= Quick Pick Mode ==========")
            print("==================================")

            user_number_list = quick_pick()

            print("Your quick pick:")
            print(user_number_list, "BONUS: ",bonus_numbers[0], end=" ")

            # No internet so no API access
            winning_numbers_list = [1,2,3,4,5,6]
            bonus_numbers[1] = generate_bonus_number()

            print("============================")
            print("====== Prizes won ==========")
            print("============================")
            get_prizes(user_number_list,winning_numbers_list)
            
        case 2:
            print("==================================")
            print("========== Manual entry ===========")
            print("==================================")

            user_number_list = manual_entry()

            winning_numbers_list = get_draw_result()

            print("============================")
            print("====== Prizes won ==========")
            print("============================")

            get_prizes(user_number_list,winning_numbers_list)

def get_prizes(users_list,winning_numbers):
    global bonus_numbers

    matched_numbers = set(users_list) & set(winning_numbers)
    num_of_matches = len(list(matched_numbers)) # converting intersection of sets & returning size (i.e. matched numbers) to a list again

    print("Debugging: ")
    print(f"{users_list} --> B: {bonus_numbers[0]}")
    print(f"{winning_numbers_list} --> B: {bonus_numbers[1]}")
    
    
    is_bonus_matched = False

    if (bonus_numbers[0] == bonus_numbers[1]):
        is_bonus_matched = True
    else:
        is_bonus_matched = False

    if num_of_matches == 0:
        print("Sorry, you didn't win anything. Do try again though!")
    else:
        print("--------------------------------")
        print(f"You've matched {num_of_matches} numbers !!!")
        print("--------------------------------")

        if (num_of_matches == 6):
            print("you've won the jackpot")
        elif (num_of_matches == 4) or (num_of_matches == 5):
            print("You've won cash prize")
        elif (num_of_matches == 3):
            print("You've won a scratch card")
        else:
            print("Sorry, you've won nothing, maybe better luck next time!")

def get_draw_result():
    global bonus_numbers

    n = 1
    user_agent='Mozilla 5.0 (Windows; U; Windows NT 5.1; en-Us; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    urlLotto = f"https://resultsservice.lottery.ie/rest/GetResults?drawType=Lotto&lastNumberOfDraws={n}"
    headers={'User-Agent':user_agent,}
    request = urllib.request.Request(urlLotto, None, headers)
    response = urllib.request.urlopen(request)
    data = response.read().decode('utf-8')

    print("\nLotto Draw Results\n")
    lottoDrawDate = re.findall("<DrawDate>(.*)</DrawDate>", data, re.DOTALL)
    print("Date %s\n" %(lottoDrawDate[0]))

    lottoResults = re.findall("<Number>(.*?)</Number>", data, re.DOTALL)

    winning_nums = []

    for i in lottoResults:
        if (i == 6):
            bonus_numbers[1] = lottoResults[6]
        else:
            winning_nums.append(int(i))

    print("W: ", winning_nums, end=", ")
    print("Bonus No.: ", bonus_numbers[1])

    return winning_nums

def generate_bonus_number():
    return random.randint(1,47)


def quick_pick():
    global bonus_numbers

    qp_numbers = []
    for n in range(6):
        random_num = random.randint(1,47)
        if (random_num not in qp_numbers) and (is_valid_lotto_number(random_num)): # double checking that random integer generated is in fact 1-47
            qp_numbers.append(random_num)
    bonus_numbers[0] = generate_bonus_number()

    return qp_numbers

def is_valid_lotto_number(chosen_num):
    if (chosen_num <= 47) and (chosen_num >= 1):
        return True
    else:
        return False

def manual_entry():
    global bonus_numbers
    
    nums_chosen = []
    for n in range(6):
        chosen_num = int(input(f"Enter a number between 1-47: "))
        if ((chosen_num not in nums_chosen) and (is_valid_lotto_number(chosen_num))):
            nums_chosen.append(chosen_num)
    bonus_numbers[0] = int(input("Enter a bonus number (1-47): "))
    
    return nums_chosen # list of numbers manually entered excluding bonus number

menu()