from search import *
from a1 import *
import json

# Read in test cases
with open('testcases.json', 'r') as f:
  data = json.load(f)

# Test course code level search
def test_findCoursescis3760():
    output = (parse_input("cis3760"))
    output2 = json.loads(output)
    assert output2 == data["testcase1"], "Did not recieve proper search results"

# Test faculty level search
def test_findFaculty():
    output = (parse_input("acct"))
    output2 = json.loads(output)
    assert output2 == data["testcase2"], "Did not recieve proper search results"

def test_emptyfile():
    emptyFile()
    assert os.path.getsize('text.json') == 0, "File was not emptied"


if __name__ == "__main__":
    test_findCoursescis3760()
    test_findFaculty()
    test_emptyfile()
    print("Everything passed")

#print(parse_input("acct"))


#print("this is a test ass bitch")
#print(parse_input("cis3760"))