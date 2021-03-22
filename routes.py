import os
from app import app
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, render_template, session, jsonify
from predict import predict, display_img
import cv2
import numpy as np
from PIL import Image

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def home():
	return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		if 'file' not in request.files:
			flash("No file selected", "danger")
			error = "No file selected"
			return render_template('upload.html')

		file = request.files['file']
		if file.filename == '':
			flash("No file selected", "error")
			return render_template('upload.html')

		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['DESTINATION_FOLDER'], filename))

			# prediction
			img = cv2.imread(os.path.join(app.config['DESTINATION_FOLDER'], filename))
			img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
			predicted_img, class_pred = predict(img)
			display_img(predicted_img)
			return render_template('predictionDisplay.html', predicted_img=predicted_img, class_pred=class_pred)

		flash("Successfully saved imaged to destination!", "success")

	return render_template('upload.html')