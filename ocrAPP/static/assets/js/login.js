document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const username = document.querySelector('.username-input').value;
    const password = document.querySelector('.password-input').value;

    
    console.log('username:', username);
    console.log('password:', password);

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
    
    fetch('http://127.0.0.1:8000/api/auth/login/', { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
        
    })
    .then(response => {
        if (response.status === 400) {
            throw new Error('Bad Request. The server could not understand the request due to invalid syntax.');
        }
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
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
            setTimeout(function() {
                window.location.replace('/login_with_token/?token=' + data.key);
            }, 3000);
        } else {
            // Invalid credentials
            swal("Oops!", "It seems like your username or password is incorrect.", "error");
        }
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        swal("Error!", "There was a problem logging you in.", "error")
    });

}
);