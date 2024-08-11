const listTasks = document.getElementById("colum-tasks");
const inputFilter = document.getElementById("filter-tasks");
const divInput = document.getElementById("div-input-search");

//!DIV FOR INFO TASK!//
const divInfoTask = document.getElementById("info-task");
const divTaskNotSelect = document.getElementById("not-selected");
const mainLoading = document.getElementById("main-loading");
const modalAdd = document.getElementById("div-modal-add");

var filter = "";
var tasks = null;

console.log("Hola mundo");

async function chargeTasks() {
  return fetch("/task/list")
    .then((response) => response.json())
    .then((data) => {
      tasks = data.tasks;
      console.log(tasks);
    });
}

function init() {
  inputFilter.addEventListener("input", filterTasks);
  divInput.addEventListener("click", () => {
    inputFilter.focus();
  });
  chargeTasks().then(() => {
    generateList();
  });
}

function generateList() {
  if (listTasks == null) {
    console.log("No se encontro el elemento");
    return;
  }
  listTasks.innerHTML = "";
  tasks.forEach((task) => {
    if (task.title.includes(filter)) {
      listTasks.innerHTML += createTask(task.title, task.id, task.status);
    }
  });
}

function createTask(nameTask, id, status) {
  return `<div class="block-task task-id-${id} row-animation-add" onClick="showTaskInfo(${id})">
  ${
    status == true
      ? '<span class="material-symbols-rounded">check_circle</span>'
      : '<span class="material-symbols-rounded">radio_button_unchecked</span>'
  }
    <div class ="info-task">
        <h4>${nameTask}</p>
    </div>
  </div>`;
}

function filterTasks() {
  filter = inputFilter.value;
  generateList();
}

init();

//!UTILS!//
function showInfoTask() {
  divTaskNotSelect.style.display = "none";
  mainLoading.style.display = "none";
  divInfoTask.style.display = "flex";
}

function hideInfoTask() {
  divTaskNotSelect.style.display = "flex";
  mainLoading.style.display = "none";
  divInfoTask.style.display = "flex";
}

function showLoading() {
  divTaskNotSelect.style.display = "none";
  mainLoading.style.display = "flex";
  divInfoTask.style.display = "none";
}

function showModalAdd() {
  modalAdd.style.display = "flex";
}

function hideModalAdd() {
  modalAdd.style.display = "none";
}

//!LOGIC FOR INFO TASK!//

const h3Title = document.getElementById("title-task");
const divIcon = document.getElementById("icon-status");
const limitTime = document.getElementById("limit-time");
const description = document.getElementById("description-task");

function showTaskInfo(id) {
  showLoading();
  fetch(`task/detail/${id}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  }).then((response) => {
    if (response.status != 200) {
      alert("Error:", error);
    } else {
      response.json().then((data) => {
        if (h3Title) {
          h3Title.textContent = data.title;
        }
        if (limitTime) {
          limitTime.textContent = data.end_date;
        }
        if (description) {
          description.textContent = data.description;
        }
        showInfoTask();
      });
    }
  });
}

//!LOGIC FOR ADD TASK!//
const formAddTask = document.getElementById("form-add-task");
const buttonAddTask = document.getElementById("button-add-task");
formAddTask.addEventListener("submit", saveTask);

function saveTask() {
  console.log("Enviando tarea");
}

function addTask() {
  showModalAdd();
}

function closeModal() {
  hideModalAdd();
}

function saveTask(event) {
  event.preventDefault();
  const data = new FormData(formAddTask, buttonAddTask);
  const title = data.get("taskName");
  const limit_time = data.get("taskLimitTime").toString();
  const description = data.get("taskDescription");
  if (title == "") {
    alert("The title can't be empty");
    return;
  }
  if (limit_time == "") {
    alert("The limit time can't be empty");
    return;
  }
  if (new Date(limit_time) < new Date()) {
    alert("The limit time can't be less than the current date");
    return;
  }
  if (description == "") {
    alert("The description can't be empty");
    return;
  }

  console.log(
    "Title: " + title,
    "Limit time: " + limit_time,
    "Description: " + description
  );

  fetch("/task/create", {
    method: "POST",
    body: data,
  }).then((response) => {
    if (response.status === 201) {
      return response.json().then((data) => {
        alert("Task added successfully");
        const task = {
          id: data.id,
          title: title,
          end_date: limit_time,
          description: description,
          status: false,
        };
        tasks.push(task);
        tasks.sort((a, b) => new Date(a.end_date) - new Date(b.end_date));
        console.log(tasks);
        //Put the task in the list but ordered by date
        const listTasksShowed = Array.from(listTasks.children);
        if (listTasksShowed.length == 0) {
          listTasks.innerHTML = createTask(task.title, task.id, task.status);
          hideModalAdd();
          return;
        }

        const newdiv = document.createElement("div");
        newdiv.innerHTML = createTask(task.title, task.id, task.status);

        listTasks.appendChild(newdiv);

        hideModalAdd();
      });
    } else {
      alert("Error adding task");
      return null;
    }
  });
}

//!LOGIC FOR POPUP USER!//
const buttonUser = document.getElementById("button-user");
const popupUser = document.getElementById("popup-user");

var isOpenPopup = false;

buttonUser.addEventListener("click", () => {
  if (isOpenPopup) {
    closePopupUser();
    return;
  } else {
    popupUser.style.display = "block";
    isOpenPopup = true;
  }
});

function closePopupUser() {
  popupUser.style.display = "none";
  isOpenPopup = false;
}

//!LOGIC FOR NAVBAR MOVILE!//
const navbar = document.getElementById("navbar-left");

function openNavbar() {
  if (navbar.className == "") {
    return;
  }
  navbar.className = "";
}

function closeNavbar() {
  if (navbar.className == "closed") {
    return;
  }
  navbar.className = "closed";
}

const buttonOpenNavbar = document.getElementById("button-navbar");

buttonOpenNavbar.addEventListener("click", () => {
  openNavbar();
});

document.addEventListener("click", (event) => {
  if (!navbar.contains(event.target) && !buttonOpenNavbar.contains(event.target)) {
    closeNavbar();
  }
});
