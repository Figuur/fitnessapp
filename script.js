document.getElementById('newExerciseForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const formData = {
        Oefeningen: document.getElementById('oefening').value,
        Sets: document.getElementById('sets').value,
        Aantal_keer: document.getElementById('aantal').value,
        Omschrijving: document.getElementById('omschrijving').value
    };

    fetch('http://127.0.0.1:5000/add_exercise', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        alert('Oefening succesvol toegevoegd!');
        document.getElementById('newExerciseForm').reset();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Er is een fout opgetreden bij het toevoegen van de oefening.');
    });
});
