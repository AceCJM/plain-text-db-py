# plain-text-db
a poorly made python db using plain text

Functional if you know what your doing

Documantation is a work in progress

- The first line is the database name.
- Each group is defined by a line in the format `(groupname)`.
- Each object in a group is a line: `"obj_name",type,immutable,"value"`

## Example

See the [`example`](./example) file for a sample database.

## Usage

```python
from plaindb import PlainDB

# Load or create a database
db = PlainDB("example")

# Insert a new object
db.insert("users", "user4", "str", False, "Diana")

# Get an object's value
value = db.get("users", "user1")
print(value)  # Output: Alice

# Delete an object
db.delete("users", "user2")

# Retrieve all table entries
db.retrieve_all("settings")
```