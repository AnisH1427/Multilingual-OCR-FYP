document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const username = document.querySelector('.username-input').value;
    const password = document.querySelector('.password-input').value;

    fetch('http://127.0.0.1:8000/api/auth/login/', { // Added trailing slash
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username,
            password
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.key) {
            // Successfully provided credential
            localStorage.setItem('token', data.key);
            // Fetch user data after successful login
            fetch('http://127.0.0.1:8000/api/auth/user/', { // Added full URL and trailing slash
                headers: {
                    'Authorization': `Token ${data.key}`
                }
            })
            .then(response => response.json())
            .then(userData => {
                console.log(userData);
                // Do something with userData if needed
            })
            .catch(error => console.log('Error:', error));
            window.location.replace('/login_with_token/?token=' + data.key);
        } else {
            // Invalid credentials
            alert('Invalid credentials');
        }
    })
    .catch(error => console.log('Error:', error));
});