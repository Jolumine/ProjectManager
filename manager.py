import sys
import os
import json
import shutil

def create_index_entry(name, path, description, lang): 
    with open(os.path.join(os.path.expanduser("~"), "./index.json"), "r") as f:
        parsed = json.load(f)
        f.close()

    parsed[name] = {
        "Path": path, 
        "Description": description, 
        "Language": lang
    }

    with open(os.path.join(os.path.expanduser("~"), "./index.json"), "w") as f: 
        json.dump(parsed, f, indent=4, sort_keys=False)
        f.close()

def create():
    DIR = os.getcwd()
    project_name = input("Name:")
    author = input("Author:")
    version = input("Version [default: 1.0.0]:")
    description = input("Description:")
    license = input("License [default: MIT]:")
    language = input("Programming language:").lower()
    project_path = os.path.join(DIR, project_name)
    
    if language == "python":
        os.mkdir(project_path)
        os.chdir(project_path)
        os.mkdir(os.path.join(project_path, "./doc"))
        os.mkdir(os.path.join(project_path, "./src"))
        os.mkdir(os.path.join(project_path, "./test"))


        with open(os.path.join(project_path, "./README.md"), "w") as f: 
            f.close()

        with open(os.path.join(project_path, "./run.py"), "w") as f: 
            f.close()

        with open(os.path.join(project_path, "./src/__init__.py"), "w") as f: 
            f.close()

        if version.strip() == "":
            version = "1.0.0"

        if license.strip() == "MIT": 
            license = "MIT"

        index = {
            "Name": project_name, 
            "Version": version, 
            "Author": author, 
            "Description": description,
            "License": license
        }

        with open(os.path.join(project_path, "./project.json"), "w") as f: 
            json.dump(index, f, indent=4, sort_keys=False)
            f.close()

        create_index_entry(project_name, project_path, description, "Python")
    elif language == "javascript" or language == "js": 
        pass 
    else: 
        print("Language not supported.") 

def read(name=""):
    with open(os.path.join(os.path.expanduser("~"), "./index.json"), "r") as f: 
        parsed = json.load(f)
        f.close()

    if name == "":
        print("Name | Description | Language")
        for entry in parsed: 
            print(f"{entry} | {parsed[entry]['Description']} | {parsed[entry]['Language']}") 
    else: 
        with open(os.path.join(parsed[name]["Path"], "./project.json"), "r") as f:
            local = json.load(f)
            f.close()

        print(f"Name: {local['Name']}")
        print(f"Author: {local['Author']}")
        print(f"Description: {parsed[name]['Description']}")
        print(f"License: {local['License']}")
        print(f"Version: {local['Version']}")
        print(f"Path: {parsed[name]['Path']}")

        
def delete():
    name = input("Name")
    with open(os.path.join(os.path.expanduser("~"), "./index.json"), "r") as f: 
        parsed = json.load(f)
        f.close()

    if name in parsed: 
        path = parsed[name]["Path"]
        del parsed[name]

        shutil.rmtree(path)

        with open(os.path.join(os.path.expanduser("~"), "./index.json"), "w") as f: 
            json.dump(parsed, f, indent=4, sort_keys=False)
            f.close()

    else: 
        print("Project not found.")

class Manager:
    def __init__(self) -> None: 
        self.args = sys.argv

        if os.path.exists(os.path.join(os.path.expanduser("~"), "./index.json")): 
            pass 
        else: 
            with open(os.path.join(os.path.expanduser("~"), "./index.json"), "w") as f: 
                json.dump({}, f, indent=4, sort_keys=False)
                f.close()

        if len(self.args) > 1: 
            if self.args[1] == "-create":
                create() 
            elif self.args[1] == "-delete":
                delete()
            elif self.args[1] == "-list":
                read()

            elif self.args[1] == "-show": 
                if len(self.args) > 2: 
                    read(self.args[2])
                else: 
                    print("Not enough arguments.")
            else: 
                print("Argument unknown.")
        else: 
            print("Not enough arguments.")


def main():
    Manager()

if __name__ == "__main__":
    main()

