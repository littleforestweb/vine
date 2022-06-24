import os

from flask import render_template, Blueprint, jsonify, request
from vine.config import Config
import datetime
import mysql.connector

workflow = Blueprint('workflow', __name__)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #


@workflow.route("/workflow")
def view_workflow():
    return render_template('workflow.html')


@workflow.route('/workflow_details')
def view_workflow_details():
    id = request.args.get('id', type=str)

    # Get workflows
    mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT startUser, assignEditor, dueDate, tags, comments, submittedDate, status FROM workflow WHERE id=" + id)
    results = mycursor.fetchall()[0]
    data = {"id": id, "startUser": results[0], "assignEditor": results[1], "dueDate": results[2], "tags": results[3], "comments": results[4], "submittedDate": results[5], "status": results[6]}
    return render_template('workflow_details.html', data=data)


@workflow.route("/api/get_workflows")
def api_get_workflows():
    # Get workflows
    mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT id, startUser, assignEditor, dueDate, comments, submittedDate, status FROM workflow")
    results = mycursor.fetchall()
    workflowsLst = [{"id": workflow[0], "startUser": workflow[1], "assignEditor": workflow[2], "dueDate": workflow[3], "comments": workflow[4], "submittedDate": workflow[5], "status": workflow[6]} for workflow in results]

    # Create json
    jsonR = {"workflows": workflowsLst}
    return jsonify(jsonR)


@workflow.route('/workflow/add', methods=['POST'])
def add_workflow():
    jsonR = {}

    try:
        if request.method == 'POST':
            # Get url from post params
            startUser = request.form.get("startUser")
            assignEditor = request.form.get("assignEditor")
            # dueDate = request.form.get("dueDate")
            comments = request.form.get("comments")
            # tags = request.form.get("tags").strip().replace(" ", ", ")
            submittedDate = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
            siteIds = request.form.get("siteIds").strip().replace(" ", ", ")
            status = "Waiting for review"

            # Connect to DB
            mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
            mycursor = mydb.cursor()

            # Run SQL Command
            mycursor.execute("INSERT INTO workflow (startUser, assignEditor, comments, submittedDate, siteIds, status) VALUES ('" + startUser + "', '" + assignEditor + "', '" + comments + "', '" + submittedDate + "', '" + siteIds + "', '" + status + "')")
            mydb.commit()
            workflow_id = mycursor.lastrowid

            jsonR = {"message": "success", "workflow_id": str(workflow_id)}
    except Exception as ex:
        print(ex)
        jsonR = {"message": "error"}
    finally:
        return jsonify(jsonR)


@workflow.route('/workflow/status', methods=['POST'])
def approve_workflow():
    jsonR = {}

    try:
        if request.method == 'POST':
            # Get url from post params
            id = request.form.get("id")
            status = request.form.get("status")

            # Connect to DB
            mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
            mycursor = mydb.cursor()

            # Run SQL Command
            mycursor.execute("UPDATE workflow SET status = '" + status + "' WHERE id = " + id + ";")
            mydb.commit()

            # Call Rich script
            if status == "Approved":
                cmd = "sshpass -p " + Config.SSH_PW + " rsync -v -r /opt/scraper/data/ 127.0.0.1:/opt/scraper/webserver/"
                os.system(cmd + " &")

            jsonR = {"message": "success"}
    except Exception as ex:
        print(ex)
        jsonR = {"message": "error"}
    finally:
        return jsonify(jsonR)
