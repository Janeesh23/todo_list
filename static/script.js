document.addEventListener("DOMContentLoaded", function() {
    fetch("/tasks")
    .then(response => response.json())
    .then(data => {
        const taskList = document.getElementById("taskList");
        taskList.innerHTML = "";
        data.tasks.forEach(task => {
            const listItem = document.createElement("li");
            listItem.textContent = task.title + (task.completed ? " ✅" : " ❌");
            listItem.setAttribute("data-id", task.id);

            // Add delete button
            const deleteBtn = document.createElement("button");
            deleteBtn.textContent = "❌";
            deleteBtn.addEventListener("click", function() {
                fetch(`/tasks/${task.id}`, { method: "DELETE" })
                .then(() => location.reload());
            });

            // Add toggle complete button
            const toggleBtn = document.createElement("button");
            toggleBtn.textContent = task.completed ? "Undo" : "Complete";
            toggleBtn.addEventListener("click", function() {
                fetch(`/tasks/${task.id}`, {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ completed: !task.completed })
                })
                .then(() => location.reload());
            });

            listItem.appendChild(deleteBtn);
            listItem.appendChild(toggleBtn);
            taskList.appendChild(listItem);
        });
    });

    document.getElementById("addTaskBtn").addEventListener("click", function() {
        const title = document.getElementById("taskInput").value;
        fetch("/tasks", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title: title })
        })
        .then(response => response.json())
        .then(() => location.reload());
    });
});
