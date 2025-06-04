
const script_container = document.getElementById("script-container");
const img_senzor = document.getElementById("senzori-img");
const img = document.getElementById("grafic-img");
let intervalId = null;






function loadScript() {
    
    script_container.style.display = "block";
    img_senzor.style.display = "none";
}



async function startScript() {
    // Pornește scriptul pe server
    const response = await fetch('/start-script');
    const data = await response.json();

    if (data.status === "success") {
        const img_senzor = document.getElementById("senzori-img");
        img_senzor.style.display = "block";
        const timestamp = new Date().getTime();
        img_senzor.src = data.img + `?t=${timestamp}`;
        // Pornește intervalul dacă nu e deja pornit
        if (!intervalId) {
            intervalId = setInterval(actualizeazaGrafic, 3000);
        }
    } else {
        alert("Eroare: " + data.message);
    }
}

function actualizeazaGrafic() {
    const img_senzor = document.getElementById("senzori-img");
    img_senzor.style.display = "block";
    const timestamp = new Date().getTime();
    img_senzor.src = `/static/grafic_sensors/grafic_raspi.png?t=${timestamp}`;
}

function stopScript() {
    fetch('/stop-script', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            clearInterval(intervalId);
            intervalId = null;
            document.getElementById("senzori-img").style.display = "none";
            alert("Script oprit cu succes.");
        } else {
            alert("Eroare la oprirea scriptului: " + data.message);
        }
    })
    .catch(error => {
        console.error('Eroare la oprirea scriptului:', error);
        alert('A aparut o eroare la oprirea scriptului.');
    });
}


