function submit_register(event) {
  event.preventDefault();
  const form = document.getElementById("form_register");
  const data = new FormData(form);
  var status = true;
  if (data.get("username").length < 5) {
    document.getElementById("user").classList.add("error");
    status = false;
  } else {
    document.getElementById("user").classList.remove("error");
  }
  if (data.get("password").length < 8) {
    document.getElementById("password").classList.add("error");
    status = false;
  } else {
    document.getElementById("password").classList.remove("error");
  }
  if (data.get("password") !== data.get("confirm_password")) {
    document.getElementById("password2").classList.add("error");
    status = false;
  } else {
    document.getElementById("password2").classList.remove("error");
  }
  if (data.get("email").length < 5) {
    document.getElementById("email").classList.add("error");
    status = false;
  } else {
    document.getElementById("email").classList.remove("error");
  }

  if (status) {
    fetch("/users/register", {
      method: "POST",
      body: data,
    })
      .then((response) => {
        if (response.status === 201) {
          window.location.href = "/users/login";
        } else {
          response.json().then((data) => {
            div_error = document.getElementById("error-div");
            div_error.innerHTML = `<p>${data.details}</p>`;
            if (data.error === "username") {
              document.getElementById("user").classList.add("error");
              document.getElementById("user_input").classList.add("error");
              document.getElementById("user_input").focus();
            }
            if (data.error === "password") {
              document.getElementById("password").classList.add("error");
              document.getElementById("password_input").classList.add("error");
              document.getElementById("password_input").focus();
            }
            if (data.error === "email") {
              document.getElementById("email").classList.add("error");
              document.getElementById("email_input").classList.add("error");
              document.getElementById("email_input").focus();
            }
          });
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
}
