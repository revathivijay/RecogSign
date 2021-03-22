import os
from app import app
from flask import Flask, flash, request, redirect, render_template, session, jsonify

@app.route('/', methods=['GET', 'POST'])
def home():
	return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	return render_template('upload.html')