from flask import Flask


app = Flask(__name__)
app.secret_key = 'апростй'


from app import views
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
#engine = create_engine('sqlite:///books.db')