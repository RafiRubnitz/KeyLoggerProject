// window.onload = function() {
//     users = load_users();
// }


async function submit() {
    let username = document.getElementById("username").value
    let password = document.getElementById("password").value
    let verify_password = document.getElementById("verify_password")

    if (verify_password.style.display == "none" || verify_password.style.display == "")
    {
        window.location.href = "../index.html"
        // if (await verify_user(username,password)) {
        //     window.location.href = "../index.html"
        // }
        // else {
        //     document.getElementById("output").innerHTML("wrong password")
        // }
    }
    else {
        if (username in users) {
            
        }
        else {
            if (password == verify_password.value) {

            }
            else {

            }
        }
    }
}

async function verify_user(username,password) {

    try {
        const response = await fetch("http://127.0.0.1:5000/user_verification",{
            method : "POST",
            headers : {
                "content-type" : "applicetion/json"
            },
            body : JSON.stringify({"username" : username,"password" : password})
        });
        if (!response.ok){
            alert("cann't response")
        }
        const data = await response.json();
        return data["message"];
    }
    catch(error) {
        alert("network doesn't working")
        return false
    }
}

function new_user() {
    let verify_password = document.getElementById("verify_password")
    if (verify_password.style.display == "none" || verify_password.style.display == "") {
        verify_password.style.display = "block"
        document.getElementById("sign_up").textContent = "sign in"
    }
    else {
        verify_password.style.display = "none"
        document.getElementById("sign_up").textContent = "sign up"
    }
}

