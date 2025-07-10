# PlainDB: A Simple Plain Text Database
import sys,os

# DB template
"""
db name

(group name)
"obj name", "type", immutable, "value"
"obj name", "type", immutable, "value"
"obj name", "type", immutable, "value"
"obj name", "type", immutable, "value"
"""

class PlainDB:
    """A simple plain text database class for managing key-value pairs in groups."""
    def __init__(self, db_path: str):
        """Initializes the PlainDB instance with the path to the database file.
        Args:
            db_path (str): The path to the database file.
        """
        self.db_path = db_path
        self.load_db()
    
    def load_db(self):
        """Initializes the PlainDB instance and loads the database from the specified path."""
        try:
            with open(self.db_path, "r") as file:
                cont = file.read()
        except FileNotFoundError:
            print(f"Database file '{self.db_path}' not found. Creating a new one.")
            self.create_db()
            return
        db = cont.splitlines()
        self.db = {"name": db[0]}
        group = {}
        for i in db[1:]:
            if i.strip() == "": continue
            if i.startswith("(") and i.endswith(")"):
                group_name = i[1:-1]
                group = {group_name: {}}
                self.db.update(group)
            else:
                obj_name, obj_type, imm, value = i.split(",")
                self.db[group_name][obj_name] = [obj_type, imm, value]
    def create_db(self):
        """Creates a new database with the specified path."""
        self.db = {"name": self.db_path.split('/')[0]}
        self.save_db()
    def save_db(self):
        """Saves the current state of the database to the specified path."""
        with open(self.db_path, "w") as file:
            file.write(self.db["name"] + "\n")
            for group_name, objects in self.db.items():
                if group_name == "name":
                    continue
                file.write(f"({group_name})\n")
                for obj_name, obj_data in objects.items():
                    file.write(f"{obj_name},{obj_data[0]},{obj_data[1]},{obj_data[2]}\n")
    def insert(self, group_name: str, obj_name: str, obj_type: str, immutable: bool, value: str):
        """Inserts a new object into the specified group.
        Args:
            group_name (str): The name of the group.
            obj_name (str): The name of the object.
            obj_type (str): The type of the object.
            immutable (bool): Whether the object is immutable.
            value (str): The value of the object.
        """
        if group_name not in self.db:
            self.db[group_name] = {}
        if obj_name in self.db[group_name]:
            if self.db[group_name][obj_name][1] == "true":
                print(f"Cannot modify immutable object '{obj_name}' in group '{group_name}'.")
                return
        self.db[group_name][obj_name] = [obj_type, str(immutable).lower(), value]
        self.save_db()
    def get(self, group_name: str, obj_name: str):
        """Retrieves the value of an object from the specified group.
        Args:
            group_name (str): The name of the group.
            obj_name (str): The name of the object.
        Returns:
            str: The value of the object, or None if not found.
        """
        return self.db.get(group_name, {}).get(obj_name, [None, None, None])[2]
    def delete(self, group_name: str, obj_name: str):
        """Deletes an object from the specified group.
        Args:
            group_name (str): The name of the group.
            obj_name (str): The name of the object.
        """
        if group_name in self.db and obj_name in self.db[group_name]:
            if self.db[group_name][obj_name][1] == "true":
                raise ValueError(f"Cannot delete immutable object '{obj_name}' in group '{group_name}'.")
            del self.db[group_name][obj_name]
            self.save_db()
        else:
            print(f"Object '{obj_name}' not found in group '{group_name}'.")
    def __repr__(self):
        return str(self.db)