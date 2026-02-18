const API = "https://jetrowebattendence.onrender.com/api/accounts";

// --- LOGIN FORM ---
document.getElementById("loginForm").addEventListener("submit", function(e){
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    fetch("https://jetrowebattendence.onrender.com/api/accounts/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    })
    .then(res => {
        if (!res.ok) throw new Error("Invalid credentials");
        return res.json();
    })
    .then(data => {
    if (data.token) {
        localStorage.setItem("token", data.token);

        if (data.is_admin) {
            window.location.href = "api/accounts/admin/";
        } else {
            window.location.href = "api/accounts/user/";
        }
    } else {
        document.getElementById("error").innerText = "Invalid login";
    }
    })
    
    .catch(err => {
        document.getElementById("error").innerText = err.message || "Server error";
    });
});

// --- TOGGLE LOGIN / REGISTER ---
document.getElementById("showRegister").onclick = () => {
    document.getElementById("loginContainer").style.display = "none";
    document.getElementById("registerContainer").style.display = "block";
};
document.getElementById("showLogin").onclick = () => {
    document.getElementById("loginContainer").style.display = "block";
    document.getElementById("registerContainer").style.display = "none";
};

// --- REGISTER FORM ---
document.getElementById("registerForm").addEventListener("submit", function(e){
    e.preventDefault();

    const username = document.getElementById("regUsername").value;
    const password = document.getElementById("regPassword").value;
    const password2 = document.getElementById("regPassword2").value;
    const email = document.getElementById("regEmail").value;

    if(password !== password2) {
        document.getElementById("regError").innerText = "Passwords do not match";
        return;
    }

    fetch("https://jetrowebattendence.onrender.com/api/accounts/register/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password, email })
    })
    .then(res => res.json())
    .then(data => {
        if(data.id || data.username){   // Django returns the created user info
            alert("Account created! Please log in.");
            document.getElementById("showLogin").click();  // switch to login
        } else if(data.error){
            document.getElementById("regError").innerText = data.error;
        } else {
            document.getElementById("regError").innerText = "Registration failed";
        }
    })
    .catch(() => {
        document.getElementById("regError").innerText = "Server error";
    });
});
