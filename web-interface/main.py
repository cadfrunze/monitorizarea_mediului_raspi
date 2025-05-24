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
    return render_template('index.html')

@app.route('/istoric', methods=['GET'])
def istoric()-> None:
    """
    Ruteaza la pagina de istoric
    """
    zile: list[str] = app_service.get_days()
    return jsonify(zile)

@app.route('/ore/<zi>', methods=['GET'])
def ore(zi: str)-> None:
    """
    Ruteaza la pagina de ore
    """
    ore: list[str] = app_service.get_hours(zi)
    return jsonify(ore)


if __name__ == '__main__':
    """
    Rularea aplicatiei
    """
    app.run(debug=True, host='0.0.0.0', port=5000)