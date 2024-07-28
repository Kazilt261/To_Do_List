function submit_login(event) {
    event.preventDefault();
    const form = document.getElementById("form_login");
    const data = new FormData(form);
    var status = true;
    if (data.get("email").length < 5) {
      document.getElementById("email_label").classList.add("error");
      status = false;
    } else {
      document.getElementById("email_label").classList.remove("error");
    }
    if (data.get("password").length < 8) {
      document.getElementById("password_label").classList.add("error");
      status = false;
    } else {
      document.getElementById("password_label").classList.remove("error");
    }
  
    if (status) {
      fetch("/users/login", {
        method: "POST",
        body: data,
      })
        .then((response) => {
          if (response.status === 200) {
            window.location.href = "/";
          } else {
            response.json().then((data) => {
              if (data.error === "username") {
                document.getElementById("user_label").classList.add("error");
              }
            });
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    }
  }