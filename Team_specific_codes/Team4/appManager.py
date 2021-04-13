from flask import Flask,render_template,url_for,request,redirect
import json
import os
import zipParsing
from zipfile import ZipFile
import csv
from kafka import KafkaConsumer, KafkaProducer
import json
import threading
from _thread import *
import time
import comm_module as cm

curpath=str(os.path.dirname(os.path.realpath(__file__)))
#create repository directory if not present
reposPath = curpath+"/Applications"
if not os.path.isdir(reposPath):
    os.mkdir(reposPath)

#read credentials into set
userCredSet = set()
if os.path.isfile("platformUserCreds.txt"):
    with open("platformUserCreds.txt","r") as file:
        for line in file:
            lst = line.strip().split(",")
            if len(lst) < 4:
                break
            tup = tuple([lst[0],lst[2],lst[3]])
            userCredSet.add(tup)

schedule_json_lst = ["start_time","end_time","request_type","priority","days","interval","duration"]
other_feilds_lst = ["userID","appID","algoID","form","location","devID","sensorList"]

app = Flask(__name__)

'''@app.route('/')
def index():
    return render_template("signup.html")'''

def registerUser(instance):
    with open('platformUserCreds.txt', mode='a+') as file:
        line = ""
        for key in instance:
            line += instance[key] + ","
        lst = line[:-1].split(",")
        tup = tuple([lst[0],lst[2],lst[3]])
        userCredSet.add(tup)
        file.write(line[:-1]+"\n")            


@app.route("/signup",methods=["GET","POST"])
def sign_up():
    if request.method=="POST":
        data=request.form
        req=dict(data)
        # keys of dict are username, email,pwd
        registerUser(req)
        # redirect to login
        return redirect("/login")
    return render_template("sign_up.html")


def validateUser(instance):
    line = ""
    for key in instance:
        line += instance[key] + ","
    lst = line[:-1].split(",")
    tup = tuple([lst[0],lst[2],lst[1]])
    if tup in userCredSet:
        return True
    else:
        return False



@app.route("/")
@app.route("/login",methods=["GET","POST"])
def login():
	if request.method=="POST":
		#print("Got login request")
		data=request.form
		req=dict(data)

		valid = validateUser(req)

		if valid:
			if req["dname"]=="Developer":
				return redirect(url_for('upload', usrname=req["user_id"]))
			else:
				return redirect("/fill-form")
		else:
			return "not a valid user, please signup first"

	return render_template("login.html")


def storeInRepo(username,zipPath):
    userRepoPath = reposPath + "/"+username
    if not os.path.isdir(userRepoPath):
        os.mkdir(userRepoPath)
    with ZipFile(zipPath, 'r') as zipObj:
        zipObj.extractall(userRepoPath)
    os.remove(zipPath)


# uploading the developer file to a directory
@app.route("/<usrname>/upload",methods=["GET","POST"])
def upload(usrname):
    if request.method == "POST":
        
        file=request.files['file']
        if not os.path.isdir(curpath+"/temp_zips"):
            os.mkdir(curpath+"/temp_zips")
        file.save(os.path.join(curpath+"/temp_zips", file.filename))
        zip_path=os.path.join(curpath+"/temp_zips", file.filename)
        valid = zipParsing.processZip(zip_path)
        if valid:
            storeInRepo(usrname,zip_path)
            return "Application is successfully deployed!"
        # upload to directory structure i.e mongo db in our case
        else:
            return "Errorrrrr!"

    return render_template("upload.html",username = usrname)

def get_schedule_dict(dict1):
    dict = {}
    for entry in schedule_json_lst:
        dict[entry] = dict1[entry]
    return dict

def get_dict(dict1):
    dict = {}
    dict["schedule"] = get_schedule_dict(dict1)
    for entry in other_feilds_lst:
        if entry == "sensorList":
            dict[entry] = dict1[entry].split(",")
            continue
        dict[entry] = dict1[entry]
    configPath = reposPath + "/" + dict["devID"] + "/" +dict["appID"] + "/" + dict["algoID"] +"/config.json"
    
    with open(configPath,"r") as file:
        x = json.load(file)
        dict["RAM"] = x["RAM"]
        dict["CPU"] = x["CPU"]
    return dict

@app.route("/fill-form",methods=["GET","POST"])
def fill_form():
    import comm_module as cm
    if request.method=="POST":
        data=request.form
        req=dict(data)
        msg = get_dict(req)
        print(msg)

        cm.send_message("AS",msg)

        return "Request Submitted"

    return render_template("service_request_form.html")
		

	



app.run(debug = True)