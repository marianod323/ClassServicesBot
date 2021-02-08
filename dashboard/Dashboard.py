import dash
import os
from flask import Flask, redirect, url_for
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from dashboard.LoginUtils import BaseConfig

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
server = Flask(__name__)
server.config.from_object(BaseConfig)
server.secret_key = b"random bytes representing flask secret key"
discord = DiscordOAuth2Session(server)


def create_app():
    register_dashapps(server)
    return server


def register_dashapps(app):
    from dashboard.Layout import index_layout, get_layout

    dash_app1 = dash.Dash(__name__, server=app, url_base_pathname='/')
    dash_app2 = dash.Dash(__name__, server=app, url_base_pathname='/dashboard_view/', external_stylesheets=external_stylesheets)

    with app.app_context():
        dash_app1.title = 'Home'
        dash_app1.layout = index_layout
        dash_app2.title = 'Dashboard'
        dash_app2.layout = get_layout(discord)

    protect_dashviews(dash_app2)


def protect_dashviews(dashapp):
    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.config.url_base_pathname):
            dashapp.server.view_functions[view_func] = requires_authorization(dashapp.server.view_functions[view_func])


@server.route('/login/')
def login():
    return discord.create_session(scopes=[""])


@server.route("/callback/")
def callback():
    discord.callback()
    return redirect("/dashboard_view/")


@server.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login"))
