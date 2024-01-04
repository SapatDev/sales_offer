from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask import Flask ,request, jsonify
from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS, cross_origin

app = Flask(__name__, template_folder='template',static_url_path='/assets')
app.secret_key = 'astghfi7589fdgnmkiuj'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mandar:Nb7Np4!lURI0u@142.93.208.119/salesoffer'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# CORS(app)



