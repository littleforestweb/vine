import os

from flask import render_template, Blueprint, request, jsonify
from vine.config import Config
import mysql.connector
import json
import html

notifications = Blueprint('notifications', __name__)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@notifications.route("/notifications")
def view_notifications():
    return render_template('notifications.html')


@notifications.route("/api/get_notifications")
def api_get_notifications():
    # Get Notifications
    mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT id, base_url, base_folder, submitted_datetime, status FROM notification_id")
    results = mycursor.fetchall()
    notificationsLst = [{"id": notification[0], "base_url": notification[1], "base_folder": notification[2], "submitted_datetime": notification[3], "status": notification[4]} for notification in results]

    # Create json
    jsonR = {"notifications": notificationsLst}
    return jsonify(jsonR)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@notifications.route('/get_notification')
def view_get_notification():
    return render_template('get_notification.html', id=request.args.get('id', type=str))


@notifications.route('/api/get_notification')
def api_get_notification():
    notification_id = request.args.get('id', type=str)

    # Search DB for local file
    mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
    mycursor = mydb.cursor()

    # Get notification
    mycursor.execute("SELECT base_url, base_folder FROM notification_id WHERE id=" + notification_id)
    notification = mycursor.fetchall()[0]
    notification = {"base_url": notification[0], "base_folder": notification[1]}

    # Get pages from notification
    mycursor.execute("SELECT id, url, title, modified_date, add_by FROM notification_meta WHERE notification_id=" + notification_id)
    pages = mycursor.fetchall()
    pagesLst = [{"id": page[0], "url": page[1], "title": page[2], "modified_date": page[3], "add_by": page[4]} for page in pages]

    # Create json
    jsonR = {"notification": notification, "pages": pagesLst}
    return jsonify(jsonR)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@notifications.route('/add/notification', methods=['POST'])
def add_notification():
    if request.method == 'POST':
        # Get url from post params
        base_url = request.form.get("base_url")

        # Connect to DB
        mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
        mycursor = mydb.cursor()

        # Run SQL Command
        mycursor.execute("INSERT INTO notification_id (base_url, base_folder, status) VALUES ('" + base_url + "', '" + "" + "', '" + "pending" + "')")
        mydb.commit()
        notification_id = mycursor.lastrowid

        try:
            # Run node crawler script
            cmd = "node /opt/scraper/main.js --notificationId=" + str(notification_id) + " &"
            os.system(cmd)

            # Get fields from inserted row
            mycursor.execute("SELECT id, base_url, base_folder, submitted_datetime, status FROM notification_id WHERE id=" + str(notification_id))
            notification = mycursor.fetchall()[0]

            # Return fields back to view
            jsonR = {"message": "success", "id": notification[0], "base_url": notification[1], "base_folder": notification[2], "submitted_datetime": notification[3], "status": notification[4]}
        except Exception as ex:
            print(ex)
            mycursor.execute("DELETE FROM notification_id WHERE id=" + str(notification_id))
            mydb.commit()
            jsonR = {"message": "failed"}

        return jsonify(jsonR)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@notifications.route('/update/notification', methods=['POST'])
def update_notification():
    if request.method == 'POST':
        # Get url from post params
        # base_url = request.form.get("base_url")
        # notifications_to_delete = request.form.get("notifications_to_delete")

        original_notification_id = request.form.get("original_notification_id")
        original_notification_url = request.form.get("original_notification_url")
        original_notification_folder = request.form.get("original_notification_folder")

        new_notification_id = request.form.get("new_notification_id")
        new_notification_url = request.form.get("new_notification_url")
        new_notification_folder = request.form.get("new_notification_folder")

        # notifications = notifications_to_delete.split(",")

        # print("notifications_to_delete : " + notifications_to_delete)

        # Connect to DB
        mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
        mycursor = mydb.cursor()

        # for notification in notifications:
        #    print("Processing notification_id : " + notification)

        cmd = "UPDATE notification_id SET base_url='" + new_notification_url + "', base_folder='" + new_notification_folder + "' WHERE id=" + original_notification_id + ""

        print(cmd)

        # mycursor.execute(cmd)
        # mydb.commit()

        #    cmd = "DELETE FROM notification_id WHERE id =" + notification
        #    print(cmd)
        #    #mycursor.execute(cmd)

        #    cmd = "DELETE FROM notification_meta WHERE notification_id=" + notification
        #    print(cmd)
        #    #mycursor.execute(cmd)

        #    #mydb.commit()

        #    print()

        # notification_id = mycursor.lastrowid

        # Return info back to view
        jsonR = {"notification_to_update": original_notification_id, "action": "updated"}
        return jsonify(jsonR)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@notifications.route('/delete/notifications', methods=['POST'])
def delete_notifications():
    if request.method == 'POST':
        ## Get url from post params
        # base_url = request.form.get("base_url")
        notifications_to_delete = request.form.get("notifications_to_delete")

        notifications = notifications_to_delete.split(",")

        print("notifications_to_delete : " + notifications_to_delete)

        # Connect to DB
        mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
        mycursor = mydb.cursor()

        for notification in notifications:
            print("Processing notification_id : " + notification)

            cmd = "DELETE FROM notification_id WHERE id =" + notification
            print(cmd)
            # mycursor.execute(cmd)

            cmd = "DELETE FROM notification_meta WHERE notification_id=" + notification
            print(cmd)
            # mycursor.execute(cmd)

            # mydb.commit()

            print()

        # notification_id = mycursor.lastrowid

        # Return info back to view
        jsonR = {"notifications_to_delete": notifications_to_delete, "action": "deleted"}
        return jsonify(jsonR)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@notifications.route('/delete/notification', methods=['POST'])
def delete_notification():
    if request.method == 'POST':
        # Get url from post params
        base_url = request.form.get("base_url")

        # Connect to DB
        mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
        mycursor = mydb.cursor()

        # Run SQL Command
        mycursor.execute("DELETE FROM notification_id WHERE base_url = '" + base_url + "'")
        mydb.commit()
        notification_id = mycursor.lastrowid

        # Return info back to view
        jsonR = {"base_url": base_url, "action": "deleted"}
        return jsonify(jsonR)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@notifications.route('/save/notification', methods=['POST'])
def save_notification():
    if request.method == 'POST':
        changesJSON = request.form.get('changesJSON', type=str)
        page_id = request.form.get('page_id', type=str)

        # Get HTMLPath from page_id
        mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
        mycursor = mydb.cursor()
        mycursor.execute("SELECT HTMLpath FROM notification_meta WHERE id=" + page_id)
        HTMLpath = mycursor.fetchall()[0][0]

        # Open page file
        with open(HTMLpath) as inFile:
            data = inFile.read().replace("\n", " ")

        # Remove break lines -> Load json string -> escape html string -> Replace original with edited
        changesJSON = changesJSON.replace("\n", " ")
        changesJSON = json.loads(changesJSON)
        for change in changesJSON["changes"]:
            data = data.replace(html.unescape(change["original"]), html.unescape(change["edited"]))

        # Saved edited file
        dataFolder = "/opt/scraper/data/"
        savedFileFolder = os.path.dirname(dataFolder)
        if not os.path.exists(savedFileFolder):
            os.makedirs(savedFileFolder)
        with open(dataFolder, "w") as outFile:
            outFile.write(data)

        # Return info back to view
        jsonR = {"message": "success"}
        return jsonify(jsonR)

# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #
