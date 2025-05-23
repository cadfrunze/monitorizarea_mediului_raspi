from services.app_service import AppService
from flask import Flask, render_template, request, jsonify

"""
Scriptul principal al aplicatiei Flask
Acesta contine rutele si logica de baza a aplicatiei.
"""

app_service: AppService = AppService()
app : Flask = Flask(__name__)

@app.route('/')
def index()-> None:
    """
    Ruteaza la pagina principala
    """
    zile: list[str] = app_service.get_days()
    return render_template('index.html', zile=zile)



if __name__ == '__main__':
    """
    Rularea aplicatiei
    """
    app.run(debug=True, host='0.0.0.0', port=5000)