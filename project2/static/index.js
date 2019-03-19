if (!localStorage.getItem("username")) {
    // Redirect user
    if (window.location.pathname !== "/")
        window.location.pathname = "/"

    document.querySelector("#submit-button").disabled = true

    document.querySelector("#username").onkeyup = () => {
        if (document.querySelector("#username").value.length > 0) {
                document.querySelector("#submit-button").disabled = false
            }
        }

    document.querySelector("#form").onsubmit = () => {
        const user = document.querySelector("#username").value
            localStorage.setItem("username", user)
        }

} else {
    if(window.location.pathname !== "/chat") {
        window.location.pathname = "/chat"
    }
}