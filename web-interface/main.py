from services.app_service import AppService
from flask import Flask, render_template, request, jsonify, url_for, current_app
import os

"""
Scriptul principal al aplicatiei Flask
Acesta contine rutele si logica de baza a aplicatiei.
"""


app : Flask = Flask(__name__)
app_service: AppService = AppService(app)
count_user: int = 0

@app.route('/')
def index()-> None:
    """
    Ruteaza la pagina principala
    """
    global count_user
    count_user += 1
    app_service.count_user = count_user  # Adauga numarul de utilizatori la lista
    app_service.list_count_user.append(count_user)  # Adauga numarul de utilizatori la lista
    # app_service.get_all_data(21, 9, "31-05-2025", "01-06-2025")
    #app_service.delete_all_graphics()  # Sterge toate graficele anterioare la fiecare accesare a paginii principale
    return render_template('index.html')

@app.route('/istoric', methods=['GET'])
def istoric()-> None:
    """
    Ruteaza la pagina de istoric
    """
    
    return render_template('istoric.html')

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
    #app_service.delete_all_graphics()  # Sterge toate graficele anterioare la fiecare accesare a paginii de afisare a graficului
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
            'img': url_for('static', filename=f"/grafic_istoric/grafic_sensori{app_service.list_count_user[count_user-1]}.png")
        }
    )


@app.route('/start-script', methods=['POST'])
def start_script()-> None:
    """ Ruteaza la pagina de start a scriptului
    Aceasta pagina porneste scriptul de pe Raspberry Pi pentru a citi datele de la senzori in fundal.
    """
    # app_service.delete_all_graphics()  # Sterge toate graficele anterioare la fiecare accesare a paginii de start a scriptului
    try:
        filename = f'grafic_raspi{app_service.list_count_user[count_user-1]}.png'
        os.path.join(current_app.root_path, 'static', 'grafic_sensors', filename)
        app_service.start_script()  

        return jsonify({
            "status": "success",
            "img": url_for('static', filename=f'grafic_sensors/{filename}'),
            'count_user': count_user,
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


if __name__ == '__main__':
    """
    Rularea aplicatiei
    """
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)