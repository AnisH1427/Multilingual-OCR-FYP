document.getElementById('registerButton').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent the form from submitting normally

    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirm_password = document.getElementById('confirmPassword').value;
    const phone_number = document.getElementById('phone').value;
    const address = document.getElementById('address').value;
    const gender = document.querySelector('input[name="gender"]:checked').value;

    // // Check if passwords match
    // if (password !== confirmPassword) {
    //     console.error('Passwords do not match');
    //     return;
    // }

    const data = {
        username,
        email,
        password,
        confirm_password,
        phone_number,
        address,
        gender
    };

    console.log(data);

    fetch('http://127.0.0.1:8000/api/auth/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => console.log('Success:', data))
    .catch((error) => {
        console.error('Error:', error);
    });
});