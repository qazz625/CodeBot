import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
collection = mydb["Users"]

if collection.count_documents({}) == 0:
	collection.insert_one({"User":"Dummy", "Code":"Dummy", "Solved":[]})

