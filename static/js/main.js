function openTaskModal(assignee = '', date = '') {
    const modal = document.getElementById('taskModal');
    if (assignee) {
        document.getElementById('modalAssignee').value = assignee;
    }
    if (date) {
        document.getElementById('modalDate').value = date;
    }
    modal.classList.add('active');
}

function openTaskDetails(title, status, complexity, assignee, description) {
    const modal = document.getElementById('detailsModal');
    document.getElementById('dt_title').innerText = title;
    document.getElementById('dt_status').innerText = status;
    document.getElementById('dt_assignee').innerText = assignee;
    document.getElementById('dt_desc').innerText = description;
    modal.classList.add('active');
}

function closeModals(event) {
    if (event && !event.target.classList.contains('modal-overlay')) {
        return;
    }
    document.querySelectorAll('.modal-overlay').forEach(m => m.classList.remove('active'));
}

// Close on escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeModals();
    }
});
