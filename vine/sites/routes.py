import os

from flask import render_template, Blueprint, request, jsonify
from vine.config import Config
import mysql.connector
import json
import html

sites = Blueprint('sites', __name__)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@sites.route("/sites")
def view_sites():
    return render_template('sites.html')


@sites.route("/api/get_sites")
def api_get_sites():
    # Get Sites
    mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT id, base_url, base_folder, submitted_datetime, status FROM site_id")
    results = mycursor.fetchall()
    sitesLst = [{"id": site[0], "base_url": site[1], "base_folder": site[2], "submitted_datetime": site[3], "status": site[4]} for site in results]

    # Create json
    jsonR = {"sites": sitesLst}
    return jsonify(jsonR)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@sites.route('/get_site')
def view_get_site():
    return render_template('get_site.html', id=request.args.get('id', type=str))


@sites.route('/api/get_site')
def api_get_site():
    site_id = request.args.get('id', type=str)

    # Search DB for local file
    mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
    mycursor = mydb.cursor()

    # Get site
    mycursor.execute("SELECT base_url, base_folder FROM site_id WHERE id=" + site_id)
    site = mycursor.fetchall()[0]
    site = {"base_url": site[0], "base_folder": site[1]}

    # Get pages from site
    mycursor.execute("SELECT id, url, title, modified_date, add_by FROM site_meta WHERE site_id=" + site_id)
    pages = mycursor.fetchall()
    pagesLst = [{"id": page[0], "url": page[1], "title": page[2], "modified_date": page[3], "add_by": page[4]} for page in pages]

    # Create json
    jsonR = {"site": site, "pages": pagesLst}
    return jsonify(jsonR)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@sites.route('/add/site', methods=['POST'])
def add_site():
    if request.method == 'POST':
        # Get url from post params
        base_url = request.form.get("base_url")

        # Connect to DB
        mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
        mycursor = mydb.cursor()

        # Run SQL Command
        mycursor.execute("INSERT INTO site_id (base_url, base_folder, status) VALUES ('" + base_url + "', '" + "" + "', '" + "pending" + "')")
        mydb.commit()
        site_id = mycursor.lastrowid

        try:
            # Run node crawler script
            cmd = "node /opt/scraper/main.js --siteId=" + str(site_id) + " &"
            os.system(cmd)

            # Get fields from inserted row
            mycursor.execute("SELECT id, base_url, base_folder, submitted_datetime, status FROM site_id WHERE id=" + str(site_id))
            site = mycursor.fetchall()[0]

            # Return fields back to view
            jsonR = {"message": "success", "id": site[0], "base_url": site[1], "base_folder": site[2], "submitted_datetime": site[3], "status": site[4]}
        except Exception as ex:
            print(ex)
            mycursor.execute("DELETE FROM site_id WHERE id=" + str(site_id))
            mydb.commit()
            jsonR = {"message": "failed"}

        return jsonify(jsonR)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@sites.route('/update/site', methods=['POST'])
def update_site():
    if request.method == 'POST':
        # Get url from post params
        # base_url = request.form.get("base_url")
        # sites_to_delete = request.form.get("sites_to_delete")

        original_site_id = request.form.get("original_site_id")
        original_site_url = request.form.get("original_site_url")
        original_site_folder = request.form.get("original_site_folder")

        new_site_id = request.form.get("new_site_id")
        new_site_url = request.form.get("new_site_url")
        new_site_folder = request.form.get("new_site_folder")

        # sites = sites_to_delete.split(",")

        # print("sites_to_delete : " + sites_to_delete)

        # Connect to DB
        mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
        mycursor = mydb.cursor()

        # for site in sites:
        #    print("Processing site_id : " + site)

        cmd = "UPDATE site_id SET base_url='" + new_site_url + "', base_folder='" + new_site_folder + "' WHERE id=" + original_site_id + ""

        print(cmd)

        # mycursor.execute(cmd)
        # mydb.commit()

        #    cmd = "DELETE FROM site_id WHERE id =" + site
        #    print(cmd)
        #    #mycursor.execute(cmd)

        #    cmd = "DELETE FROM site_meta WHERE site_id=" + site
        #    print(cmd)
        #    #mycursor.execute(cmd)

        #    #mydb.commit()

        #    print()

        # site_id = mycursor.lastrowid

        # Return info back to view
        jsonR = {"site_to_update": original_site_id, "action": "updated"}
        return jsonify(jsonR)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@sites.route('/delete/sites', methods=['POST'])
def delete_sites():
    if request.method == 'POST':
        ## Get url from post params
        # base_url = request.form.get("base_url")
        sites_to_delete = request.form.get("sites_to_delete")

        sites = sites_to_delete.split(",")

        print("sites_to_delete : " + sites_to_delete)

        # Connect to DB
        mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
        mycursor = mydb.cursor()

        for site in sites:
            print("Processing site_id : " + site)

            cmd = "DELETE FROM site_id WHERE id =" + site
            print(cmd)
            # mycursor.execute(cmd)

            cmd = "DELETE FROM site_meta WHERE site_id=" + site
            print(cmd)
            # mycursor.execute(cmd)

            # mydb.commit()

            print()

        # site_id = mycursor.lastrowid

        # Return info back to view
        jsonR = {"sites_to_delete": sites_to_delete, "action": "deleted"}
        return jsonify(jsonR)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@sites.route('/delete/site', methods=['POST'])
def delete_site():
    if request.method == 'POST':
        # Get url from post params
        base_url = request.form.get("base_url")

        # Connect to DB
        mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
        mycursor = mydb.cursor()

        # Run SQL Command
        mycursor.execute("DELETE FROM site_id WHERE base_url = '" + base_url + "'")
        mydb.commit()
        site_id = mycursor.lastrowid

        # Return info back to view
        jsonR = {"base_url": base_url, "action": "deleted"}
        return jsonify(jsonR)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@sites.route('/save/site', methods=['POST'])
def save_site():
    if request.method == 'POST':
        changesJSON = request.form.get('changesJSON', type=str)
        page_id = request.form.get('page_id', type=str)

        # Get HTMLPath from page_id
        mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
        mycursor = mydb.cursor()
        mycursor.execute("SELECT HTMLpath FROM site_meta WHERE id=" + page_id)
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
