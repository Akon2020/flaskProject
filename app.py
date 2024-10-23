from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import matplotlib.pyplot as plt
import os
from werkzeug.utils import secure_filename
import io
import base64

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

@app.route('/utilite', methods=['GET', 'POST'])
def info():
    if request.method == 'POST':
        titre = request.form['titre']
        fichier = request.files['document']
        if fichier and allowed_file(fichier.filename):
            filename = secure_filename(fichier.filename)
            cheminFichier = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            fichier.save(cheminFichier)
            data = pd.read_csv(cheminFichier)
            tables = data.to_html(classes='table table-striped', header="true")
            fig, ax = plt.subplots()
            data.plot(ax=ax)
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode('utf8')

            return render_template('utilite.html', titre=titre, tables=tables, plot_url=f'data:image/png;base64,{plot_url}')

    return render_template('utilite.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def pagenotfound(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
