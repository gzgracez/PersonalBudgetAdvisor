import requests
import json

apiKey = "638e3a40768577cc14440e93f78f7085"

def getAccountBalance():
	accountsUrl = 'http://api.reimaginebanking.com/accounts?key={}'.format(apiKey)
	accountsResponse = requests.get(accountsUrl)
	if accountsResponse.status_code == 200:
		accounts = json.loads(accountsResponse.text)
	return accounts

if __name__=="__main__":
    print getAccountBalance()