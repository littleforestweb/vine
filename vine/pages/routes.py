import os
from flask import render_template, Blueprint, request, send_from_directory, jsonify
from vine.config import Config
import mysql.connector

pages = Blueprint('pages', __name__)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@pages.route('/all_pages')
def view_all_pages():
    return render_template('all_pages.html')


@pages.route("/api/all_pages")
def api_all_pages():
    mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
    mycursor = mydb.cursor()

    # Get all pages
    mycursor.execute("SELECT url, status, title FROM site_meta")
    results = mycursor.fetchall()
    pagesLst = [{"url": page[0], "status": page[1], "title": page[2]} for page in results]

    # Create json
    jsonR = {"pages": pagesLst}
    return jsonify(jsonR)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@pages.route('/get_page')
def get_page():
    id = request.args.get('id', type=str)

    # Search DB for local file
    mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT HTMLpath FROM site_meta WHERE id='" + id + "'")
    HTMLpath = mycursor.fetchall()[0][0]
    folderPath = os.path.dirname(HTMLpath)
    filePath = os.path.basename(HTMLpath)
    print(folderPath)
    print(filePath)
    return send_from_directory(folderPath, filePath)


@pages.route('/get_screenshot')
def get_screenshot():
    id = request.args.get('id', type=str)

    # Search DB for local file
    mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT screenshotPath FROM site_meta WHERE id='" + id + "' ORDER BY ID DESC LIMIT 1")
    screenshotPath = mycursor.fetchall()[0][0]
    folderPath = os.path.dirname(screenshotPath)
    filePath = os.path.basename(screenshotPath)

    return send_from_directory(folderPath, filePath)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@pages.route('/delete_page')
def delete_page():
    url = request.args.get('url', type=str)

    # Search DB for local file
    mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
    mycursor = mydb.cursor()
    mycursor.execute("DELETE FROM site_meta WHERE url='" + url + "'")

    jsonR = {"url": url, "action": deleted}
    return jsonify(jsonR)

# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #
