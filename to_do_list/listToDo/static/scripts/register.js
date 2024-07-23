function submit_register(event) {
  event.preventDefault();
  const form = document.getElementById("form_register");
  const data = new FormData(form);
  var status = true;
  if (data.get("username").length < 5) {
    document.getElementById("user_label").classList.add("error");
    status = false;
  } else {
    document.getElementById("user_label").classList.remove("error");
  }
  if (data.get("password").length < 8) {
    document.getElementById("password_label").classList.add("error");
    status = false;
  } else {
    document.getElementById("password_label").classList.remove("error");
  }
  if (data.get("password") !== data.get("confirm_password")) {
    document.getElementById("password2_label").classList.add("error");
    status = false;
  } else {
    document.getElementById("password2_label").classList.remove("error");
  }
  if (data.get("email").length < 5) {
    document.getElementById("email_label").classList.add("error");
    status = false;
  } else {
    document.getElementById("email_label").classList.remove("error");
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
            if (data.error === "username") {
              document.getElementById("user_label").classList.add("error");
            } else if (data.error === "email") {
              document.getElementById("email_label").classList.add("error");
            }
          });
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
}
