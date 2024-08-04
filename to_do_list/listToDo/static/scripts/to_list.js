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
    setTimeout(() => {
      generateList();
    }, 2000);
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
  return `<div class="block-task task-id-${id}" onClick="showTaskInfo(${id})">
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

function showModalAdd(){
  modalAdd.style.display = "flex";
}

function hideModalAdd(){
  modalAdd.style.display = "none";
}

//!LOGIC FOR INFO TASK!//

const h3Title = document.getElementById("title-task");
const divIcon = document.getElementById("icon-status");
const limitTime = document.getElementById("limit-time");
const description = document.getElementById("description-task");

function showTaskInfo(id) {
  console.log("Mostrando tarea con id: " + id);
  //!Show loading
  //!AQUI TENEMOS QUE CAMBIAR TODO LO QUE ESTAMOS MOSTRANDO
  //!POR EL CONTENIDO DE LA TAREA QUE FUE SELECCIONADO
}

//!LOGIC FOR ADD TASK!//
function saveTask() {
  console.log("Enviando tarea");
}

function addTask() {
  console.log("Agregando tarea");
}