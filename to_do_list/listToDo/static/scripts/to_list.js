const listTasks = document.getElementById("colum-tasks");
const inputFilter = document.getElementById("filter-tasks");
const divInput = document.getElementById("div-input-search")

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

function addTask() {
  console.log("Agregando tarea");
}

function init() {
  inputFilter.addEventListener("input", filterTasks);
  divInput.addEventListener("click", ()=>{
    inputFilter.focus()
  })
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
  return `<div class="block-task task-id-${id}">
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
