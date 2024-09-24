from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

@app.route('/info')
def info():
    return render_template('utilite.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def pagenotfound(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
