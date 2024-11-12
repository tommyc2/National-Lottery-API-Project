import urllib.request
import random
import re

def get_winning_numbers():
    n = 1
    user_agent='Mozilla 5.0 (Windows; U; Windows NT 5.1; en-Us; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    urlLotto = f"https://resultsservice.lottery.ie/rest/GetResults?drawType=Lotto&lastNumberOfDraws={n}"
    headers={'User-Agent':user_agent,}
    request = urllib.request.Request(urlLotto, None, headers)
    response = urllib.request.urlopen(request)
    data = response.read().decode('utf-8')

    print("Lotto Draw Results\n")
    lottoDrawDate = re.findall("<DrawDate>(.*)</DrawDate>", data, re.DOTALL)
    print("Date %s\n" %(lottoDrawDate[0]))

    lottoResults = re.findall("<Number>(.*?)</Number>", data, re.DOTALL)
    for num in lottoResults:
        print(num, end=" ")


def menu():
    pass

def quick_pick():
    qp_numbers = []
    for n in range(7):
        random_num = random.randint(1,47)
        if random_num not in qp_numbers:
            qp_numbers.append(random_num)
    bonus_num = qp_numbers[6]
    print("Your Quick Pick Card: ", qp_numbers)
    print("Bonus Number: ", bonus_num)

def manual_entry():
    pass
