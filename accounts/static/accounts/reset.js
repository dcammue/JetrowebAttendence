console.log("Reset JS loaded");

// Get token from URL
const urlParams = new URLSearchParams(window.location.search);
const token = urlParams.get("token");

document.getElementById("resetForm").addEventListener("submit", function(e) {
    e.preventDefault();

    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    if (password !== confirmPassword) {
        document.getElementById("msg").innerText = "Passwords do not match";
        return;
    }

    fetch("http://127.0.0.1:8000/api/accounts/reset-password/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            token: token,
            password: password
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.message) {
            document.getElementById("msg").innerText = "Password updated. Redirecting to login...";

            // Redirect to Django login page after 2 seconds
            setTimeout(() => {
                window.location.href = "http://127.0.0.1:8000/api/accounts/";
            }, 2000);

        } else if (data.error) {
            document.getElementById("msg").innerText = data.error;
        } else {
            document.getElementById("msg").innerText = "Reset failed";
        }
    })
    .catch(err => {
        console.error(err);
        document.getElementById("msg").innerText = "Server error";
    });
});
