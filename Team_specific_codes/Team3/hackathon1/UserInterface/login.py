#!/usr/bin/env python3

'''initial program to application developer to check login and upload algorithms
author : rbachina
date : 14 mar 2021
purpose : team hackathon
'''
import os
import pymongo
from pymongo import MongoClient
from subprocess import call
from bson.objectid import ObjectId


client = MongoClient("mongodb+srv://admin:admin123@cluster0.ze4na.mongodb.net")
db = client['IOT']
userTable = db['user_details']


def __copy_alg_to_repo__(destinationDir):
    print(" \n")
    sourceDir = input("Provide source directory/folder: ")
    call(['cp', '-r', sourceDir, destinationDir])
    print("Algorithm is hosted now")
    __app_dev_operations__()


def __list_all_alg__(algRepPath):
    __repo_exist__(algRepPath)
    my_algorithms = os.listdir(algRepPath)
    i = 0
    print("*******List of algorithsm*******")
    for alg in my_algorithms:
        i = i+1
        print("algorithm"+str(i)+": "+alg)


def __delete_alg__(dirNameWithFullPath):
    try:
        os.rmdir(dirNameWithFullPath)
        print("algorithm removed successfully")
    except OSError as error:
        print(error)
        print("Error deleting the algorithm")


def __repo_exist__(algRepPath):
    isExist = os.path.exists(algRepPath)
    if not isExist:
        print("creating dir now")
        os.makedirs(algRepPath)


def __upload_algorithm__(algRepPath):
    __repo_exist__(algRepPath)
    __copy_alg_to_repo__(algRepPath)


def __validation__(userName, password):

    for x in userTable.find({'userid': userName, 'password': password}):
        print(x)

    if x.get('password', None) != password:
        print("please enter proper credentials, userid/password wrong")
        login()
    else:
        print("login successful")
        __app_dev_operations__()


def __newUser_registration__(userName, name, password):
    x = userTable.find({"_id": userName})
    if x is not None:
        print('Username already exists')
        return
    mydict = {'_id': userName, 'name': name, 'password': password}
    x = userTable.insert_one(mydict)
    print(x)


def __app_dev_operations__():
    print('Select "1" to upload algorithm \n')
    print('Select "2" list the algorithms from repo \n')
    print('Select "3" delete algorithms from repo \n')
    print('Select "4" to logout and exit \n')
    devChoice = input("Choice: ")
    homePath = os.environ['HOME']
    algRepPath = homePath+"/AlgorithmRepo"
    if devChoice == "1":
        __upload_algorithm__(algRepPath)
    elif devChoice == "2":
        __list_all_alg__(algRepPath)
        __app_dev_operations__()
    elif devChoice == "3":
        __list_all_alg__(algRepPath)
        deleteDirName = input("Enter Dir Name: ")
        dirNameWithFullPath = algRepPath+'/'+deleteDirName
        __delete_alg__(dirNameWithFullPath)
        __list_all_alg__(algRepPath)
        __app_dev_operations__()
    elif devChoice == "4":
        exit()
    else:
        print("please select appropriate choice")
        __app_dev_operations__()


def registration():
    userName = input("Enter Username: ")
    name = input("Enter Full Name: ")
    password = input("Enter Password: ")
    print(userName + "\n" + name + "\n" + password)
    __newUser_registration__(userName, name, password)
    print("registration successful")
    print("Now please login with your credentials \n")
    login()


def login():
    userName = input("Enter Username: ")
    password = input("Enter password: ")

    __validation__(userName, password)
    __app_dev_operations__()


def main():
    print('****************Welcome to IOT Platform****************')
    print('Please enter appropriate action from below choice \n')
    print('Select "1" for new user registration \n')
    print('Select "2" for existing user login \n')
    print('Select "3" to exit')
    userChoice = input("Choice: ")

    if userChoice == "1":
        registration()
    elif userChoice == "2":
        login()
    elif userChoice == "3":
        exit()
    else:
        print("please select appropriate choice")


if __name__ == "__main__":
    main()
