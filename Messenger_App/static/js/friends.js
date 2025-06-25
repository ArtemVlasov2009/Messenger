document.addEventListener('DOMContentLoaded', () => {
    const deleteButtons = document.querySelectorAll('.btn-secondary');
    const modalOverlay = document.getElementById('deleteModal');
    const confirmDeleteBtn = document.getElementById('confirmDelete');
    const cancelDeleteBtn = document.getElementById('cancelDelete');

    function showModal() {
        if (modalOverlay) {
            modalOverlay.classList.remove('hidden');
            modalOverlay.style.display = 'flex';
        }
    }

    function hideModal() {
        if (modalOverlay) {
            modalOverlay.classList.add('hidden');
            modalOverlay.style.display = 'none';
        }
    }

    deleteButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            showModal();
        });
    });

    if (cancelDeleteBtn) {
        cancelDeleteBtn.addEventListener('click', () => {
            hideModal();
        });
    }

    if (confirmDeleteBtn) {
        confirmDeleteBtn.addEventListener('click', () => {
            alert('User would be deleted now!');
            hideModal();
        });
    }

    if (modalOverlay) {
        modalOverlay.addEventListener('click', (event) => {
            if (event.target === modalOverlay) {
                hideModal();
            }
        });
    }

    hideModal();
});