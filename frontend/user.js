const API = "http://127.0.0.1:8000/api/accounts";
const token = localStorage.getItem("token");

// Redirect if not logged in
if (!token) {
    window.location.href = "index.html";
}

// Generic API function
function api(url, method = "GET", body = null) {
    return fetch(API + url, {
        method,
        headers: {
            "Authorization": "Token " + token,
            "Content-Type": "application/json"
        },
        body: body ? JSON.stringify(body) : null
    })
    .then(res => res.json());
}

// Show status message temporarily
function showStatus(msg) {
    const statusDiv = document.getElementById("status");
    statusDiv.innerText = msg;
    setTimeout(() => { statusDiv.innerText = ""; }, 5000);
}

// Start work
document.getElementById("startBtn").onclick = () => {
    api("/work/", "POST", { action: "start" })
        .then(res => {
            showStatus(res.message || "Work started");
            loadDashboard();
        })
        .catch(err => showStatus("Error starting work"));
};

// Stop work
document.getElementById("stopBtn").onclick = () => {
    api("/work/", "POST", { action: "stop" })
        .then(res => {
            showStatus(res.message || "Work stopped");
            loadDashboard();
        })
        .catch(err => showStatus("Error stopping work"));
};

// Load today's dashboard
function loadDashboard() {
    api("/today/", "GET")
        .then(data => {
            // Show date
            if (!data || !data.sessions) {
                document.getElementById("today").innerHTML = "No work data for today.";
                return;
            }

            document.getElementById("date").innerText = `Date: ${data.date}`;

            // Show welcome message
            document.getElementById("welcome").innerText = `Welcome ${data.username}`;

            // Display total hours
            let html = `<p><strong>Total hours today:</strong> ${data.total_hours}</p>`;

            // Display sessions in a table
            html += `<table border="1" cellpadding="5">
                        <tr>
                            <th>Start</th>
                            <th>End</th>
                            <th>Minutes</th>
                            <th>Running</th>
                        </tr>`;

            
            data.sessions.forEach(session => {
                const bg = session.running ? "#d4edda" : "white";

                html += `<tr style="background-color:${bg}">
                    <td>${session.start}</td>
                    <td>${session.end || "—"}</td>
                    <td>${session.minutes}</td>
                    <td>${session.running ? "Running" : "Stopped"}</td>
                </tr>`;
            });


            html += `</table>`;

            document.getElementById("today").innerHTML = html;
        })
        .catch(err => {
            document.getElementById("today").innerText = "Failed to load dashboard";
        });
}

// Initial load
loadDashboard();
setInterval(loadDashboard, 30000);


document.getElementById("deleteAccountBtn").onclick = () => {
    if (!confirm("This will permanently delete your account. Are you sure?")) {
        return;
    }

    fetch("http://127.0.0.1:8000/api/accounts/delete-account/", {
        method: "DELETE",
        headers: {
            "Authorization": "Token " + localStorage.getItem("token")
        }
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        localStorage.removeItem("token");
        window.location.href = "index.html";
    });
};
