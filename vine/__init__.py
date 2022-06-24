from flask import Flask
from vine.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from vine.main.routes import main
    from vine.sites.routes import sites
    from vine.pages.routes import pages
    from vine.users.routes import users
    from vine.groups.routes import groups
    from vine.ugmappings.routes import ugmappings
    from vine.deployments.routes import deployments
    from vine.workflow.routes import workflow

    #from vine.ticket.routes import ticket
    from vine.tickets.routes import tickets
    #from vine.article.routes import article
    from vine.articles.routes import articles
    #from vine.notification.routes import notification
    from vine.notifications.routes import notifications

    app.register_blueprint(main)
    app.register_blueprint(sites)
    app.register_blueprint(pages)
    app.register_blueprint(users)
    app.register_blueprint(groups)
    app.register_blueprint(ugmappings)
    app.register_blueprint(deployments)
    app.register_blueprint(workflow)

    #app.register_blueprint(ticket)
    app.register_blueprint(tickets)
    #app.register_blueprint(article)
    app.register_blueprint(articles)
    #app.register_blueprint(notification)
    app.register_blueprint(notifications)

    return app
