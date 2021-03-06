import requests
import os
import sys
import json
from todoist.api import TodoistAPI

canvasCourses = {}


def loadKeys(reset=False):
    if not open("keys.txt", "r"):
        canvasKey, todoistKey, courseID = getInfo()
        keys = {"Canvas": canvasKey,
                "Todoist": todoistKey,
                "Courses": courseID}
        with open("keys.txt", "w") as file:
            json.dump(keys, file)
    if reset:
        resetClasses()


def resetClasses():
    with open("keys.txt", "r") as file:
        keys = json.load(file)
    courseID = listCourses(keys["Canvas"])
    keys['Courses'] = courseID
    with open("keys.txt", "w") as file:
        json.dump(keys, file)


def getInfo():
    canvasKey = ""
    todoistKey = ""

    while not canvasKey:
        usrKey = input("Paste your Canvas API key here: ").strip()
        check = requests.get("https://canvas.instructure.com/api/v1/courses",
                             headers={"Authorization": "Bearer "+usrKey})
        if check.ok:
            canvasKey = usrKey
        else:
            print("Could not make connection. Check API key")

    while not todoistKey:
        usrKey = input("Paste your Todoist API key here: ").strip()
        api = TodoistAPI(usrKey)
        if 'error' not in api.sync():
            todoistKey = usrKey
        else:
            print("Could not make connection. Check API key")
    courseID = listCourses(canvasKey)
    return canvasKey, todoistKey, courseID


def listCourses(canvasKey):
    courseIDs = {}

    API_KEY = canvasKey
    header = {"Authorization": "Bearer " + API_KEY}
    parameter = {'per_page': 9999}

    courseList = requests.get(
        'https://canvas.instructure.com/api/v1/courses', headers=header, params=parameter).json()
    for index, name in enumerate(courseList):
        try:
            print(str(index+1) + ".)", name['name'])
        except:
            continue
    userIn = int(
        input("Enter number of course you would like to sync (Enter -1 when done): "))
    while userIn != -1:
        try:
            if courseList[userIn-1]:
                courseIDs[courseList[userIn-1]["id"]
                          ] = [courseList[userIn-1]["name"], "0"]
        except:
            print("Entry out of range")
        userIn = int(
            input("Enter number of course you would like to sync (Enter -1 when done): "))
    return courseIDs


if __name__ == "__main__":
    if sys.argv[-1] == "-r":
        loadKeys(True)
    else:
        loadKeys()
