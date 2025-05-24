// function toggleIstoric() {
//             const container = document.getElementById("istoric-container");
//             container.style.display = container.style.display === "none" ? "block" : "none";
//         }

function loadIstoric() {
    fetch('/istoric')
        .then(response => response.json())
        .then(zile => {
            const container = document.getElementById("istoric-container");
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
            container.style.display = "block";
        })
        .catch(error => console.error("Eroare la preluarea zilelor:", error));
}

function loadOre(){
    const ziua1 = document.getElementById("ziua1").value;
    const ziua2 = document.getElementById("ziua2").value;
    fetch(`/ore/${ziua1}`)
    .then(response => response.json())
    .then(ore => {
        const oraSelect = document.getElementById("ora1");
        oraSelect.innerHTML = "";
        ore.forEach(ora => {
            const option = document.createElement("option");
            option.value = ora;
            option.textContent = ora;
            oraSelect.appendChild(option);
        });
    })
    .catch(error => console.error("Eroare la preluarea orelor:", error));
    
    fetch(`/ore/${ziua2}`)
    .then(response => response.json())
    .then(ore => {
        const oraSelect2 = document.getElementById("ora2");
        oraSelect2.innerHTML = "";
        ore.forEach(ora => {
            const option = document.createElement("option");
            option.value = ora;
            option.textContent = ora;
            oraSelect2.appendChild(option);
        });
    })

}
