document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('modal');
    const openBtn = document.querySelector('.publish-button');
    const closeBtn = document.querySelector('.close-button');
    const deleteModal = document.getElementById('delete-modal');
    const deleteConfirmBtn = document.querySelector('.delete-confirm-button');
    const deleteCancelBtn = document.querySelector('.delete-cancel-button');
    const questionInput = document.querySelector('.question-input');
    const postTextArea = document.getElementById('post-text');
    let currentPostId = null;

    // Открыть основное модальное окно для создания поста
    openBtn?.addEventListener('click', function() {
        modal.style.display = 'flex';
        deleteModal.style.display = 'none';
        if (questionInput?.value.trim() !== '') {
            postTextArea.value = questionInput.value;
            questionInput.value = '';
        }
    });

    // Закрыть основное модальное окно
    closeBtn?.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    // Закрыть основное модальное окно при клике вне контента
    window.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Показать основное модальное окно, если есть ошибки формы
    const formErrorList = document.querySelector('.custom-post-form .errorlist');
    if (formErrorList?.children.length > 0) {
        modal.style.display = 'flex';
    }

    // Обработка клика по иконке Dots.svg
    document.querySelectorAll('.dots-icon').forEach(function(dotsIcon) {
        dotsIcon.addEventListener('click', function(e) {
            e.stopPropagation();
            currentPostId = this.getAttribute('data-post-id');
            const rect = this.getBoundingClientRect();
            deleteModal.style.display = 'block';
            deleteModal.style.top = `${rect.bottom + window.scrollY}px`;
            deleteModal.style.left = `${rect.left + window.scrollX - 180}px`;
            modal.style.display = 'none';
        });
    });

    // Закрыть модальное окно удаления при клике на "Скасувати"
    deleteCancelBtn?.addEventListener('click', function() {
        deleteModal.style.display = 'none';
        currentPostId = null;
    });

    // Обработка удаления поста
    deleteConfirmBtn?.addEventListener('click', function() {
        if (currentPostId) {
            fetch(`/posts/delete/${currentPostId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (response.ok) {
                    document.querySelector(`.post-frame:has([data-post-id="${currentPostId}"])`)?.remove();
                    deleteModal.style.display = 'none';
                    currentPostId = null;
                } else {
                    alert('Помилка при видаленні поста');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Помилка при видаленні поста');
            });
        }
    });

    // Закрыть модальное окно удаления при клике вне его
    window.addEventListener('click', function(e) {
        if (!deleteModal.contains(e.target) && !e.target.classList.contains('dots-icon')) {
            deleteModal.style.display = 'none';
            currentPostId = null;
        }
    });

    // Функция для получения CSRF-токена
    function getCookie(name) {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [cookieName, cookieValue] = cookie.trim().split('=');
            if (cookieName === name) {
                return decodeURIComponent(cookieValue);
            }
        }
        return null;
    }
});
