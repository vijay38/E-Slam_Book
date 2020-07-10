from pymongo import MongoClient
from bson.objectid import ObjectId

client=MongoClient("mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false")

mongodb=client.get_database("Fill_up_form")

mongocoll=mongodb.slambook

l=list(mongocoll.find({"userid":"5f06ff49c8f4d137b280726b"}))

print(l)
#mongocoll.insert_one(data)

#l=list(mongocoll.find({"_id":ObjectId('5f007e8cb7a11d1511d21637')}))
client.close()
