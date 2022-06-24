from flask import render_template, Blueprint, jsonify, request
from vine.config import Config
import mysql.connector

ugmappings = Blueprint('ugmappings', __name__)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@ugmappings.route("/ugmappings")
def view_ugmappings():
    return render_template('ugmappings.html')

##### 
##### @groups.route('/api/get_groups')
##### def api_get_groups():
#####     # Get Groups
#####     mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
#####     mycursor = mydb.cursor()
#####     mycursor.execute("SELECT name, display_name, description, id FROM user_groups")
#####     groups = mycursor.fetchall()
#####     groupsLst = [{"name": group[0], "display_name": group[1], "description": group[2], "id": str(group[3])} for group in groups]
##### 
#####     # Create json
#####     jsonR = {"groups": groupsLst}
##### 
#####     return jsonify(jsonR)
##### 
##### 
##### # ---------------------------------------------------------------------------------------------------------- #
##### # ---------------------------------------------------------------------------------------------------------- #
##### 
##### @groups.route('/add/group', methods=['POST'])
##### def add_group():
#####     if request.method == 'POST':
#####         # Get post params
#####         name = request.form.get("name")
#####         display_name = request.form.get("group_display_name")
#####         description = request.form.get("description")
#####         id = request.form.get("group_id")
##### 
#####         # Connect to DB
#####         mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
#####         mycursor = mydb.cursor()
##### 
#####         # Run SQL Command
#####         mycursor.execute("INSERT INTO user_groups (name, display_name, description, id) VALUES ('" + name + "', '" + display_name + "', '" + description + "', '" + id + "')")
#####         mydb.commit()
##### 
#####         # Return fields back to view
#####         #jsonR = {"name": name, "display_name": display_name, "description": description}
#####         jsonR = {"name": name, "display_name": display_name, "description": description, "id": id }
#####         return jsonify(jsonR)
##### 
##### # ---------------------------------------------------------------------------------------------------------- #
##### # ---------------------------------------------------------------------------------------------------------- #
##### 
##### @groups.route('/update/group', methods=['POST'])
##### def update_group():
#####     if request.method == 'POST':
#####         # Get post params
#####         original_name = request.form.get("original_name")
#####         original_group_display_name = request.form.get("original_group_display_name")
#####         original_description = request.form.get("original_description")
#####         original_group_id = request.form.get("original_group_id")
##### 
#####         new_name = request.form.get("new_name")
#####         new_group_display_name = request.form.get("new_group_display_name")
#####         new_description = request.form.get("new_description")
#####         new_group_id = request.form.get("new_group_id")
##### 
#####         # Connect to DB
#####         mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
#####         mycursor = mydb.cursor()
##### 
#####         # Run SQL Command
#####         mycursor.execute("UPDATE user_groups SET name = '" + new_name + "', display_name = '" + new_group_display_name + "', description = '" + new_description + "', id = '" + new_group_id + "' WHERE name = '" + original_name + "' AND display_name = '" + original_group_display_name + "' AND description = '" + original_description + "' AND id = '" + original_group_id + "'")
#####         mydb.commit()
##### 
#####         ## Return fields back to view
#####         #return jsonify(jsonR)
##### 
#####         jsonR = {"group_id": "group_id", "action": "updated"}
#####         return jsonify(jsonR)
##### 
##### # ---------------------------------------------------------------------------------------------------------- #
##### # ---------------------------------------------------------------------------------------------------------- #
##### 
##### @groups.route('/delete/groups', methods=['POST'])
##### def delete_group():
#####     if request.method == 'POST':
#####         # Get post params
#####         groups_to_delete = request.form.get("groups_to_delete")
##### 
#####         print("groups_to_delete : [" + groups_to_delete + "]")
##### 
#####         # Connect to DB
#####         mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
#####         mycursor = mydb.cursor()
##### 
#####         # Run SQL Command
#####         cmd = "DELETE FROM user_groups WHERE id IN (" + groups_to_delete + ")"
#####         print(cmd)
#####         mycursor.execute(cmd)
#####         mydb.commit()
##### 
#####         # Return fields back to view
#####         jsonR = {"groups_to_delete": groups_to_delete, "action": "deleted"}
#####         return jsonify(jsonR)
##### 
##### # ---------------------------------------------------------------------------------------------------------- #
##### # ---------------------------------------------------------------------------------------------------------- #
#####
