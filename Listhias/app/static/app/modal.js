
function openModal() {
    const modal = document.getElementById("modal");
    modal.classList.add("show");
    modal.classList.remove("hidden");
}

function closeModal() {
    const modal = document.getElementById("modal");
    modal.classList.add("hidden");
    modal.classList.remove("show");
}

function closeModalIfNotEmpty() {
    const inputField = document.getElementById('task-title');
    
    if (inputField.value != "") {
        closeModal();  // Only close the modal if there's text in the input
    }
}

document.body.addEventListener("htmx:afterRequest", (event) => {
    if (event.detail.target.id === "modal-content") {
        openModal();
    }
});