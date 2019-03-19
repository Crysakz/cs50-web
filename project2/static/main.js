document.addEventListener("DOMContentLoaded", () => {

    if (!localStorage.getItem("username")) {
        document.querySelector("#submit-button").disabled = true

        document.querySelector("#username").onkeyup = () => {
            if (document.querySelector("#username").value.length > 0) {
                document.querySelector("#submit-button").disabled = false
            }
        }

        document.querySelector("#form").onsubmit = () => {
            const user = document.querySelector("#username").value

            localStorage.setItem("username", user)
            alert(user)
        }
    } else {
        alert(localStorage.getItem("username"))
    }
})
