"""search"""
# from curses.ascii import NUL
# from operator import truediv
# import pathlib
# from pickle import TRUE
from zipfile import ZipFile
import json
import xml.etree.ElementTree as ET
import re
import sys as system
from lxml import etree

# Not used right now
# class color:
#    """colours"""
#    BOLD = '\033[1m'
#    END = '\033[0m'
#    GREEN = '\033[92m'
#    RED = '\033[91m'


def parseschedule(sectionnum_element, meetingsdiv):
    """parsing the schedule"""
    schedulestring = ''
    meetings = meetingsdiv.findall("div")
    for meet in meetings:
        lines = meet.findall("div")
        for line in lines:
            # If the line includes a link handle it differently
            if line.find("a") is not None:
                schedulestring += line.find("a").text
                # Just using line.text doesn't work since there is also an <a> tag
                schedulestring += "".join(
                    text for text in line.xpath("text()")) + '\n'
            else:
                schedulestring += line.text + '\n'

    # Strip the extra newline character an the end of the string
    sectionnum_element.set("meetings", schedulestring.rstrip())


def parse_html():  # pylint: disable=too-many-locals
    """parse the html file"""
    parser = etree.HTMLParser()
    tree = etree.parse(
        'Section Selection Results WebAdvisor University of Guelph.html', parser)
    root = tree.getroot()
    table = root.find(
        "./body/div[3]/div/div[1]/div[3]/form/table/tbody/tr/td/div/table/tbody/tr[2]/td \
        /div/table/tbody")

    xmlroot = ET.Element("courses")
    currentdepartment = ""
    currentcoursenum = ""
    currentdepartment_element = ET.Element("")
    currentcoursenum_element = ET.Element("")

    # Iterate through each course in the table, first two lines are headers
    for count in range(2, len(table)):
        row = table[count]
        fullcoursecode = row[3][0][0].text.split(' ')[0].split('*')
        department = fullcoursecode[0]
        coursenum = fullcoursecode[1]
        sectionnum = fullcoursecode[2]

        # Since courses are ordered, only need to add a new dept/coursenum when they change
        if department != currentdepartment:
            currentdepartment = department
            currentdepartment_element = ET.Element(currentdepartment)
            xmlroot.append(currentdepartment_element)

        if coursenum != currentcoursenum:
            currentcoursenum = coursenum
            currentcoursenum_element = ET.Element('c' + currentcoursenum)
            currentdepartment_element.append(currentcoursenum_element)

        sectionnum_element = ET.Element('s' + sectionnum)
        sectionnum_element.set("term", row[1][0][0].text)
        sectionnum_element.set("status", row[2][0][0].text)
        sectionnum_element.set("name", row[3][0][0].text)
        sectionnum_element.set("location", row[4][0][0].text)
        sectionnum_element.set("faculty", row[6][0][0].text)
        sectionnum_element.set("capacity", row[7][0][0].text)
        sectionnum_element.set("credits", row[8][0][0].text)
        sectionnum_element.set("level", row[10][0][0].text)
        parseschedule(sectionnum_element, row[5][0])
        currentcoursenum_element.append(sectionnum_element)

    xmltree = ET.ElementTree(xmlroot)
    ET.indent(xmltree)
    xmltree.write("parsed.xml")


def print_course_json(course):
    """returns course info"""
    term = course.get('term')
    status = course.get('status')
    name = course.get('name')
    location = course.get('location')
    meetings = course.get('meetings')
    meetings = meetings.strip()
    faculty = course.get('faculty')
    capacity = course.get('capacity')
    credit = course.get('credits')
    level = course.get('level')

    tmp = {
        "name": name,
        "term": term,
        "capacity": capacity,
        "status": status,
        "faculty": faculty,
        "credit": credit,
        "level": level,
        "location": location,
        "meetings": meetings
    }

    temp = json.dumps(tmp, indent="\t")
    return temp

# Lists the attributes from a section of a course


def print_course_table(course):
    """returns course table"""
    # commented out if not used - pylint
    term = course.get('term')
    status = course.get('status')
    name = course.get('name')
    # location = course.get('location')
    meetings = course.get('meetings')
    meetings = meetings.strip()
    faculty = course.get('faculty')
    # capacity = course.get('capacity')
    # credit = course.get('credits')
    # level = course.get('level')

    # create python dictionary - unused right now
    # tmp = {
    #    "name": name,
    #    "term": term,
    #    "capacity": capacity,
    #    "status": status,
    #    "faculty": faculty,
    #    "credit": credit,
    #    "level": level,
    #    "location": location,
    #    "meetings": meetings
    # }

    # format into table string
    temp = '<tr>' + '<td>' + name + term + '</td>' + '<td>' + meetings + \
        '</td>' + '<td>' + faculty + '</td>' + '<td>' + status + '</td>' + \
        '<td><button type=\"button\" class=\"btn btn-success btn-sm\"><i class=\" \
        bi bi-plus-lg style="--bs-btn-padding-y: .25rem; --bs-btn-padding-x: .5rem; \
        --bs-btn-font-size: .75rem;"\"></i></button></td>' + '</tr>'

    return temp


def print_course(course):
    """prints course info"""
    # commented out if not used - pylint
    # term = course.get('term')
    status = course.get('status')
    # name = course.get('name')
    location = course.get('location')
    meetings = course.get('meetings')
    meetings = meetings.strip()
    faculty = course.get('faculty')
    # capacity = course.get('capacity')
    credit = course.get('credits')
    level = course.get('level')

    # print('\n' + color.BOLD + name + '\t' + term +
    # color.END + '\t' + capacity,  end=" ")
    if status == 'Open':
        print("check")
       # print(color.BOLD + color.GREEN + status + color.END, end=" ")
        # else:
        # print(color.BOLD + color.RED + status + color.END, end=" ")
    print('\n' + faculty + '\t' + credit + '\t' +
          level + '\t' + location + '\n' + meetings + '\n')


def find_courses(path,semester):
    #print(path)
    """ Lists all the sections of a course, given a path. Ex. ./CIS/c2750"""
    tree = ET.parse(semester+'.xml')
    root = tree.getroot()

    # temp ='<table class=\"table text-white table-hover\"><tbody>'
    temp = "["
    list_json = []

    # go through all the path(s) (findClasses returns a list of paths)
    # and get JSON formatting if it exists
    for count in path:
        if not root.findall(count):
            return "\nCould not find course, please try again.\n"
        for courses in root.findall(count):
            print(courses)
            for child in courses:
                # array of JSON strings, will format into proper JSON array after
                list_json.append(print_course_json(child))

    # create proper JSON string array
    for course in list_json:
        temp += course + ','

    # get rid of ',' at the end of list and add ']'
    # temp += ' </tbody></table> '
    temp = temp[:-1]
    temp += "]"
    print(temp)

    return temp


def find_classes(path,semester):
    """Lists all the classes if the user did not specify what class"""
    tree = ET.parse(semester+'.xml')
    root = tree.getroot()
    course_level_path = []
    # foundCourses = False

    # Error check if no classes are found
    if not root.findall(path):
        # print("Could not find any courses, please try again.\n")
        return "\nCould not find any courses, please try again.\n"
    for courses in root.findall(path):
        # foundCourses = True
        for child in courses:  # list all course codes for that major
            # print(path[2:], child.tag[1:])
            levelpath = "./" + path[2:] + "/c" + child.tag[1:]

            # add all courses for major for course level search
            course_level_path.append(levelpath)

    # find course sections
    return find_courses(course_level_path, semester)


def course_level_search(path, course_levels):
    """filtered search option for searching course levels"""
    a_level_search = input("\nDo you want to search by course Level? Y/N: ")
    a_level_search = a_level_search.upper()
    found = False

    # ensures correct input from user
    if a_level_search not in {'Y', 'N', 'YES', 'NO'}:
        a_level_search = input("\nPlease enter Y/N: ")

    a_level_search = a_level_search.upper()

    if a_level_search in {'Y', 'YES'}:
        level = input("Enter course level (1000, 2000, etc.) : ")

        # error check if valid course level was entered
        if not level.isdigit():
            level = input("Please enter a number (1000, 2000, etc. : ")
        for courses in course_levels:
            # print the course information if the first number in the 4 digit number matches
            if level[0] == courses[1]:
                course_path = path + '/' + courses
                find_courses(course_path)
                found = True
        if found is False:
            print("Could not find any courses at the " + level + " level\n")

    if a_level_search == 'N' or found is False or a_level_search == 'NO':
        search_commands()


def level_search(path, courses):
    """automatically get all the levels"""
    all_course_paths = []

    for level in range(1, 10):
        for course in courses:
            if level == int(course[1]):
                course_path = path + '/' + course
                all_course_paths.append(course_path)

                # findCourses(coursePath)

    return all_course_paths


def parse_input(section,semester):
    """parses the input"""
    inp = ''.join(filter(str.isalnum, section))
    inp = inp.upper()
    my_class = re.split(r'(\d+)', inp)

    if len(my_class) < 3:  # check to see if they did not enter course code
        path = "./" + my_class[0]
        return find_classes(path,semester)

    path = "./" + my_class[0] + "/c" + my_class[1]
    path_list = []
    path_list.append(path)
    # print("path = ", path)
    return find_courses(path_list,semester)


def open_zip():
    """ open zip imported ZIP file to extract HTML file
    https://www.geeksforgeeks.org/working-zip-files-python/ """
    file_name = "CIS3760Courses.zip"
    # open ZIP file to read
    with ZipFile(file_name, 'r') as zip1:
        # extract only the HTML file for parsing
        zip1.extract(
            'Section Selection Results WebAdvisor University of Guelph.html')


def search_commands():
    """Main loop that handles all user input and calls the other functions"""
    searchflag = 1
    while searchflag == 1:
        search = input(
            "Please search for courses using the course codes. To exit the program enter EXIT:\n\n")
        search = search.replace(" ", "")
        if len(search) == 0:
            print("Nothing was entered\n")
        elif search.lower() == "exit":
            print("Exiting Program")
            system.exit(0)
        else:
            parse_input(search,"W23")



#     # Catches any error that may occur when parsing the HTML file
#     try:
#         open_zip()
#         parse_html()
#     except OSError:
#         print("There was an error trying to read the html file entered")
#         quit()
#     except:
#         print("An unknown error occured. Please check the html file entered")
#         quit()

#     print("Welcome!\n")
#     #start searching
#     search_commands()
