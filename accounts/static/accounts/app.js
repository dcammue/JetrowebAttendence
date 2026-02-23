const API = "http://127.0.0.1:8000/api/accounts";

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
