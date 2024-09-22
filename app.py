from flask import Flask, render_template

# Initialiser l'application Flask
app = Flask(__name__)

# Route pour la page d'accueil
@app.route('/')
def home():
    return "Bienvenue dans mon projet Flask !"

@app.route('/home')
def dash():
    return render_template('index.html')

# Lancer l'application Flask
if __name__ == '__main__':
    app.run(debug=True)
