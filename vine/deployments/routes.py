from flask import render_template, Blueprint, jsonify, request
from vine.config import Config
import mysql.connector

deployments = Blueprint('deployments', __name__)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #


@deployments.route("/deployments")
def view_deployments():
    return render_template('deployments.html')


@deployments.route("/api/deployments")
def api_deployments():
    # Get deployments from MySQL
    mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT deployment_number, deployment_user, submitted_timestamp, source_files, destination_location, completed_timestamp, status, deployment_log FROM deployments")
    deployments = mycursor.fetchall()

    # Add deployments to list
    deploymentsLst = [{"deployment_number": deployment[0], "deployment_user": deployment[1],
                       "submitted_timestamp": deployment[2], "source_files": deployment[3],
                       "destination_location": deployment[4], "completed_timestamp": deployment[5],
                       "status": deployment[6], "deployment_log": deployment[7]} for deployment in deployments]

    # Create json
    jsonR = {"deployments": deploymentsLst}
    return jsonify(jsonR)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@deployments.route('/delete/deployments', methods=['POST'])
def delete_deployments():
    if request.method == 'POST':
        # Get post params
        deployments_to_delete = request.form.get("deployments_to_delete")
        print("deployments_to_delete: " + deployments_to_delete)

        # Connect to DB
        mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
        mycursor = mydb.cursor()

        # Run SQL Command
        cmd = "DELETE FROM deployments WHERE deployment_number IN (" + deployments_to_delete + ")"
        # print(cmd)
        mycursor.execute(cmd)
        mydb.commit()

        # Return fields back to view
        jsonR = {"deployments_deleted": deployments_to_delete, "action": "deleted"}
        return jsonify(jsonR)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@deployments.route('/pause/deployments', methods=['POST'])
def pause_deployments():
    if request.method == 'POST':
        # Get post params
        deployments_to_pause = request.form.get("deployments_to_pause")
        print("deployments_to_pause: " + deployments_to_pause)

        # Connect to DB
        mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
        mycursor = mydb.cursor()

        # Run SQL Command
        cmd = "UPDATE deployments SET status='paused' WHERE deployment_number IN (" + deployments_to_pause + ") AND (status='pending' OR status='failed')"
        print(cmd)
        mycursor.execute(cmd)
        mydb.commit()

        # Return fields back to view
        jsonR = {"deployments_paused": deployments_to_pause, "action": "paused"}
        return jsonify(jsonR)


@deployments.route('/update/deployment', methods=['POST'])
def deployment_group():
    if request.method == 'POST':
        # Get post params

        deployment_number = request.form.get("h_e_deployment_number")
        new_deployment_source_server = request.form.get("e_deployment_source_server")
        new_deployment_source_path = request.form.get("e_deployment_source_path")
        new_deployment_target_server = request.form.get("e_deployment_target_server")
        new_deployment_target_path = request.form.get("e_deployment_target_path")

        print("Updating deployment")

        print()

        print("deployment_number: " + deployment_number)

        print("new_deployment_source_server: " + new_deployment_source_server)
        print("new_deployment_source_path: " + new_deployment_source_path)
        print("new_deployment_target_server: " + new_deployment_target_server)
        print("new_deployment_target_path: " + new_deployment_target_path)

        print()

        # Connect to DB
        mycursor = mydb.cursor()

        # Run SQL Command
        cmd = "UPDATE deployments SET source_server_name='" + new_deployment_source_server + "', source_files='" + new_deployment_source_path + "', destination_server_name='" + new_deployment_target_server + "', destination_location='" + new_deployment_target_path + "' WHERE deployment_number=" + deployment_number + ""

        print(cmd)
        mycursor.execute(cmd)

        cmd = "UPDATE deployments SET source_server_ip='" + new_deployment_source_server + "', source_files='" + new_deployment_source_path + "', destination_server_ip='" + new_deployment_target_server + "', destination_location='" + new_deployment_target_path + "' WHERE deployment_number=" + deployment_number + ""
        print(cmd)
        mycursor.execute(cmd)

        mydb.commit()

        ## Return fields back to view
        ##jsonR = {"name": name, "display_name": display_name, "description": description}
        # jsonR = {"name": name, "display_name": display_name, "description": description, "id": id }
        # return jsonify(jsonR)

        jsonR = {"deployment_number": deployment_number, "action": "updated"}
        return jsonify(jsonR)

# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #
