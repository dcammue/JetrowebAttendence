const API = "https://jetrowebattendence.onrender.com/api/accounts";

const token = localStorage.getItem("token");

function api(url, method="POST", body=null) {
    return fetch(API + url, {
        method: method,
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Token " + token
        },
        body: body ? JSON.stringify(body) : null
    }).then(res => res.json());
}
