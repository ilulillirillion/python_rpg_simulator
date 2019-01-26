#!/usr/bin/env python3


from flask import Flask, jsonify, redirect
from flask_restful import Api


app = Flask(__name__)
app.api = Api(app)
