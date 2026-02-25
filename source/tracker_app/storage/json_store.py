# 1.) starts by...          Reads from the JSON file and turns it into a pythong list/dict
# 2.) then...               writes the JSON back into a file 
# 3.) file doesnt exist...  returns value to handle crashing

# https://docs.python.org/3/library/os.html USED IN IMPLEMENTATION: import os
# https://docs.python.org/3/library/json.html USED IN IMPLEMENTATION: import json

def read_jsonFILE(path, value) # read JSON 
    if not os.path.exists(path): # if the file doesnt exist, return the value
        return value
    with open(path, "r", encoding="utf-8") as f: #open path in reading mode and tells pythong to interpret the 
                                                 # text in UTF-8
        return json.load(f)     #load data in file f
                                # EXAMPLE: JSON         = {"city": "LA", "count": 3}
                                #          json.load(f) = {"city": "LA", "count": 3} PYTHON DIRECTORY NOW 

def write_jsonFILE(path, data): #write JSON
    folder = os.path.dirname(path) # creates folders

    if folder and not os.path.exists(folder): 
        os.makedirs(folder)
    with open(path, "w", encoding="utf-8") as f: #open path in writing mode and encode data
        json.dump(data, f, indent=2)   # dump data in file f

# Example usage: 

# from tracker_app.storage.paths import data_file                   <<< Paths.py
# from tracker_app.storage.json_store import read_json, write_json
# 

# path = data_file("test.json")
# stuff = read_json(path, default_value={"hello": "world"})
# stuff["count"] = stuff.get("count", 0) + 1
# write_json(path, stuff)