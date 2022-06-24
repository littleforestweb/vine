from flask import render_template, Blueprint, jsonify, request
from vine.config import Config
import mysql.connector

users = Blueprint('users', __name__)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@users.route("/users")
def view_users():
    return render_template('users.html')


@users.route('/api/get_users')
def api_get_users():
    # Get Users
    mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT users.name, users.email, users.display_name, users_groups_mappings.group_name FROM users, users_groups_mappings WHERE users.name=users_groups_mappings.user_name")
    users = mycursor.fetchall()
    usersLst = [{"name": user[0], "email": user[1], "display_name": user[2], "group_name": user[3]} for user in users]

    # Create json
    jsonR = {"users": usersLst}
    return jsonify(jsonR)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@users.route('/add/user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        # Get post params
        name = request.form.get("name")
        email = request.form.get("email")
        ismaster = request.form.get("ismaster")
        display_name = request.form.get("display_name")
        user_group_name= request.form.get("user_group_name")

        # Connect to DB
        mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
        mycursor = mydb.cursor()

        #cmd = "SELECT id FROM user_groups WHERE name =='" +   + "'"
        #mycursor.execute("SELECT id, base_url, base_folder, submitted_datetime, status FROM site_id")
        #results = mycursor.fetchall()
        #sitesLst = [{"id": site[0], "base_url": site[1], "base_folder": site[2], "submitted_datetime": site[3], "status": site[4]} for site in results]

        # Run SQL Command
        mycursor.execute("INSERT INTO users (name, email, ismaster, display_name) VALUES ('" + name + "', '" + email + "', '" + ismaster + "', '" + display_name + "')")
        mycursor.execute("INSERT INTO users_groups_mappings (group_name, group_id, user_name) VALUES ('" + "EVERYONE" + "', '" + "1" + "', '" + name +  "')")
        mydb.commit()

        # Return fields back to view
        jsonR = {"name": name, "email": email, "display_name": display_name}
        return jsonify(jsonR)

# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@users.route('/update/user', methods=['POST'])
def update_user():
    if request.method == 'POST':
        # Get post params
        name = request.form.get("name")
        email = request.form.get("email")
        ismaster = request.form.get("ismaster")
        display_name = request.form.get("display_name")
        user_group_name= request.form.get("user_group_name")

        original_user_name = request.form.get("original_user_name")
        original_user_email = request.form.get("original_user_email")
        original_user_master = request.form.get("original_user_master")
        original_user_display_name = request.form.get("original_user_display_name")
        original_user_group_name = request.form.get("original_user_group_name")

        new_user_name = request.form.get("new_user_name")
        new_user_email = request.form.get("new_user_email")
        new_user_master = request.form.get("new_user_master")
        new_user_display_name = request.form.get("new_user_display_name")
        new_user_group_name = request.form.get("new_user_group_name")

        #print(f"name : [{name}]")
        #print(f"email : [{email}]")
        #print(f"ismaster : [{ismaster}]")
        #print(f"display_name : [{display_name}]")
        #print(f"user_group_name : [{user_group_name}]")

        print(f"original_user_name : [{original_user_name}]")
        print(f"original_user_email : [{original_user_email}]")
        print(f"original_user_display_name : [{original_user_display_name}]")
        print(f"original_user_master : [{original_user_master}]")
        print(f"original_user_group_name : [{original_user_group_name}]")

        print(f"new_user_name : [{new_user_name}]")
        print(f"new_user_email : [{new_user_email}]")
        print(f"new_user_display_name : [{new_user_display_name}]")
        print(f"new_user_master : [{new_user_master}]")
        print(f"new_user_group_name : [{new_user_group_name}]")


        # Connect to DB
        mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
        mycursor = mydb.cursor()

        # Run SQL Command
        cmd = "UPDATE users SET name='" + new_user_name + "', email='" + new_user_email + "', display_name='" + new_user_display_name + "' WHERE name='" + original_user_name + "'"
        print(cmd)
        mycursor.execute(cmd)

        cmd = "UPDATE users_groups_mappings SET user_name='" + new_user_name + "' WHERE user_name='" + original_user_name + "'"
        print(cmd)
        mycursor.execute(cmd)
        mydb.commit()

        # Return fields back to view
        jsonR = {"name": new_user_name, "email": new_user_email, "display_name": new_user_display_name}
        return jsonify(jsonR)



# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@users.route('/delete/users', methods=['POST'])
def delete_users():
    if request.method == 'POST':
        # Get post params
        #name = request.form.get("name")
        users_to_delete = request.form.get("users_to_delete")

        if users_to_delete == "":
            jsonR = {"users_to_delete": "None provided", "action": "none"}
            return jsonify(jsonR)

        users_to_delete = users_to_delete.replace("\\","\\\\")

        users_to_delete = "'" + users_to_delete.replace(",","','") + "'"

        #print("DU1")

        #print("users_to_delete = [" + users_to_delete + "]")
        #print("name = [" + name + "]")

        #print("DU2")

        # Connect to DB
        mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
        mycursor = mydb.cursor()

        # Run SQL Command
        cmd = "DELETE FROM users WHERE name IN (" + users_to_delete + ")"
        #print("cmd = [" + cmd + "]")
        mycursor.execute(cmd)
        mydb.commit()

        # Return fields back to view
        jsonR = {"users_to_delete": users_to_delete, "action": "deleted"}
        return jsonify(jsonR)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@users.route('/delete/user', methods=['POST'])
def delete_user():
    if request.method == 'POST':
        # Get post params
        name = request.form.get("name")

        # Connect to DB
        mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
        mycursor = mydb.cursor()

        # Run SQL Command
        mycursor.execute("DELETE FROM users WHERE name = '" + name + "'")
        mydb.commit()

        # Return fields back to view
        jsonR = {"name": name, "action": deleted}
        return jsonify(jsonR)

# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #
