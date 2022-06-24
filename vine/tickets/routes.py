import os

from flask import render_template, Blueprint, request, jsonify
from vine.config import Config
import mysql.connector
import json
import html

tickets = Blueprint('tickets', __name__)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@tickets.route("/tickets")
def view_tickets():
    print("view_tickets() ")

    cookie = request.cookies.get('lfvine')
    print(">>>>>>>>>>> " + str(cookie) + " <<<<<<<<<<<<")

    print("Cookie 'lfvine' set to '" + cookie + "'. Rendering template '" + cookie + "_tickets.html'")

    if cookie == "customer":
        return render_template('customer_tickets.html')
    elif cookie == "staff":
        return render_template('staff_tickets.html')
    elif cookie == "kanban":
        return render_template('kanban_tickets.html')

    return render_template('tickets.html')

@tickets.route("/api/get_tickets")
def api_get_tickets():
    # Get Tickets
    mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT id, url, problem, submitted, status FROM ticket")
    results = mycursor.fetchall()
    ticketsLst = [{"id": ticket[0], "url": ticket[1], "problem": ticket[2], "submitted": ticket[3], "status": ticket[4]} for ticket in results]

    # Create json
    jsonR = {"tickets": ticketsLst}
    return jsonify(jsonR)

# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@tickets.route('/get_ticket')
def view_get_ticket():
    return render_template('get_ticket.html', id=request.args.get('id', type=str))


@tickets.route('/api/get_ticket')
def api_get_ticket():
    ticket_id = request.args.get('id', type=str)

    # Search DB for local file
    mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
    mycursor = mydb.cursor()

    # Get ticket
    mycursor.execute("SELECT url, problem FROM ticket WHERE id=" + ticket_id)
    ticket = mycursor.fetchall()[0]
    ticket = {"url": ticket[0], "problem": ticket[1]}

    ## Get pages from ticket
    #mycursor.execute("SELECT id, url, title, modified_date, add_by FROM ticket_meta WHERE ticket_id=" + ticket_id)
    #pages = mycursor.fetchall()
    #pagesLst = [{"id": page[0], "url": page[1], "title": page[2], "modified_date": page[3], "add_by": page[4]} for page in pages]

    # Create json
    jsonR = {"ticket": ticket, "pages": pagesLst}
    return jsonify(jsonR)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@tickets.route('/add/ticket', methods=['POST'])
def add_ticket():
    if request.method == 'POST':
        # Get url from post params
        base_url = request.form.get("base_url")

        #ticket_id = request.form.get("ticket_id")
        ticket_url = request.form.get("ticket_url")
        ticket_title = request.form.get("ticket_title")
        ticket_description = request.form.get("ticket_description")
        ticket_accessibility = request.form.get("ticket_accessibility")
        ticket_codesearch = request.form.get("ticket_codesearch")
        ticket_other = request.form.get("ticket_other")
        ticket_screencapture = request.form.get("ticket_screencapture")

        #print("ticket_id : " + ticket_id)
        print("ticket_url : " + ticket_url)
        print("ticket_title : " + ticket_title)
        print("ticket_description : " + ticket_description)
        print("ticket_accessibility : " + ticket_accessibility)
        print("ticket_codesearch : " + ticket_codesearch)
        print("ticket_other : " + ticket_other)
        print("ticket_screencapture : " + str(ticket_screencapture))


        # Connect to DB
        mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
        mycursor = mydb.cursor()


        # Run SQL Command
        mycursor.execute("INSERT INTO ticket (title, user_id, feature, error_name, problem, url, status) VALUES ('" + ticket_title + "', -1, 'Screen', 'BSOD', '" + ticket_description + "','" + ticket_url + "','" + "new" + "');")
        mydb.commit()
        print("mycursor.lastrowid = " + str(mycursor.lastrowid))
        #ticket_id = mycursor.lastrowid

        #print("Ticket # " + str(ticket_id) + " created")

        #try:
        #    ## Run node crawler script
        #    #cmd = "node /opt/scraper/main.js --ticketId=" + str(ticket_id) + " &"
        #    #os.system(cmd)
        #
        #    ## Get fields from inserted row
        #    #mycursor.execute("SELECT id, base_url, base_folder, submitted_datetime, status FROM ticket_id WHERE id=" + str(ticket_id))
        #    #ticket = mycursor.fetchall()[0]
        #
        #    ## Return fields back to view
        #    #jsonR = {"message": "success", "id": ticket[0], "base_url": ticket[1], "base_folder": ticket[2], "submitted_datetime": ticket[3], "status": ticket[4]}
        #except Exception as ex:
        #    print(ex)
        #    mycursor.execute("DELETE FROM ticket_id WHERE id=" + str(ticket_id))
        #    mydb.commit()
        #    jsonR = {"message": "failed"}

        jsonR = {"message": "failed"}

        if mycursor.lastrowid > 0:
                jsonR = {"message": "success", "ticket_id": str(mycursor.lastrowid)}

        return jsonify(jsonR)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@tickets.route('/update/ticket', methods=['POST'])
def update_ticket():
    if request.method == 'POST':
        # Get url from post params
        # base_url = request.form.get("base_url")
        # tickets_to_delete = request.form.get("tickets_to_delete")

        original_ticket_id = request.form.get("original_ticket_id")
        original_ticket_url = request.form.get("original_ticket_url")
        original_ticket_folder = request.form.get("original_ticket_folder")

        new_ticket_id = request.form.get("new_ticket_id")
        new_ticket_url = request.form.get("new_ticket_url")
        new_ticket_folder = request.form.get("new_ticket_folder")

        # tickets = tickets_to_delete.split(",")

        # print("tickets_to_delete : " + tickets_to_delete)

        # Connect to DB
        mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
        mycursor = mydb.cursor()

        # for ticket in tickets:
        #    print("Processing ticket_id : " + ticket)

        cmd = "UPDATE ticket_id SET base_url='" + new_ticket_url + "', base_folder='" + new_ticket_folder + "' WHERE id=" + original_ticket_id + ""

        print(cmd)

        # mycursor.execute(cmd)
        # mydb.commit()

        #    cmd = "DELETE FROM ticket_id WHERE id =" + ticket
        #    print(cmd)
        #    #mycursor.execute(cmd)

        #    cmd = "DELETE FROM ticket_meta WHERE ticket_id=" + ticket
        #    print(cmd)
        #    #mycursor.execute(cmd)

        #    #mydb.commit()

        #    print()

        # ticket_id = mycursor.lastrowid

        # Return info back to view
        jsonR = {"ticket_to_update": original_ticket_id, "action": "updated"}
        return jsonify(jsonR)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@tickets.route('/delete/tickets', methods=['POST'])
def delete_tickets():
    if request.method == 'POST':
        ## Get url from post params
        # base_url = request.form.get("base_url")
        tickets_to_delete = request.form.get("tickets_to_delete")

        tickets = tickets_to_delete.split(",")

        print("tickets_to_delete : " + tickets_to_delete)

        # Connect to DB
        mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
        mycursor = mydb.cursor()

        for ticket in tickets:
            print("Processing ticket_id : " + ticket)

            cmd = "DELETE FROM ticket_id WHERE id =" + ticket
            print(cmd)
            # mycursor.execute(cmd)

            cmd = "DELETE FROM ticket_meta WHERE ticket_id=" + ticket
            print(cmd)
            # mycursor.execute(cmd)

            # mydb.commit()

            print()

        # ticket_id = mycursor.lastrowid

        # Return info back to view
        jsonR = {"tickets_to_delete": tickets_to_delete, "action": "deleted"}
        return jsonify(jsonR)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@tickets.route('/delete/ticket', methods=['POST'])
def delete_ticket():
    if request.method == 'POST':
        # Get url from post params
        base_url = request.form.get("base_url")

        # Connect to DB
        mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
        mycursor = mydb.cursor()

        # Run SQL Command
        mycursor.execute("DELETE FROM ticket_id WHERE base_url = '" + base_url + "'")
        mydb.commit()
        ticket_id = mycursor.lastrowid

        # Return info back to view
        jsonR = {"base_url": base_url, "action": "deleted"}
        return jsonify(jsonR)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@tickets.route('/save/ticket', methods=['POST'])
def save_ticket():
    if request.method == 'POST':
        changesJSON = request.form.get('changesJSON', type=str)
        page_id = request.form.get('page_id', type=str)

        # Get HTMLPath from page_id
        mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
        mycursor = mydb.cursor()
        mycursor.execute("SELECT HTMLpath FROM ticket_meta WHERE id=" + page_id)
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
