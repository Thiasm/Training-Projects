function openModal() {
    console.log('Open Modal')
    const modal = document.getElementById("modal");
    modal.classList.add("show");
    modal.classList.remove("hidden");
}

function openDropdownMenu() {
    const dropdownButton = document.getElementById('filter-button');
    const isHidden = dropdownMenu.classList.toggle('hidden');

    if (!isHidden) {
        // Add the event listener to close the dropdown when clicking outside
        document.addEventListener('click', closeDropdownMenuOnClickOutside);
        dropdownButton.classList.add('bg-gray-300');
    } else {
        // Remove the event listener when dropdown is hidden
        document.removeEventListener('click', closeDropdownMenuOnClickOutside);
        dropdownButton.classList.remove('bg-gray-300');
    }
}

function closeDropdownMenuOnClickOutside(event) {
    const dropdownMenu = document.getElementById('dropdownMenu');
    const dropdownButton = document.getElementById('filter-button');
    
    if (!dropdownMenu.contains(event.target) && !dropdownButton.contains(event.target)) {
        dropdownMenu.classList.add('hidden');
        document.removeEventListener('click', closeDropdownMenuOnClickOutside);
        dropdownButton.classList.remove('bg-gray-300');
    }
}

function closeModal() {
    console.log('close modal');
    const modal = document.getElementById("modal");
    modal.classList.add("hidden");
    modal.classList.remove("show");
}

function closeModalOnOutsideClick(event) {
    const modalContent = document.getElementById('modal-content');

    if (!modalContent.contains(event.target) && !event.target.closest('.modal-content')) {
        closeModal();
    } 
}

function closeModalIfNotEmpty(inputId) {
    console.log('close modal if not empty');
    const inputField = document.getElementById(inputId);
    // console.log(inputField);
    // console.log(inputId);
    
    if (inputField.value != "") {
        closeModal(); 
    }
}
