from flask import Blueprint, render_template

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("index.html")


@main.app_errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@main.app_errorhandler(500)
def internal_server_error(error):
    return render_template("errors/500.html"), 500