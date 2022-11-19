from reclaim_sdk.models.task import ReclaimTask
from reclaim_sdk.client import ReclaimClient
from datetime import datetime, timedelta

token = "eyJhbGciOiJIUzI1NiJ9.eyJhdF9oYXNoIjoiN2lrSXVSSHB6UkFvMkw1SnJFWUVwZyIsInN1YiI6IjEwOTY1NTYwMjcxMzkyODkzMDU3MSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJyb2xlcyI6W10sImlzcyI6InJlY2xhaW0tYXBpIiwiZ2l2ZW5fbmFtZSI6IkVzdGVhayIsImxvY2FsZSI6ImVuIiwibm9uY2UiOiJjY2IxYzYyZS1jYTU4LTQwZWEtOTMzYS0zZGVmMGZkNGJkN2MiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUxtNXd1MFhxUHQ3WGRUd1dLeFZiYW93R2tKa0VxSVJOZFVRbEpLcWlQbG9iQT1zOTYtYyIsIm5iZiI6MTY2ODcyNjY3NCwiYXpwIjoiMjIwOTM4MDgyMDI3LWdrYzg1ZGIxZHVldWJyNTQ0cHM5c3ZndGxlYzQ2MDhsLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwibmFtZSI6IkVzdGVhayBTaGFwaW4iLCJzdGF0ZSI6eyJhcHAiOiJhcHAiLCJhcHBVcmwiOiJodHRwczovL2FwcC5yZWNsYWltLmFpLyIsInJlZiI6bnVsbCwic2xhY2tUZWFtSWQiOm51bGwsInNsYWNrVXNlcklkIjpudWxsLCJyZWRpcmVjdCI6Ii9wbGFubmVyPyIsImppcmFTdGF0ZSI6bnVsbCwib3JpZ2luYWxVcmkiOm51bGwsInJlZGlyZWN0VXJpIjoiaHR0cHM6Ly9hcGkuYXBwLnJlY2xhaW0uYWkvb2F1dGgvY2FsbGJhY2svZ29vZ2xlIiwiaW52aXRlS2V5IjpudWxsLCJ1dG1DYW1wYWlnbiI6bnVsbCwidXRtTWVkaXVtIjpudWxsLCJ1dG1UZXJtIjpudWxsLCJyc3ZwIjpudWxsLCJvbmVPbk9uZUlkIjpudWxsLCJub25jZSI6IjEyNjI2MTkwLTIxNjktNGFlYS05Yjk2LWQ3YjQ1ZjMwMTMxMSJ9LCJleHAiOjE2NjkzMzE0NzQsImlhdCI6MTY2ODcyNjY3NCwiZmFtaWx5X25hbWUiOiJTaGFwaW4iLCJlbWFpbCI6ImVzdGVha3NoYXBpbkBnbWFpbC5jb20iLCJvYXV0aDJQcm92aWRlciI6Imdvb2dsZSJ9.xHcP5HSmLpc3LWApAh5NNo4SOYLGdvBaW2L-s8R4lLk"

ReclaimClient(token=token)


assignments = []

file1 = open('data.txt', 'r')
Lines = file1.readlines()

counter = 0

assignments = []

currentAssignment = {}

for line in Lines:
    # reset assignment object
    if (counter % 8 == 0):
        currentAssignment = {}

    # title
    if (counter % 8 == 1):
        start = line.find("HW")
        if start < 0: 
            start = line.find("Exam")
        end = line.find("<", start)
        title = line[start:end]

        if (not title):
            counter += 7
            continue
        
        currentAssignment["title"] = "(MATH 125) " + title
        
    # grade
    if (counter % 8 == 2):
        start = line.find(">") + 1
        grade = line[start: line.find("<", start)]
        currentAssignment["grade"] = grade
    
    if (counter % 8 == 5):
        start = line.find(">") + 1
        dueDate = line[start: line.find("<", start)]
        currentAssignment["dueDate"] = dueDate

    if (counter % 8 == 7):
        if(currentAssignment["grade"] == "0%" and datetime.strptime(currentAssignment["dueDate"], '%m/%d/%y %H:%M%p') > datetime.now()):
            # It is also possible to create an object without using a context manager.
            task = ReclaimTask()

            task.name = currentAssignment["title"]

            if (currentAssignment["title"].find("HW") > -1):
                task.duration = .75
            else:
                task.duration = 5
            
            task.min_work_duration = 0.5
            task.max_work_duration = 1.5
            task.start_date = datetime.now() 
            task.due_date = datetime.strptime(currentAssignment["dueDate"], '%m/%d/%y %H:%M%p')

            # Then the object needs to be saved manually to the API.
            task.save()

            assignments.append(currentAssignment)
    counter += 1

print(assignments)