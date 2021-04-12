from pymongo import *

client = MongoClient("mongodb+srv://admin:admin123@cluster0.ze4na.mongodb.net/myFirstDatabase",connect=False)
db = client['IOT']
TexDB = db['user_details']
mydict = {'userid':'gty', 'name': 'gty', 'password': 'hyyrr'}
x = TexDB.insert_one(mydict)
print(x)