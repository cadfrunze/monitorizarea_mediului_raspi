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

@app.route('/afisare-grafic', methods=['POST'])
def afisare_grafic()-> None:
    """
    Ruteaza la pagina de afisare a graficului
    """
    data = request.get_json()
    ziua1 = data['ziua1']
    ora1 = data['ora1']
    ziua2 = data['ziua2']
    ora2 = data['ora2']
    # print(f"Ziua 1: {ziua1}, Ora 1: {ora1}, Ziua 2: {ziua2}, Ora 2: {ora2}")
    
    app_service.get_all_data(ziua1, ora1, ziua2, ora2)
    
    return jsonify(
        {
            "status": "success",
            "message": "Graficul a fost generat cu succes.",
            "img": "/static/grafic_sensori.png"
        }
    )


if __name__ == '__main__':
    """
    Rularea aplicatiei
    """
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)