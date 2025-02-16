var my_username = "rafi"
var my_password = "1234"

function submit() {
    let username = document.getElementById("username").value
    let password = document.getElementById("password").value

    if (username == my_username && password == my_password){
        window.location.href = "../index.html"
    }
}

function new_user() {
    let verify_password = document.getElementById("verify_password")
    if (verify_password.style.display == "none") {
        verify_password.style.display = "block"
        document.getElementById("sign_up").textContent = "sign in"
    }
    else {
        verify_password.style.display = "none"
        document.getElementById("sign_up").textContent = "sign up"
    }
}