from flask import Flask, render_template, request, redirect, url_for, flash
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
# from sklearn import metricsfrom sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn import metrics
import os
from werkzeug.utils import secure_filename
import io
import base64
import matplotlib
matplotlib.use('Agg')

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

def get_last_uploaded_file():
    files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if allowed_file(f)]
    if not files:
        return None
    latest_file = max([os.path.join(app.config['UPLOAD_FOLDER'], f) for f in files], key=os.path.getctime)
    return latest_file

@app.route('/dashboard')
def dashboard():
    # fichier_defaut = os.path.join(app.config['UPLOAD_FOLDER'], 'dataTest.csv')
    fichier_defaut = get_last_uploaded_file()
    if fichier_defaut is None:
        return render_template('index.html', plot_url=None)

    if os.path.exists(fichier_defaut):
        data = pd.read_csv(fichier_defaut)
        data['date_vente'] = pd.to_datetime(data['date_vente'], format='%d/%m/%Y', errors='coerce')
        data = data.dropna(subset=['date_vente'])
        data.set_index('date_vente', inplace=True)
        # data.set_index('date_vente').resample('M').sum()['prix_total_de_vente'].plot(figsize=(10,6))
        plt.title('Distribution des prix unitaires de vente')
        plt.xlabel('Prix Unitaire de Vente')
        plt.ylabel('Fréquence')
        
        # data.plot(ax=ax)
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')
        
        return render_template('index.html', plot_url=f'data:image/png;base64,{plot_url}')
    return render_template('index.html', plot_url=None)

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
