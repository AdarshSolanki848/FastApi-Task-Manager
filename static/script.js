const taskInput=document.getElementById("taskInput")
const addBtn=document.getElementById("addBtn")
const taskList=document.getElementById("taskList")

addBtn.addEventListener("click",addTask);

async function loadTasks() {
    console.log("Loadtasks called");
    const response= await fetch("/tasks");
    const tasks= await response.json()
    taskList.innerHTML="";
    if(tasks.length===0){
        const message=document.createElement("div");
        message.className="empty-task";
        message.textContent="No Task! Please Add Task";
        taskList.appendChild(message);
        return;
    }
    
    tasks.forEach(task => {

    const li=document.createElement("li");
    li.className="task-card";

    const taskInfo=document.createElement("div");
    taskInfo.className="task-info";

    const buttons=document.createElement("div");
    buttons.className="buttons";


    const tick=document.createElement("input");
    tick.checked=task.completed
    tick.type="checkbox";
    tick.className="Check";
    tick.addEventListener('change',()=>{updateTask(task.id,tick.checked)});

    const title=document.createElement("span");
    title.textContent=task.title;
    title.className="title";
    if(task.completed){
        title.classList.add("completed");
    }

    const deleteBtn=document.createElement("button");
    deleteBtn.textContent="🗑️";
    deleteBtn.className="delete-btn";
    deleteBtn.addEventListener("click",()=>{delTask(task.id)});


    taskInfo.appendChild(tick);
    taskInfo.appendChild(title);

    buttons.appendChild(deleteBtn);
    li.appendChild(taskInfo);
    li.appendChild(buttons);
    

    taskList.appendChild(li)
    });    
}

async function addTask() {
    const title=taskInput.value;
    if(title.trim()===""){
        alert("Please enter a task");
        return;
    }
    console.log(title);
    console.log(title.length);
    if(title.length>99){
        alert("⚠️Task length is too long!");
        return;
    }
    const response=await fetch("/tasks",{
        method:"Post",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            title:title
        })
    });
    const newTask=await response.json();
    loadTasks();
    taskInput.value = "";
}



async function delTask(id){
    if(confirm("Delete this task?")){
        const response=await fetch(`/tasks/${id}`,
            {
                method:"Delete",
            });
    
            if(response.ok){
                loadTasks();
            }
            else{
                alert("Task Not Found");
            }
    }
}
loadTasks();

async function updateTask(id,completed) {
    const response=await fetch(`/tasks/${id}`,
        {
            method:"Put",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                completed:completed
            })
        }
    )
    if(response.ok){
        await loadTasks();
    }
    else{
        alert("Task not Found");
    }
}