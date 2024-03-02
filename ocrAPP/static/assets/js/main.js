// Load the reCAPTCHA library
var script = document.createElement('script');
script.src = 'https://www.google.com/recaptcha/api.js?onload=onRecaptchaLoad';
document.body.appendChild(script);

// Function to run when the reCAPTCHA library is loaded
window.onRecaptchaLoad = function() {
    // Event listener for the button
    document.getElementById('registerButton').addEventListener('click', function(event) {
        event.preventDefault(); // Prevent the form from submitting normally

        // Get form field values
        const username = document.getElementById('username').value;
        if (!/^[a-z0-9]{3,30}$/i.test(username)) {
            return swal("Error!", "Username must be alphanumeric and between 3 and 30 characters", "error");
        }
        const email = document.getElementById('email').value;
        if (!/^\S+@\S+\.\S+$/.test(email)) {
            return swal("Error!", "Please enter a valid email address", "error");
        }
        const password = document.getElementById('password').value;
        if (password.length < 8) {
            return swal("Error!", "Password must be at least 8 characters", "error");
        }
        const confirm_password = document.getElementById('confirmPassword').value;
        if (password !== confirm_password) {
            return swal("Error!", "Password and confirm password must be the same", "error");
        }
        const phone_number = document.getElementById('phone').value;
        if (!/^\d{10}$/.test(phone_number)) {
            return swal("Error!", "Phone number must be 10 digits", "error");
        }
        const address = document.getElementById('address').value;
        if (address === '') {
            return swal("Error!", "Address must not be empty", "error");
        }
        const genderRadio = document.querySelector('input[name="gender"]:checked');
        
        const gender = genderRadio ? genderRadio.value : null;
        if (!gender) {
            return swal("Error!", "Please select a gender", "error");
        }

        // If all validations pass, trigger the reCAPTCHA check
        grecaptcha.execute();
    });
};

// Callback function for the reCAPTCHA
window.onSubmit = function(token) {
    console.log('reCAPTCHA token:', token);

    // Get form field values
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirm_password = document.getElementById('confirmPassword').value;
    const phone_number = document.getElementById('phone').value;
    const address = document.getElementById('address').value;
    const genderRadio = document.querySelector('input[name="gender"]:checked');
    const gender = genderRadio ? genderRadio.value : null;

    const data = {
        username,
        email,
        password,
        confirm_password,
        phone_number,
        address,
        gender,
        'g-recaptcha-response': token  // Include the reCAPTCHA token
    };

    console.log(data);

    fetch('http://127.0.0.1:8000/api/auth/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        swal("Success!", "You have successfully registered.", "success");
    })
    .catch((error) => {
        console.error('Error:', error);
        swal("Error!", "There was a problem registering your account.", "error");
    });
};