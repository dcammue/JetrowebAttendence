const token = localStorage.getItem("token");
const API = "http://127.0.0.1:8000/api/accounts";

// Redirect if not logged in
if (!token) {
    window.location.href = "index.html";
}

// Generic API call
function api(url, method = "GET", body = null) {
    const options = {
        method,
        headers: {
            "Authorization": "Token " + token
        }
    };
    if (body) {
        options.headers["Content-Type"] = "application/json";
        options.body = JSON.stringify(body);
    }
    return fetch(API + url, options).then(res => res.json());
}

// Show status message
function showStatus(msg) {
    const statusEl = document.getElementById("status");
    if (statusEl) {
        statusEl.innerText = msg;
        setTimeout(() => statusEl.innerText = "", 3000);
    } else {
        console.log(msg);
    }
}

// Start work
document.getElementById("startBtn").onclick = () => {
    api("/work/", "POST", { action: "start" })
        .then(res => {
            showStatus(res.message || "Work started");
            loadAdminDashboard();
        })
        .catch(() => showStatus("Error starting work"));
};

// Stop work
document.getElementById("stopBtn").onclick = () => {
    api("/work/", "POST", { action: "stop" })
        .then(res => {
            showStatus(res.message || "Work stopped");
            loadAdminDashboard();
        })
        .catch(() => showStatus("Error stopping work"));
};

// Load admin dashboard
function loadAdminDashboard() {
    api("/today/")
    .then(data => {
        // Update date
        document.getElementById("date").innerText = `Date: ${data.date}`;

        // Update total time
        document.getElementById("totalTime").innerText = `Total hours: ${data.total_hours}`;

        // Update sessions table
        const sessionsDiv = document.getElementById("sessions");
        sessionsDiv.innerHTML = "";
        data.sessions.forEach(s => {
            const runningStyle = s.running ? "background-color:#d4edda;" : "";
            sessionsDiv.innerHTML += `
                <tr style="${runningStyle}">
                    <td>${s.start}</td>
                    <td>${s.end || "Running"}</td>
                    <td>${s.minutes}</td>
                    <td>${s.running ? "Running" : "Stopped"}</td>
                </tr>
            `;
        });

        // Update Start/Stop buttons text
        const startBtn = document.getElementById("startBtn");
        const stopBtn = document.getElementById("stopBtn");
        if (data.running) {
            startBtn.disabled = true;
            stopBtn.disabled = false;
        } else {
            startBtn.disabled = false;
            stopBtn.disabled = true;
        }
    })
    .catch(() => showStatus("Failed to load dashboard"));

    // Load users table if needed (optional)
    api("/admin-dashboard/").then(data => {
        const usersDiv = document.getElementById("users");
        if (usersDiv && data.users) {
            usersDiv.innerHTML = "";
            data.users.forEach(user => {
                const status = user.is_running ? "RUNNING" : "Stopped";
                const bg = user.is_running ? "#d4edda" : "white";
                usersDiv.innerHTML += `
                    <tr style="background-color:${bg}">
                        <td>${user.username}</td>
                        <td>${user.today_minutes}</td>
                        <td>${user.today_hours}</td>
                        <td>${status}</td>
                    </tr>
                `;
            });
        }
    });
}

// Payroll PDF
document.getElementById("payrollBtn").onclick = () => {
    const month = document.getElementById("month").value;
    window.open(`${API}/monthly_payroll_pdf/?month=${month}&token=${token}`);
};

// Initial load
loadAdminDashboard();
setInterval(loadAdminDashboard, 30000);
