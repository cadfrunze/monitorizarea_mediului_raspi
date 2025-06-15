from services.app_service import AppService
from flask import Flask, render_template, request, jsonify, url_for, current_app
import os

"""
Scriptul principal al aplicatiei Flask
Acesta contine rutele si logica de baza a aplicatiei.
"""


app : Flask = Flask(__name__)
app_service: AppService = AppService(app)


@app.route('/')
def index()-> None:
    """
    Ruteaza la pagina principala
    """
    app_service.web_adress()
    return render_template('index.html')

@app.route('/istoric', methods=['GET'])
def istoric()-> None:
    """
    Ruteaza la pagina de istoric
    """
    
    return render_template('istoric.html')

@app.route('/istoric/grafic', methods=['POST'])
def istoric_grafic():
    data = request.get_json()

    start_date = data.get('startDate')
    ora1 = data.get('ora1')
    end_date = data.get('endDate')
    ora2 = data.get('ora2')

    if not all([start_date, ora1, end_date, ora2]):
        return jsonify({
            "status": "error",
            "message": "Date incomplete primite."
        }), 400

    ora1 = int(ora1)
    ora2 = int(ora2)
    app_service.get_all_data(start_date, ora1, end_date, ora2)

    img_filename = f"grafic_istoric/grafic_sensori.png"

    return jsonify({
        "status": "success",
        "message": "Graficul a fost generat cu succes.",
        "img": url_for('static', filename=img_filename)
    })



@app.route('/start-script', methods=['GET'])
def start_script()-> None:
    """ Ruteaza la pagina de start a scriptului
    Aceasta pagina porneste scriptul de pe Raspberry Pi pentru a citi datele de la senzori in fundal.
    """
    # app_service.delete_all_graphics()  # Sterge toate graficele anterioare la fiecare accesare a paginii de start a scriptului
    try:
        filename = 'grafic_raspi.png'
        os.path.join(current_app.root_path, 'static', 'grafic_sensors', filename)
        app_service.start_script()  

        return jsonify({
            "status": "success",
            "img": url_for('static', filename=f'grafic_sensors/{filename}'),
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
@app.route('/stop-script', methods=['POST'])
def stop_script()-> None:
    """
    Ruteaza la pagina de oprire a scriptului
    """
    #app_service.delete_all_graphics()  # Sterge toate graficele anterioare la fiecare accesare a paginii de oprire a scriptului
    app_service.stop_script()
    return jsonify(
        {
            "status": "success",
            "message": "Scriptul a fost oprit cu succes."
        }
    )

@app.route('/adresa', methods=['GET'])
def adresa()-> None:
    """
    1. Afiseaza adresa web a aplicatiei 
    """
    return render_template('adresa.html')


if __name__ == '__main__':
    """
    Rularea aplicatiei
    """
     
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)