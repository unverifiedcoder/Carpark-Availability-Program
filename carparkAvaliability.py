print("Loading Application...")
import time
start = time.time()

import requests
import os
import math

print("Fetching requests from server...")

url = 'https://api.data.gov.sg/v1/transport/carpark-availability'

def startup():
    response = requests.get(url)
    data = response.json()
    for i in data['items'][0]['carpark_data']:
        new = Carpark()
        new.cpNum = i['carpark_number']
        new.totalLots = i['carpark_info'][0]['total_lots']
        new.lotType = i['carpark_info'][0]['lot_type']
        new.lotsAvaliable = i['carpark_info'][0]['lots_available']
        new.updateDT = i['update_datetime']
        allData.append(new)

def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

allData = []

class Carpark():
    def __init__(self):
        cpNum = 0
        totalLots = 0
        lotType = 0
        lotsAvaliable = 0
        updateDateTime = 0

startup()

print(f'Loading took {math.ceil(time.time() - start)} second(s)!')
time.sleep(2)
clear()

quit = False
searchHistory = []

with open('carparkAvailability\searchHistory') as shTestFile:
    searchHistory = [i.strip() for i in shTestFile.readlines()]

print(searchHistory)

def main():
    clear()
    print("Singapore Carpark Availability Program")
    print('Checks for carpark availability of all carparks in Singapore in real time.')
    print('-------------\n')
    print('Selections:')
    print('[1] Search for Specific Carpark')
    print('[6] Refresh Data')
    print('[7] Clear Search History')
    print('[8] Credits')
    print('[9] Quit Program')
    
    query = input('Enter selection: ')
    clear()
    if query == '1':
        search = 'null'
        while search != '':
            print("Previous Search Queries:")
            if len(searchHistory) > 0:
                for i in searchHistory:
                    print(i)
                print()
            else:
                print("[No recent search queries.]\n\n-------------\n\n")
            
            search = input("Enter Carpark Code\n-------------\n\nLeave search query blank to exit search & return to menu.\nSearch: ")
            if search != '' and len(search) <= 4:
                if search not in searchHistory:
                    searchHistory.append(search)
                results = []
                directFound = False
                for i in allData:
                    if i.cpNum == search.upper():
                        clear()
                        print(f'Information about Carpark {i.cpNum}:')
                        print('-------------\n')
                        print(f'Lots Available: {i.lotsAvaliable}')
                        print(f'Total Lots: {i.totalLots}')
                        percentage = math.floor(100 * (int(i.lotsAvaliable) / int(i.totalLots)))
                        print(f'Lots Availability Percentage: {percentage}%')
                        date, Time = i.updateDT.split('T')
                        print(f'Last updated: {date} {Time}')
                        input("Enter to continue. ")
                        directFound = True
                        break
                    elif search.upper() in i.cpNum:
                        results.append(i.cpNum)

                if not directFound:
                    clear()
                    if len(results) < 1:
                        input("No Results Found\n-------------\n\nEnter to continue. ")
                    elif len(results) == 1:
                        clear()
                        print(f"No Direct Result(s) Found\n-------------\n\nPerhaps you were trying to search for:\n{results[0]}?\nIf so, here's more information about carpark {results[0]}:\n-------------\n")
                        for i in allData:
                            if i.cpNum == results[0]:
                                print(f'Information about Carpark {i.cpNum}:')
                                print('-------------\n')
                                print(f'Lots Available: {i.lotsAvaliable}')
                                print(f'Total Lots: {i.totalLots}')
                                percentage = math.floor(100 * (int(i.lotsAvaliable) / int(i.totalLots)))
                                print(f'Lots Availability Percentage: {percentage}%')
                                date, Time = i.updateDT.split('T')
                                print(f'Last updated: {date} {Time}')
                                input("Enter to continue. ")
                    else:
                        newResults = []
                        for i in results:
                            v = search.upper()
                            if i[0:len(search)] == v[0:len(search)]:
                                newResults.append(i)

                        if len(newResults) == 0:
                            print("No Direct Result(s) Found\n-------------\n\nPerhaps you were trying to search for:")
                            results.sort()
                            for i in range(len(results)):
                                if i == len(results) - 1:
                                    print(results[i], end='?')
                                else:
                                    print(results[i], end=', ')
                        else:
                            print("No Direct Result(s) Found\n-------------\n\nPerhaps you were trying to search for:")
                            newResults.sort()
                            for i in range(len(newResults)):
                                if i == len(newResults) - 1:
                                    print(newResults[i], end='?')
                                else:
                                    print(newResults[i], end=', ')
                       

                        print()
                        input("\n-------------\nPlease re-enter your desired carpark number into the search query and try again.\nEnter to continue. ")
            elif len(search) > 4:
                clear()
                input('Invalid Carpark Number\nCarpark numbers should are only 4 characters maximum in length.\n-------------\n\nPlease enter a vaild carpark number.')  
            
            clear()
            with open('carparkAvailability\searchHistory', 'w') as shTestFile:
                for i in searchHistory:
                    shTestFile.writelines(i+'\n')

    elif query == '6':
        start = time.time()
        print("Fetching new requests from server...")  
        startup()
        input(f'Loading took {math.ceil(time.time() - start)} second(s)!\n-------------\n\nEnter to continue. ')
    elif query == '7':
        searchHistory.clear()
        input('Search History Cleared\n-------------\n\nEnter to continue. ')
    elif query == '8':
        print(f'Credits\n-------------\n\nAPI Data Source: {url}')
        input('\n-------------\n\nEnter to continue. ')
    elif query == '9':
        return True
    else:
        input('Error Encountered\n-------------\n\nSelection not valid nor found. Enter to continue. ')
    
    return False

while not quit:
    quit = main()
    try:
        #quit = main()
        pass
    except:
        clear()
        input('Error Encountered\n-------------\n\nSomething went wrong. Enter to continue. ')

clear()
print("Quitting program...\nThank you for using Singapore Carpark Availability Program!")