from requests import get
import random
import time
from collections import defaultdict
import pymongo

codeforces_usernames = defaultdict(str)
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
collection = mydb["Users"]
extension = 'https://codeforces.com/api/'

def request_link_user(username):
	req = extension+'user.info?'+'handles='+username
	res = get(req)
	json_data = res.json()
	if json_data['status'] == 'FAILED':
		return (0, json_data['comment'])
	else:
		val = ''
		for i in range(10):
			val += str(random.randint(0, 9))
		message = "Please change you first name to "+val+" in 60 seconds"
		return (1, message, val)

def link_user(username, codeforces, val):
	t = time.time()
	while True:
		time.sleep(1)
		if time.time() - t > 60:
			return 0
		req = extension+'user.info?'+'handles='+codeforces
		res = get(req)
		json_data = res.json()

		if 'firstName' in json_data['result'][0] and json_data['result'][0]['firstName'] == val:
			codeforces_usernames[username] = codeforces
			return 1

def insert_user(discord, codeforces):
	discord = str(discord)
	arr = collection.find({"Code":codeforces})
	if len(list(arr)) == 0:
		req = extension + "user.status?" + "handle=" + codeforces
		data = get(req).json()
		solved = set()
		for x in data['result']:
			if x['verdict'] == 'OK':
				if 'contestId' in x['problem']:
					solved.add(str(x['problem']['contestId']) + x['problem']['index'])
				else:
					solved.add(str(x['problem']['problemsetName']) + x['problem']['index'])

		solved = list(solved)
		collection.insert_one({"User":discord, "Code":codeforces, "Solved":solved})


def get_problemset(arr):
	if len(arr) == 1:
		arr += [arr[-1]]

	req = extension + 'problemset.problems'
	problems = get(req).json()
	valid = []
	for x in problems['result']['problems']:
		if 'rating' in x and x['rating'] >= int(arr[0]) and x['rating'] <= int(arr[1]):
			valid += [x]
	return valid


def get_problem(discord, arr):
	user = list(collection.find({"User":discord}))
	if len(user) == 0:
		solved = []
	else:
		solved = user[0]['Solved']

	valid = get_problemset(arr)

	while True:
		ret = random.choice(valid)
		ide = str(ret['contestId']) + ret['index']
		if ide not in solved:
			break

	ext = 'https://codeforces.com/problemset/problem/'
	return ext + str(ret['contestId']) + '/' + ret['index']


def get_virtual(discord):
	user = list(collection.find({"User":discord}))
	if len(user) == 0:
		return -1

	req = extension+'user.info?'+'handles='+user[0]['Code']
	user = get(req).json()
	problems = []
	rating = user['result'][0]['rating']//100 * 100
	valid = get_problemset([rating])
	user = list(collection.find({"User":discord}))
	solved = user[0]['Solved']
	ext = 'https://codeforces.com/problemset/problem/'


	for i in range(5):
		while True:
			ret = random.choice(valid)
			ide = str(ret['contestId']) + ret['index']
			if ide not in solved and ext + str(ret['contestId']) + '/' + ret['index'] not in problems:
				break

		problems += [ext + str(ret['contestId']) + '/' + ret['index']]

	return problems

