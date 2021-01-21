import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

from flask import Flask, redirect, url_for
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

app = Flask(__name__)

app.secret_key = b"random bytes representing flask secret key"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"  # !! Only in development environment.

app.config["DISCORD_CLIENT_ID"] = 793229007255633920  # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = "dqeqcslM0sEkyiv-rysUO5_QQM7QQZRD"  # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:8050/callback"  # URL to your callback endpoint.
app.config[
    "DISCORD_BOT_TOKEN"] = "NzkzMjI5MDA3MjU1NjMzOTIw.X-pOFA.RtmjRvyEcRnAzJHUjCc4kTwoh4Y"  # Required to access BOT resources.

discord = DiscordOAuth2Session(app)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

dashboard = dash.Dash(__name__, server=app, external_stylesheets=external_stylesheets, url_base_pathname='/')


@app.route("/login/")
def login():
    return discord.create_session()


@app.route("/callback/")
def callback():
    discord.callback()
    return redirect("/dashboardview/")


@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login"))


@app.route("/me/guilds/")
def user_guilds():
    guilds = discord.fetch_guilds()
    return "<br />".join([f"[ADMIN] {g.name}" if g.permissions.administrator else g.name for g in guilds])


@app.route("/me/")
@requires_authorization
def me():
    user = discord.fetch_user()
    return f"""
    <html>
        <head>
            <title>{user.name}</title>
        </head>
        <body>
            <img src='{user.avatar_url}' />
        </body>
    </html>"""


@app.route("/dashboardview/")
@requires_authorization
def dashboardview():
    return dashboard.index()


@app.route("/logout/")
def logout():
    discord.revoke()
    return redirect("/")


df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

dashboard.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Faça login para poder entrar no dashboard
    '''),

    dcc.Link('Clique aqui', href='/login/', refresh=True)
])

if __name__ == "__main__":
    dashboard.run_server()
