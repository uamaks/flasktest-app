from flask import Flask


app = Flask(__name__)
app.secret_key = 'апростй'


from app import views
