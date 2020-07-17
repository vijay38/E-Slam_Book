from django.shortcuts import render
from django.http import HttpResponse
from pymongo import MongoClient
from bson.objectid import ObjectId
import random
import pyrebase
from .forms import GeeksForm
import os
import dotenv
# Create your views here.
#def home(request):
#    return render(request,"Slamform.html")
dotenv.load_dotenv()

def thanks(request,id):
    qnum=request.POST["questions"]
    qnum=list(map(int,qnum.split("-")))
    data={}
    data["userid"]=id
    print(os.getenv("mongolink"))
    client=MongoClient(os.getenv("mongolink"))
    mongodb=client.get_database("Fill_up_form")
    mongocoll=mongodb.questions
    l=list(mongocoll.find({},{"_id":0}).sort("num"))
    
    data["Name"]=request.POST["name"]
    data["Nickname"]=request.POST["nickname"]
    data["Address"]=request.POST["address"]
    data["Ring me on"]=request.POST["ring"]
    data["Born on"]=request.POST["dob"]
    data["Zodiac Sign"]=request.POST["zodiac"]
    
    c=1
    for i in qnum:
        data[l[i-1]["question"]]=request.POST["q"+str(c)]
        c+=1
    data["About you I feel"]=request.POST["about"]
    data["Date"]=request.POST["date"]
    data["image"]=request.POST["url"]
    mongocoll=mongodb.slambook
    mongocoll.insert_one(data)
    client.close()
    return render(request,"thanks.html")

def homes(request,id):
    print(os.getenv("mongolink"))
    client=MongoClient(os.getenv("mongolink"))
    mongodb=client.get_database("Fill_up_form")
    mongocoll=mongodb.users
    if len(id)!=24:
        return render(request,"invalid.html")
    userlist=list(mongocoll.find({"_id":ObjectId(str(id))}))
    if userlist==[]:
        return render(request,"invalid.html")
    txn=userlist[0]["txnstatus"]
    gender=userlist[0]["gender"]
    uname=userlist[0]["username"]
    if txn==False:
        mongocoll=mongodb.slambook
        count=len(list(mongocoll.find({"userid":id})))
        if count>=5:
            return render(request,"free.html")
    mongocoll=mongodb.questions
    l=list(mongocoll.find({},{"_id":0}).sort("num"))
    client.close()
    choices=list(range(20))
    random.shuffle(choices)
    random_list=choices[:10]
    display={}
    c=1
    toget=""
    for i in random_list:
        display["q"+str(c)]=l[i]["question"]
        toget+=str(l[i]["num"])+"-"
        c+=1
    display["q11"]=toget[:-1]
    display["q12"]=id
    display["gender"]=gender
    display["uname"]=uname
    display["male"]="male"
    #display['form']=GeeksForm()
    return render(request,"Slamform.html",display)