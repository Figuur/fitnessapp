let datum = new Date().toLocaleDateString();
document.getElementById('datum').innerHTML = `<h1>Datum: ${datum}</h1>`;


const toggleSwitch = document.querySelector('#checkbox');
const body = document.body;

toggleSwitch.addEventListener('change', function() {
    body.classList.toggle('light-theme');
    
    // Save preference to localStorage
    if(body.classList.contains('light-theme')) {
        localStorage.setItem('theme', 'light');
    } else {
        localStorage.setItem('theme', 'dark');
    }
});

// Check for saved theme preference
const currentTheme = localStorage.getItem('theme');
if (currentTheme === 'light') {
    body.classList.add('light-theme');
    toggleSwitch.checked = true;
}

// Voeg deze functies toe aan je bestaande JavaScript
function openModal() {
    document.getElementById('workoutModal').style.display = 'block';
    document.body.style.overflow = 'hidden'; // Voorkomt scrollen van de achtergrond
}

function closeModal() {
    document.getElementById('workoutModal').style.display = 'none';
    document.body.style.overflow = 'auto'; // Herstelt scrollen
}

// Sluit modal als er buiten de content wordt geklikt
window.onclick = function(event) {
    const modal = document.getElementById('workoutModal');
    if (event.target == modal) {
        closeModal();
    }
}