function handleDragOver(event) {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'copy';
    document.getElementById('dropArea').classList.add('highlight');
}

function handleDragLeave(event) {
    event.preventDefault();
    document.getElementById('dropArea').classList.remove('highlight');
}

function handleDrop(event) {
    event.preventDefault();
    document.getElementById('dropArea').classList.remove('highlight');
    const files = event.dataTransfer.files;
    handleFiles(files);
}

function handleFiles(files) {
    document.getElementById('uploadForm').file.files = files;
    submitForm();
}   

function submitForm() {
    document.getElementById('uploadForm').submit();
}

function toggleForm() {
    var form = document.getElementById('uploadForm');
    form.classList.toggle('closed');
    document.getElementById('toggleFormButton').textContent = form.classList.contains('closed') ? 'DB Hochladen' : 'ausblenden';
}

function toggleDarkMode() {
    var body = document.body;
    var button = document.querySelector('.dark-mode-button');
    body.classList.toggle('dark-mode');
    if (body.classList.contains('dark-mode')) {
        button.textContent = '🌞';
    } else {
        button.textContent = '🌙';
    }
}