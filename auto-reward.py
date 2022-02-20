import csv
import os

# ---------------------------------- Arguments ----------------------------------

INPUT_CSV = 'rewardData.csv'
TOKEN_HEX = '4D45582D616232363261'
PEM = 'wallet-owner.pem'
GAS_LIMIT = str(400000)
PROXY = 'https://devnet-gateway.elrond.com'
CHAIN = 'D'

# ---------------------------------- Functions ----------------------------------

# Convert a csv MEX value to elrond compatible hex value
def elrondHex(decstr):
	hval = str(hex(int(decstr))).replace("0x", "")
	if( len(hval)%2==1 ):
		hval = '0' + hval
	return hval

# Builds an erdpy transaction using the given arguments
def buildErdTx(addr, amount):
	return 'erdpy tx new' + \
	' --pem ' + PEM + \
	' --recall-nonce' + \
	' --receiver ' + addr + \
	' --value 0' + \
	' --gas-limit ' + GAS_LIMIT + \
	' --send' + \
	' --wait-result' + \
	' --outfile ' + './reports/' + addr + '.report.json' + \
	' --proxy ' + PROXY + \
	' --chain ' + CHAIN + \
	' --data ' + 'ESDTTransfer@' + TOKEN_HEX + '@' + elrondHex(amount)

# -------------------------------------------------------------------------------

# Open and parse the csv file
file = open(INPUT_CSV)
csvreader = csv.reader(file)
rows = []
for row in csvreader:
	rows.append(row)

# Create the reports directory
os.system("mkdir reports")

# Distribute the rewards
print("\n (i) Distributing rewards to Investors...")
for i, row in enumerate(rows):
	print("\n  " + str(i+1) + ". " + row[0] + " - " + row[1] + " MEX")
	os.system( buildErdTx( row[0], row[1]) )

print( "\n (i) Reward distribution complete\n")
