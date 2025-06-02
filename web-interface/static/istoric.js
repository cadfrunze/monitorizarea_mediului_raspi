let date = new Date();
let year = date.getFullYear();
let month = date.getMonth();

const day = document.querySelector(".calendar-dates");
const currdate = document.querySelector(".calendar-current-date");
const prenexIcons = document.querySelectorAll(".calendar-navigation span");

const months = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

let startDate = null;
let endDate = null;
let selectedDayElements = [];
let ora1 = null;
let ora2 = null;
const img = document.getElementById("grafic-img");

let startDayFinal = null;
let endDayFinal = null;

const manipulate = () => {
  let dayone = new Date(year, month, 1).getDay();
  let lastdate = new Date(year, month + 1, 0).getDate();
  let dayend = new Date(year, month, lastdate).getDay();
  let monthlastdate = new Date(year, month, 0).getDate();

  let lit = "";

  for (let i = dayone; i > 0; i--) {
    lit += `<li class="inactive">${monthlastdate - i + 1}</li>`;
  }

  for (let i = 1; i <= lastdate; i++) {
    let isToday = (i === date.getDate()
      && month === new Date().getMonth()
      && year === new Date().getFullYear()) ? "active" : "";

    lit += `<li class="${isToday}" data-day="${i}">${i}</li>`;
  }

  for (let i = dayend; i < 6; i++) {
    lit += `<li class="inactive">${i - dayend + 1}</li>`;
  }

  currdate.innerText = `${months[month]} ${year}`;
  day.innerHTML = lit;

  addClickListenersToDays();
};

function addClickListenersToDays() {
  const allDays = day.querySelectorAll('li:not(.inactive)');
  allDays.forEach(li => {
    li.addEventListener('click', () => {
      const dayNum = parseInt(li.getAttribute('data-day'));
      const clickedDate = new Date(year, month, dayNum);

      if (!startDate || (startDate && endDate)) {
        clearSelection();
        startDate = clickedDate;
        endDate = null;
        highlightDay(li);
      } else if (clickedDate >= startDate) {
        endDate = clickedDate;
        highlightRange();
      } else {
        clearSelection();
        startDate = clickedDate;
        endDate = null;
        highlightDay(li);
      }
    });
  });
}

function clearSelection() {
  selectedDayElements.forEach(el => el.classList.remove('highlight', 'range'));
  selectedDayElements = [];
}

function highlightDay(dayElement) {
  dayElement.classList.add('highlight');
  selectedDayElements.push(dayElement);
}

function highlightRange() {
  clearSelection();

  const dayItems = day.querySelectorAll('li:not(.inactive)');
  dayItems.forEach(li => {
    const dayNum = parseInt(li.getAttribute('data-day'));
    const currentDate = new Date(year, month, dayNum);

    if (currentDate.getTime() === startDate.getTime() || currentDate.getTime() === endDate.getTime()) {
      li.classList.add('highlight');
      selectedDayElements.push(li);
    } else if (currentDate > startDate && currentDate < endDate) {
      li.classList.add('range');
      selectedDayElements.push(li);
    }
  });
}

manipulate();

prenexIcons.forEach(icon => {
  icon.addEventListener("click", () => {
    month = icon.id === "calendar-prev" ? month - 1 : month + 1;

    if (month < 0 || month > 11) {
      date = new Date(year, month, new Date().getDate());
      year = date.getFullYear();
      month = date.getMonth();
    } else {
      date = new Date();
    }

    startDate = null;
    endDate = null;
    selectedDayElements = [];

    manipulate();
  });
});

function formatDate(date) {
  if (!date) return null;
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const year = date.getFullYear();
  return `${day}-${month}-${year}`;
}

function populateHours(selectId) {
  const select = document.getElementById(selectId);
  if (!select) return;

  select.innerHTML = ""; // Curăță opțiunile anterioare

  const defaultOption = document.createElement('option');
  defaultOption.value = "";
  defaultOption.textContent = "Selectează ora";
  select.appendChild(defaultOption);

  for (let i = 0; i <= 23; i++) {
    const option = document.createElement('option');
    option.value = i;
    option.textContent = i;
    select.appendChild(option);
  }
}

populateHours('ora1');
populateHours('ora2');

document.getElementById('submit-button').addEventListener('click', () => {
  ora1 = document.getElementById("ora1").value;
  ora2 = document.getElementById("ora2").value;

  if (!startDate || !ora1 || !ora2) {
    alert("Te rog completează toate câmpurile.");
    return;
  }
  else if (!endDate) {
    endDate = startDate; // Dacă nu s-a selectat o dată de sfârșit, folosim data de început
  }

  startDayFinal = formatDate(startDate);
  endDayFinal = formatDate(endDate);

  loadData();
});

async function loadData() {
  if (!startDayFinal || !endDayFinal || !ora1 || !ora2) {
    alert("Date incomplete pentru trimitere.");
    return;
  }

  try {
    const response = await fetch('istoric/grafic', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        startDate: startDayFinal,
        endDate: endDayFinal,
        ora1: ora1,
        ora2: ora2
      })
    });

    if (!response.ok) throw new Error("Eroare la încărcarea datelor");

    const data = await response.json();

    if (data.status === "success") {
      alert(data.message);
      img.src = data.img + '?t=' + new Date().getTime();
      img.style.display = "block";
    } else {
      alert("Eroare: " + data.message);
    }
  } catch (error) {
    console.error("Eroare la încărcarea datelor:", error);
    alert("A apărut o eroare la încărcarea datelor.");
  }
}
