from etherscan import Etherscan
import time
import csv

#This is your API Key from Etherscan.
with open('apikey', 'r') as file:
    apiKey = file.read().replace('\n', '')
    
#Open the address list file. Delimited by new line
addrList = open("addresslist" , "r")
#Counts amount of lines in the address list
addrLine = addrList.readlines()

#Initiate Eth Api
eth = Etherscan(apiKey)

def main():

    print("\n \n" + str(len(addrLine)) + " Address's found \n \n \n")
    #Current Addr Line
    addrCur = 0
    apiCallCount = 0
    apiSleepCount = 5 #Sleep every 5 api actions.
    apiSleepTime = 0 #Sleep Time period.

    #initialize csv output
    output_file = open('output.csv', mode='w',newline='') 
    file_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #write initial row
    file_writer.writerow(['Eth Balance','Address','Etherscan','Opensea'])
        
    #This will loop and execute an action for each line of the address list.
    for line in addrLine:
      
        addrCur += 1
        #print current position and address
        
        ethBalance = convEth(eth.get_eth_balance(line.strip()))
        addrOut = line.strip()
                
        print("Address #" + str(addrCur) +": " + addrOut)
        
        #api is called once.
        apiCallCount += 1 #increment apiCallCount
        
        #print eth balance
        print ("Eth Balance: " + str(ethBalance) + "\n")
        #write address and eth value to csv 
        file_writer.writerow([ethBalance,addrOut,"""=HYPERLINK("https://etherscan.io/address/"""+str(addrOut) + """")""","""=HYPERLINK("https://opensea.io/"""+str(addrOut) + """")"""])
           

    addrList.close()
    print("\n //////// \n Finished \n //////// \n")

    
def convEth(ethIn, n=18):

    if len(ethIn) == n:
            return "0." + str(ethIn)
    elif len(ethIn) == n-1:
            return "0.0" + str(ethIn)
    elif len(ethIn) == n-2:
            return "0.00" + str(ethIn)
    elif len(ethIn) < n-2:
            return "0" #under 0.00 eth rounding to 0
    elif len(ethIn) > 18:
        ethRev = ethIn[::-1]
        ethOut = '.'.join(ethRev[i:i+n] for i in range(0, len(ethRev), n))
        ethOutF = ethOut[::-1]
        return ethOutF
    

main()