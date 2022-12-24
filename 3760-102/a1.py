"""module docstring"""
import json
#from pickle import FALSE
#import array as arr
import random

#import urlib
import os

# from jmespath import search
from flask import Response

from flask import Flask, request, render_template

from search import parse_input

#import xml.etree.cElementTree as ET
import re
#import sys

# import lxml import etree

# import zipfile import ZipFile

# run virtual env
# . venv/bin/activate

APP = Flask(__name__)

#f = open('text.json', 'r')

"""
Homepage of your website.

Experimenting with HTTP status codes. You can change 201 to something else:

https://developer.mozilla.org/en-US/docs/Web/HTTP/Status

You can see the status code in your browser. Web Developer Tools --> Network tab.

Changing this to a code outside the 200s will "break" the javascript button
click ajax request. (Because the response is no longer success.)

https://stackoverflow.com/questions/7824101/return-http-status-code-201-in-flask

"""


def random_colour():
    """function to generate a random colour, used to assign different colours to events"""
    red = random.randint(30, 240)
    green = random.randint(30, 240)
    blue = random.randint(30, 240)

    # check if text should be black or white
    if red*0.299 + green*0.587 + blue*0.114 > 150:
        textColour = "black"
    else:
        textColour = "white"
    #rgb = "rgb({},{},{})".format(red, green, blue)
    rgb = f"rgb({red},{green},{blue})"
    return rgb + "|" + textColour


def convert_time(time):
    """function to convert time"""
    # is AM and first two elements are 12
    if time[-2:] == "AM" and time[:2] == "12":
        return "00" + time[2:-2]

    # remove the AM
    if time[-2:] == "AM":
        return time[:-2]

    # is PM and first two elements are 12
    if time[-2:] == "PM" and time[:2] == "12":
        return time[:-2]

    # add 12 to hours and remove PM
    return str(int(time[:2]) + 12) + time[2:5]


@APP.route('/')
def index():
    """renders index.html"""
    return render_template('index.html')


@APP.route('/getClasses', methods=['GET'])
def search():
    """get classes"""
    retStatus = 201
    search_val = request.values.get("searchFor")
    semester = request.values.get("semester")
    # excludedDay = request.values.get("dayOff[]")
    # size = len(request.values.get("dayOff[]"))
    monday = request.values.get("mon")
    tuesday = request.values.get("tues")
    wednesday = request.values.get("wed")
    thursday = request.values.get("thurs")
    friday = request.values.get("fri")
    lMonday = request.values.get("labMon")
    lTuesday = request.values.get("labTues")
    lWednesday = request.values.get("labWed")
    lThursday = request.values.get("labThurs")
    lFriday = request.values.get("labFri")

    kurtis = "Kurtis"

    if ("None" in monday):
        monday = kurtis
    if ("None" in tuesday):
        tuesday = kurtis
    if ("None" in wednesday):
        wednesday = kurtis
    if ("None" in thursday):
        thursday = kurtis
    if ("None" in friday):
        friday = kurtis

    if ("None" in lMonday):
        lMonday = kurtis
    if ("None" in lTuesday):
        lTuesday = kurtis
    if ("None" in lWednesday):
        lWednesday = kurtis
    if ("None" in lThursday):
        lThursday = kurtis
    if ("None" in lFriday):
        lFriday = kurtis

    lec1 = "LEC " + monday
    lec2 = "LEC " + tuesday
    lec3 = "LEC " + wednesday
    lec4 = "LEC " + thursday
    lec5 = "LEC " + friday
    lec6 = "LEC " + "Mon" + ", " + wednesday
    lec7 = "LEC " + "Mon" + ", " + "Wed" + ", " + friday

    lec8 = "LEC " + "Tues" + ", " + thursday
    lec9 = "LEC " + "Mon" + ", " + wednesday
    lec10 = "LEC " + "Mon" + ", " + friday
    lec11 = "LEC " + "Tues" + ", " + friday

    lab1 = "LAB " + lMonday
    lab2 = "LAB " + lTuesday
    lab3 = "LAB " + lWednesday
    lab4 = "LAB " + lThursday
    lab5 = "LAB " + lFriday
    lab6 = "LAB " + "Mon" + ", " + lTuesday
    lab7 = "LAB " + "Mon" + ", " + lWednesday
    lab8 = "LAB " + "Mon" + ", " + lThursday
    lab9 = "LAB " + "Mon" + ", " + lFriday
    lab10 = "LAB " + "Tues" + ", " + lWednesday
    lab11 = "LAB " + "Tues" + ", " + lThursday
    lab12 = "LAB " + "Tues" + ", " + lFriday
    lab13 = "LAB " + "Wed" + ", " + lThursday
    lab14 = "LAB " + "Wed" + ", " + lFriday
    lab15 = "LAB " + "Thur" + ", " + lFriday

    sem1 = "SEM " + lMonday
    sem2 = "SEM " + lTuesday
    sem3 = "SEM " + lWednesday
    sem4 = "SEM " + lThursday
    sem5 = "SEM " + lFriday

    returnStr = "["

    temp = parse_input(str(search_val), semester)

    print("tempppppppp", temp)

    if ("Could not find" not in temp):
        daysOff = json.loads(temp)

        for idx, obj in enumerate(daysOff):
            temp2 = json.dumps(obj)
            print("Searching through ", temp2)
            if (lec1 in temp2 or lec2 in temp2 or lec3 in temp2 or lec4 in temp2 or lec5 in temp2 or lec6 in temp2 or lec7 in temp2 or lec8 in temp2 or lec9 in temp2 or lec10 in temp2 or lec11 in temp2):
                returnStr = returnStr
            elif (lab1 in temp2 or lab2 in temp2 or lab3 in temp2 or lab4 in temp2 or lab5 in temp2 or lab6 in temp2 or lab7 in temp2 or lab8 in temp2 or lab9 in temp2 or lab10 in temp2 or lab11 in temp2 or lab12 in temp2 or lab13 in temp2 or lab14 in temp2 or lab15 in temp2 or sem1 in temp2 or sem2 in temp2 or sem3 in temp2 or sem4 in temp2 or sem5 in temp2):
                returnStr = returnStr
            else:
                if (returnStr != '['):
                    returnStr = returnStr + ',' + temp2
                else:
                    returnStr = returnStr + temp2
            # daysOff.pop(idx)
            # print("popped index = ", idx)
    else:
        retStatus = 500
    # temp1 = json.dumps(daysOff)

    returnStr = returnStr + "]"
    return Response(returnStr, retStatus)


@APP.route('/saveSelected', methods=['POST'])
def save():  # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    """called when a course is added"""
    name = request.values.get("name")
    term = request.values.get("term")
    capacity = request.values.get("capacity")
    status = request.values.get("status")
    faculty = request.values.get("faculty")
    credit = request.values.get("credit")
    level = request.values.get("level")
    location = request.values.get("location")
    meetings = request.values.get("meetings")

    bgAndTextColour = random_colour()
    colours = bgAndTextColour.split("|")
    bgColour = colours[0]
    textColour = colours[1]

    name_exists = 0

    name_arr = name.split(' ')
    # gets rid of things like (7164) in name string
    name_arr.pop(1)

    # create string again
    name = ' '.join(name_arr)

    # split formats into:
    # ['LEC Mon, Wed, Fri', '04:30PM - 05:20PM', 'LA, Room 204', 'LAB Wed', ...
    # '02:30PM - 04:20PM', 'THRN, Room 2420', 'EXAM Tues', '11:30AM - 01:30PM ...
    # (2022/12/13)', 'Room TBA']
    meeting_arr = meetings.split('\n')
    lec_time = ""
    lec_days = ""
    lec_s_time = ""
    lec_e_time = ""

    lab_day = ""
    lab_time = ""
    lab_s_time = ""
    lab_e_time = ""

    # if TBA is not found in lecture dates parse them further
    # convert times if they exist
    if meeting_arr[0].find('TBA') == -1 and len(meetings) != 0:
        lec_days = meeting_arr[0]
        lec_days = lec_days[4:]

        lec_time = meeting_arr[1].split(' - ')
        lec_s_time = convert_time(lec_time[0])
        lec_e_time = convert_time(lec_time[1])

    else:
        lec_days = "TBA"
        lec_s_time = "TBA"
        lec_e_time = "TBA"

    numbers = []

    if "Mon" in lec_days:
        numbers.append(1)
        # (numbers)

    if "Tues" in lec_days:
        numbers.append(2)
       # print(numbers)

    if "Wed" in lec_days:
        numbers.append(3)
        # print(numbers)

    if "Thur" in lec_days:
        numbers.append(4)
       # print(numbers)

    if "Fri" in lec_days:
        numbers.append(5)
        # print(numbers)

    if len(meeting_arr) > 3:
        # there's lab/seminar for class
        if meeting_arr[3].find('LAB') != -1 or meeting_arr[3].find('SEM') != -1:
            lab_day = meeting_arr[3]
            lab_day = lab_day[4:]

            lab_time = meeting_arr[4].split(' - ')
            lab_s_time = convert_time(lab_time[0])
            lab_e_time = convert_time(lab_time[1])
    # create dictionary
    dictionary = {
        "id": name,
        "title": name,
        "term": term,
        "capacity": capacity,
        "status": status,
        "faculty": faculty,
        "credit": credit,
        "level": level,
        "location": location,
        "lecDays": lec_days,
        "daysOfWeek": numbers,
        "startTime": lec_s_time,
        "endTime": lec_e_time,
        "labDay": lab_day,
        "lab_sTime": lab_s_time,
        "lab_eTime": lab_e_time,
        "backgroundColor": bgColour,
        "textColor": textColour

    }

    numbers = []

    if "Mon" in lab_day:
        numbers.append(1)
        # print(numbers)

    if "Tues" in lab_day:
        numbers.append(2)
        # print(numbers)

    if "Wed" in lab_day:
        numbers.append(3)
        # print(numbers)

    if "Thur" in lab_day:
        numbers.append(4)
       # print(numbers)

    if "Fri" in lab_day:
        numbers.append(5)
       # print(numbers)

    dictionary1 = {
        "id": name+" Lab",
        "title": name,
        "term": term,
        "capacity": capacity,
        "status": status,
        "faculty": faculty,
        "credit": credit,
        "level": level,
        "location": location,
        "daysOfWeek": numbers,
        "startTime": lab_s_time,
        "endTime": lab_e_time,
        "backgroundColor": bgColour,
        "textColor": textColour

    }

    # print(meetings)

    json_object = json.dumps(dictionary, indent=4)
    json_object1 = json.dumps(dictionary1, indent=4)
    with open("text.json", "r", encoding="utf8") as filehandle:
        content = filehandle.read()
        if name in content:
            name_exists = 1
        if bgColour in content:
            bgAndTextColour = random_colour()
            colours = bgAndTextColour.split("|")
            bgColour = colours[0]

    if name_exists == 0:
        with open("text.json", 'rb+') as filehandle:
            filesize = os.path.getsize("text.json")

            if (filesize != 0 & filesize != 2):
                filehandle.seek(-1, os.SEEK_END)
                filehandle.truncate()

        with open("text.json", "a", encoding="utf8") as outfile:
            filesize = os.path.getsize("text.json")

            if filesize == 0:
                outfile.write("["+json_object + "]")
            elif filesize < 10:
                outfile.write(json_object + "}")
            else:
                outfile.write(","+json_object + "]")
        # -------------------
        with open("text.json", 'rb+') as filehandle:
            filesize = os.path.getsize("text.json")
            if filesize != 0:
                filehandle.seek(-1, os.SEEK_END)
                filehandle.truncate()

        with open("text.json", "a", encoding="utf8") as outfile:
            filesize = os.path.getsize("text.json")

            if filesize == 0:
                outfile.write("["+json_object1 + "]")

            else:
                outfile.write(","+json_object1 + "]")
    json_object3 = json_object + " | " + json_object1
    return Response(json_object3, status=201)
    # else:
    #     return Response("repeat class", status=201)


@APP.route('/readJSON', methods=['GET'])
def readJSON():  # pylint: disable=invalid-name
    """read json"""
    data = {'name': 'empty'}
    filesize = ""
    # open for reading create file if not exists
    with open('text.json', 'a', encoding='utf-8') as file1:
        filesize = os.path.getsize("text.json")

    # read file if not empty and send json data
    if filesize != 0:
        with open('text.json', 'r', encoding='utf-8') as file1:
            data = json.loads(file1.read())

    data = json.dumps(data)
    return Response(data, status=201)


@APP.route('/deleteJSON', methods=['DELETE'])
def deleteJSON():  # pylint: disable=invalid-name
    """delete event from json"""
   # print("in deleteJSON\n")
    name = request.values.get("title")
    with open('text.json', 'r', encoding='utf-8') as file1:
        my_list = json.load(file1)
        # print(my_list)
        for idx, obj in enumerate(my_list):
           # print(name)
            # print(obj['title'])
            if obj['title'] == name:
                my_list.pop(idx)
        for idx, obj in enumerate(my_list):
            # print(name)
           # print(obj['title'])
            if obj['title'] == name:
                my_list.pop(idx)

    with open('text.json', 'w', encoding='utf-8') as file1:
        file1.write(json.dumps(my_list, indent=4))

    return Response()


@APP.route('/emptyFile', methods=['POST'])
def emptyFile():  # pylint: disable=invalid-name
    """empty file"""
    with open("text.json", "w", encoding="utf8") as file1:
        file1.close()

    return Response()


if __name__ == '__main__':
    APP.run(debug=True)
