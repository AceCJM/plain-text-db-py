# PlainDB: A Simple Plain Text Database
# DB template
"""
db name

(table name)
"obj name", "type", immutable, "value"
"obj name", "type", immutable, "value"
"obj name", "type", immutable, "value"
"obj name", "type", immutable, "value"
"""


class PlainDB:
    """A simple plain text database class for managing key-value pairs in tables."""

    def __init__(self, db_path: str) -> None:
        """Initializes the PlainDB instance with the path to the database file.
        Args:
            db_path (str): The path to the database file.
        """
        self.db_path = db_path
        self.db = {}
        self.load_db()

    def load_db(self) -> None:
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
        table = {}
        table_name = ""
        for i in db[1:]:
            if i.strip() == "":
                continue
            if i.startswith("(") and i.endswith(")"):
                table_name = i[1:-1]
                table = {table_name: {}}
                self.db.update(table)
            else:
                obj_name, obj_type, imm, value = i.split(",")
                self.db[table_name][obj_name] = [obj_type, imm, value]

    def create_db(self) -> None:
        """Creates a new database with the specified path."""
        self.db = {"name": self.db_path.split("/")[0]}
        self.save_db()

    def save_db(self) -> None:
        """Saves the current state of the database to the specified path."""
        with open(self.db_path, "w") as file:
            file.write(self.db["name"] + "\n")
            for table_name, objects in self.db.items():
                if table_name == "name":
                    continue
                file.write(f"({table_name})\n")
                for obj_name, obj_data in objects.items():
                    file.write(
                        f"{obj_name},{obj_data[0]},{obj_data[1]},{obj_data[2]}\n"
                    )

    def insert(self, table_name: str, obj_name: str, obj_type: str, immutable: bool, value: str) -> None:
        """Inserts a new object into the specified table.
        Args:
            table_name (str): The name of the table.
            obj_name (str): The name of the object.
            obj_type (str): The type of the object.
            immutable (bool): Whether the object is immutable.
            value (str): The value of the object.
        """
        if table_name not in self.db:
            self.db[table_name] = {}
        if obj_name in self.db[table_name]:
            if self.db[table_name][obj_name][1] == "true":
                print(
                    f"Cannot modify immutable object '{obj_name}' in table '{table_name}'."
                )
                return
        self.db[table_name][obj_name] = [obj_type, str(immutable).lower(), value]
        self.save_db()

    def get(self, table_name: str, obj_name: str) -> str:
        """Retrieves the value of an object from the specified table.
        Args:
            table_name (str): The name of the table.
            obj_name (str): The name of the object.
        Returns:
            str: The value of the object, or None if not found.
        """
        return self.db.get(table_name, {}).get(obj_name, [None, None, None])[2]

    def delete(self, table_name: str, obj_name: str) -> None:
        """Deletes an object from the specified table.
        Args:
            table_name (str): The name of the table.
            obj_name (str): The name of the object.
        """
        if table_name in self.db and obj_name in self.db[table_name]:
            if self.db[table_name][obj_name][1] == "true":
                raise ValueError(
                    f"Cannot delete immutable object '{obj_name}' in table '{table_name}'."
                )
            del self.db[table_name][obj_name]
            self.save_db()
        else:
            print(f"Object '{obj_name}' not found in table '{table_name}'.")

    def retrieve_all(self, table_name: str) -> list:
        """Retrireves all objects from a table.
        Args:
            table_name (str): The name of the table.
        Returns:
            list: All the data from the table 
        """
        table = self.db[table_name]
        parsed_table = []
        for entry in table:
            parsed_table.append([entry] + table[entry])
        return parsed_table