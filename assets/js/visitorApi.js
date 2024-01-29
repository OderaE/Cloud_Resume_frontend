document.addEventListener('DOMContentLoaded', function () {
    // API endpoint URL
    const apiUrl = 'https://oderalabs.link/count/visits';

    // Get the element where API data will be displayed
    const apiDataElement = document.getElementById('apiData');

    // Fetch data from the API
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            
            // Process the data and update the HTML
            apiDataElement.innerHTML = `
                <p>Visitor Count: ${data}</p>
            `;
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            apiDataElement.innerHTML = 'Error fetching data';
        });
});
