document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const username = document.querySelector('.username-input').value;
    const password = document.querySelector('.password-input').value;

    // Check if username field is empty
    if (!username) {
        return swal("Oops!", "Looks like you forgot to fill in the username.", "warning");
    }

    // Check if password field is empty
    if (!password) {
        return swal("Oops!", "Looks like you forgot to fill in the password.", "warning");
    }

    // Check if fields are at least 4 characters long
    if (username.length < 4) {
        return swal("Oops!", "Username must be at least 4 characters long.", "warning");
    }

    if (password.length < 4) {
        return swal("Oops!", "Password must be at least 4 characters long.", "warning");
    }
    
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
            .catch(error => swal("Error!", "There was a problem fetching your user data.", "error"));
            swal("Success!", "You have successfully logged in.", "success");
            window.location.replace('/login_with_token/?token=' + data.key);
        } else {
            // Invalid credentials
            swal("Oops!", "It seems like your username or password is incorrect.", "error");
        }
    })
    .catch(error => swal("Error!", "There was a problem logging you in.", "error"));
});