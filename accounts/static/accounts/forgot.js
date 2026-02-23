console.log("FORGOT JS LOADED");

document.getElementById("forgotForm").addEventListener("submit", function(e){
    e.preventDefault();

    const email = document.getElementById("email").value;

    console.log("Sending reset for:", email);

    fetch("/api/accounts/forgot-password/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username: email })
    })
    .then(res => {
        if (!res.ok) {
            throw new Error("Server returned " + res.status);
        }
        return res.json();
    })
    .then(data => {
        console.log("Server response:", data);
        document.getElementById("msg").innerText = data.message || data.error;
    })
    .catch(err => {
        console.error("Forgot password failed:", err);
        document.getElementById("msg").innerText = "Network or server error. Check console.";
    });
});
