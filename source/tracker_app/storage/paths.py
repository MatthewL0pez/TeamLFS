# helper that knows where your data/ folder is, so we don’t hardcode  
# file paths all over the project when needing to access the folder.

# example: open("../../../../data/businesses.json") 

# https://docs.python.org/3/library/os.html USED IN IMPLEMENTATION: import os

import os 

def project_root(): # finds the repos main folder by going from... storage -> tracker_app -> source

    location_path = os.path.dirname(__file__) 
    root = os.path.abspath(os.path.join(location_path, "..", "..", ".."))
    return root

def data_directory(): # path: project_root + /data
    return os.path.join(project_root(), "data")
    # Example: /home/user/project/data

def data_file(filename): # path: project_root + /data + filename
    return os.path.join(data_directory(), filename)
    # Example: data_file("businesses.json") -> /.../project/data/businesses.json

# Example use:
#
# from tracker_app.storage.paths import data_file <<<<<
#
# business_path = data_file("businesses.json")    <<<<<
# user_path     = data_file("users.json")         <<<<<
#
# print("Business file location:", business_path) <<<<<
# print("User file location:", user_path)         <<<<<
#
# helps us in avoiding coding paths like "../../data/businesses.json" to access data for specific needs
# and keeps file locations consistent everywhere in the project.