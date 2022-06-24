import os

from flask import render_template, Blueprint, request, jsonify
from vine.config import Config
import mysql.connector
import json
import html

articles = Blueprint('articles', __name__)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@articles.route("/articles")
def view_articles():
    return render_template('articles.html')


@articles.route("/api/get_articles")
def api_get_articles():
    # Get Articles
    mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT id, base_url, base_folder, submitted_datetime, status FROM article_id")
    results = mycursor.fetchall()
    articlesLst = [{"id": article[0], "base_url": article[1], "base_folder": article[2], "submitted_datetime": article[3], "status": article[4]} for article in results]

    # Create json
    jsonR = {"articles": articlesLst}
    return jsonify(jsonR)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@articles.route('/get_article')
def view_get_article():
    return render_template('get_article.html', id=request.args.get('id', type=str))


@articles.route('/api/get_article')
def api_get_article():
    article_id = request.args.get('id', type=str)

    # Search DB for local file
    mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
    mycursor = mydb.cursor()

    # Get article
    mycursor.execute("SELECT base_url, base_folder FROM article_id WHERE id=" + article_id)
    article = mycursor.fetchall()[0]
    article = {"base_url": article[0], "base_folder": article[1]}

    # Get pages from article
    mycursor.execute("SELECT id, url, title, modified_date, add_by FROM article_meta WHERE article_id=" + article_id)
    pages = mycursor.fetchall()
    pagesLst = [{"id": page[0], "url": page[1], "title": page[2], "modified_date": page[3], "add_by": page[4]} for page in pages]

    # Create json
    jsonR = {"article": article, "pages": pagesLst}
    return jsonify(jsonR)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@articles.route('/add/article', methods=['POST'])
def add_article():
    if request.method == 'POST':
        # Get url from post params
        base_url = request.form.get("base_url")

        # Connect to DB
        mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
        mycursor = mydb.cursor()

        # Run SQL Command
        mycursor.execute("INSERT INTO article_id (base_url, base_folder, status) VALUES ('" + base_url + "', '" + "" + "', '" + "pending" + "')")
        mydb.commit()
        article_id = mycursor.lastrowid

        try:
            # Run node crawler script
            cmd = "node /opt/scraper/main.js --articleId=" + str(article_id) + " &"
            os.system(cmd)

            # Get fields from inserted row
            mycursor.execute("SELECT id, base_url, base_folder, submitted_datetime, status FROM article_id WHERE id=" + str(article_id))
            article = mycursor.fetchall()[0]

            # Return fields back to view
            jsonR = {"message": "success", "id": article[0], "base_url": article[1], "base_folder": article[2], "submitted_datetime": article[3], "status": article[4]}
        except Exception as ex:
            print(ex)
            mycursor.execute("DELETE FROM article_id WHERE id=" + str(article_id))
            mydb.commit()
            jsonR = {"message": "failed"}

        return jsonify(jsonR)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@articles.route('/update/article', methods=['POST'])
def update_article():
    if request.method == 'POST':
        # Get url from post params
        # base_url = request.form.get("base_url")
        # articles_to_delete = request.form.get("articles_to_delete")

        original_article_id = request.form.get("original_article_id")
        original_article_url = request.form.get("original_article_url")
        original_article_folder = request.form.get("original_article_folder")

        new_article_id = request.form.get("new_article_id")
        new_article_url = request.form.get("new_article_url")
        new_article_folder = request.form.get("new_article_folder")

        # articles = articles_to_delete.split(",")

        # print("articles_to_delete : " + articles_to_delete)

        # Connect to DB
        mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
        mycursor = mydb.cursor()

        # for article in articles:
        #    print("Processing article_id : " + article)

        cmd = "UPDATE article_id SET base_url='" + new_article_url + "', base_folder='" + new_article_folder + "' WHERE id=" + original_article_id + ""

        print(cmd)

        # mycursor.execute(cmd)
        # mydb.commit()

        #    cmd = "DELETE FROM article_id WHERE id =" + article
        #    print(cmd)
        #    #mycursor.execute(cmd)

        #    cmd = "DELETE FROM article_meta WHERE article_id=" + article
        #    print(cmd)
        #    #mycursor.execute(cmd)

        #    #mydb.commit()

        #    print()

        # article_id = mycursor.lastrowid

        # Return info back to view
        jsonR = {"article_to_update": original_article_id, "action": "updated"}
        return jsonify(jsonR)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@articles.route('/delete/articles', methods=['POST'])
def delete_articles():
    if request.method == 'POST':
        ## Get url from post params
        # base_url = request.form.get("base_url")
        articles_to_delete = request.form.get("articles_to_delete")

        articles = articles_to_delete.split(",")

        print("articles_to_delete : " + articles_to_delete)

        # Connect to DB
        mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
        mycursor = mydb.cursor()

        for article in articles:
            print("Processing article_id : " + article)

            cmd = "DELETE FROM article_id WHERE id =" + article
            print(cmd)
            # mycursor.execute(cmd)

            cmd = "DELETE FROM article_meta WHERE article_id=" + article
            print(cmd)
            # mycursor.execute(cmd)

            # mydb.commit()

            print()

        # article_id = mycursor.lastrowid

        # Return info back to view
        jsonR = {"articles_to_delete": articles_to_delete, "action": "deleted"}
        return jsonify(jsonR)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@articles.route('/delete/article', methods=['POST'])
def delete_article():
    if request.method == 'POST':
        # Get url from post params
        base_url = request.form.get("base_url")

        # Connect to DB
        mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
        mycursor = mydb.cursor()

        # Run SQL Command
        mycursor.execute("DELETE FROM article_id WHERE base_url = '" + base_url + "'")
        mydb.commit()
        article_id = mycursor.lastrowid

        # Return info back to view
        jsonR = {"base_url": base_url, "action": "deleted"}
        return jsonify(jsonR)


# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@articles.route('/save/article', methods=['POST'])
def save_article():
    if request.method == 'POST':
        changesJSON = request.form.get('changesJSON', type=str)
        page_id = request.form.get('page_id', type=str)

        # Get HTMLPath from page_id
        mydb = mysql.connector.connect(host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASS, database=Config.DB_NAME)
        mycursor = mydb.cursor()
        mycursor.execute("SELECT HTMLpath FROM article_meta WHERE id=" + page_id)
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
