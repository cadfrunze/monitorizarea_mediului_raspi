// function toggleIstoric() {
//             const container = document.getElementById("istoric-container");
//             container.style.display = container.style.display === "none" ? "block" : "none";
//         }
const istoric_container = document.getElementById("istoric-container");
const script_container = document.getElementById("script-container");
const img_senzor = document.getElementById("senzori-img");
const img = document.getElementById("grafic-img");
let intervalId = null;






function loadIstoric() {
    fetch('/istoric')
        .then(response => response.json())
        .then(zile => {
            
            const select = document.getElementById("ziua1");
            const select2 = document.getElementById("ziua2");
            // curăță opțiunile existente
            select.innerHTML = "";
            select2.innerHTML = "";

            // adaugă fiecare zi în <select>
            zile.forEach(zi => {
                const option = document.createElement("option");
                option.value = zi;
                option.textContent = zi;
                select.appendChild(option);
                const option2 = document.createElement("option");
                option2.value = zi;
                option2.textContent = zi;
                select2.appendChild(option2);
            });

            // afișează containerul
            istoric_container.style.display = "block";
            script_container.style.display = "none"; // ascunde script container
            img_senzor.style.display = "none";
            img.style.display = "none";
            
        })
        .catch(error => console.error("Eroare la preluarea zilelor:", error));
}

function loadOre() {
    const ziua1 = document.getElementById("ziua1").value;
    const oraSelect1 = document.getElementById("ora1");
    oraSelect1.innerHTML = "<option>Se incarca...</option>";

    const ziua2 = document.getElementById("ziua2").value;
    const oraSelect2 = document.getElementById("ora2");
    oraSelect2.innerHTML = "<option>Se incarca...</option>";

    // Daca ziua1 este selectata, interogheaza serverul pentru orele disponibile

    if (ziua1) {
        fetch(`/ore/${encodeURIComponent(ziua1)}`)
            .then(response => {
                if (!response.ok) throw new Error("Eroare raspuns server");
                return response.json();
            })
            .then(ore => {
                oraSelect1.innerHTML = ""; // curata complet
                ore.forEach(ora => {
                    const opt = document.createElement("option");
                    opt.value = ora;
                    opt.textContent = ora;
                    oraSelect1.appendChild(opt);
                });
            })
            .catch(error => {
                oraSelect1.innerHTML = "<option>Eroare la incarcare</option>";
                console.error("Eroare ziua1:", error);
            });
    }

    // La fel pentru ziua2
    if (ziua2) {
        fetch(`/ore/${encodeURIComponent(ziua2)}`)
            .then(response => {
                if (!response.ok) throw new Error("Eroare raspuns server");
                return response.json();
            })
            .then(ore => {
                oraSelect2.innerHTML = "";
                ore.forEach(ora => {
                    const opt = document.createElement("option");
                    opt.value = ora;
                    opt.textContent = ora;
                    oraSelect2.appendChild(opt);
                });
            })
            .catch(error => {
                oraSelect2.innerHTML = "<option>Eroare la incarcare</option>";
                console.error("Eroare ziua2:", error);
            });
    }
}

function afisareGrafic() {
    const zi1 = document.getElementById("ziua1").value;
    const ora1 = document.getElementById("ora1").value;
    const zi2 = document.getElementById("ziua2").value;
    const ora2 = document.getElementById("ora2").value;

    fetch('/afisare-grafic', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            ziua1: zi1,
            ora1: ora1,
            ziua2: zi2,
            ora2: ora2
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            alert(data.message);
            
            img.src = data.img + '?t=' + new Date().getTime(); // timestamp pt cache
            img.style.display = "block"; // afisare img
            img_senzor.style.display = "none"; // ascunde imaginea senzorului
        }
        else {
            alert("Nu s-a putut genera graficul: " + data.message);
        }
    })
    .catch(error => {
        console.error('Eroare la trimiterea datelor:', error);
        alert('A aparut o eroare.');
    });
}

function loadScript() {
    
    script_container.style.display = "block";
    istoric_container.style.display = "none";
    img_senzor.style.display = "none";
    img.style.display = "none"; 
}

async function startScript(){
    await fetch('/start-script', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            if (!intervalId) {
                    intervalId = setInterval(actualizeazaGrafic, 3000);
                }
        
        } else {alert("Eroare: " + data.message);}
})  
    .catch(error => {
        console.error('Eroare la trimiterea datelor:', error);
        alert('A aparut o eroare la pornirea scriptului.');
    });
}

function actualizeazaGrafic() {
    img_senzor.style.display = "block"; // afișează imaginea senzorului
    const timestamp = new Date().getTime(); // forțează browserul să reîncarce
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

