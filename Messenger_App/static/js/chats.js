document.addEventListener('DOMContentLoaded', function() {
    function formatTime(isoString) {
        if (!isoString) return '';
        const date = new Date(isoString);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hourCycle: 'h23' });
    }


    document.querySelectorAll('.message-time[data-timestamp]').forEach(timeElement => {
        timeElement.textContent = formatTime(timeElement.getAttribute('data-timestamp'));
    });

    const modal = document.getElementById('group-chat-modal');
    const createGroupBtn = document.getElementById('create-group-chat-btn');
    const closeModalSpan = document.querySelector('.modal .close');
    const groupChatForm = document.getElementById('create-group-chat-form');


    const modalStep1 = document.getElementById('modal-step-1');
    const modalStep2 = document.getElementById('modal-step-2');
    const nextBtn = document.getElementById('modal-next-btn');
    const backBtn = document.getElementById('modal-back-btn');
    const cancelBtn1 = document.getElementById('modal-cancel-btn-1');

    const avatarPreview = document.getElementById('group-avatar-preview');
    const avatarInput = document.getElementById('group-avatar-input');
    const photoActions = document.getElementById('photoActionsContainer');

    const membersChecklist = modalStep1.querySelector('.members-list');
    const selectedMembersContainer = document.getElementById('selected-members-list');

    if (createGroupBtn && modal) {

        createGroupBtn.onclick = function() {
            resetModal();
            modal.style.display = 'block';
        }

        closeModalSpan.onclick = () => modal.style.display = 'none';
        cancelBtn1.onclick = () => modal.style.display = 'none';
        window.onclick = (event) => {
            if (event.target == modal) {
                modal.style.display = 'none';
            }
        };

        nextBtn.onclick = function() {
            const selectedMembers = membersChecklist.querySelectorAll('input[name="members"]:checked');
            if (selectedMembers.length === 0) {
                alert('Будь ласка, оберіть хоча б одного учасника.');
                return;
            }
            updateSelectedMembersList();
            modalStep1.style.display = 'none';
            modalStep2.style.display = 'block';
        };

        backBtn.onclick = function() {
            modalStep2.style.display = 'none';
            modalStep1.style.display = 'block';
        };

        if (avatarPreview && avatarInput && photoActions) {
            [avatarPreview, photoActions].forEach(el => {
                el.onclick = () => avatarInput.click();
            });
            avatarInput.onchange = function(event) {
                const file = event.target.files[0];
                if (file) {
                    avatarPreview.src = URL.createObjectURL(file);
                }
            };
        }

        groupChatForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const selectedMembers = membersChecklist.querySelectorAll('input[name="members"]:checked');
            if (selectedMembers.length === 0) {
                alert('Помилка: не обрано жодного учасника. Будь ласка, поверніться назад та оберіть учасників.');
                return;
            }

            const formData = new FormData(this);
            const csrfToken = formData.get('csrfmiddlewaretoken');

            fetch('/create_group_chat/', {
                method: 'POST',
                body: formData,
                headers: { 'X-CSRFToken': csrfToken }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = data.chat_url;
                } else {
                    alert('Помилка створення групи: ' + (data.error || 'Невідома помилка'));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Сталася мережева помилка. Спробуйте ще раз.');
            });
        });

        selectedMembersContainer.addEventListener('click', function(e) {
            if (e.target.classList.contains('remove-member-btn')) {
                const userId = e.target.dataset.userId;
                e.target.closest('.selected-member-item').remove();
                const checkbox = membersChecklist.querySelector(`input[value="${userId}"]`);
                if (checkbox) {
                    checkbox.checked = false;
                }
            }
        });
    }

    function resetModal() {
        groupChatForm.reset();
        modalStep1.style.display = 'block';
        modalStep2.style.display = 'none';
        selectedMembersContainer.innerHTML = '';
        avatarPreview.src = "{% static 'images/gruppa.svg' %}"; 
    }

    function updateSelectedMembersList() {
        selectedMembersContainer.innerHTML = '';
        const selectedMembers = membersChecklist.querySelectorAll('input[name="members"]:checked');
        selectedMembers.forEach(checkbox => {
            const userId = checkbox.value;
            const username = checkbox.dataset.username;
            const avatarUrl = checkbox.dataset.avatar;

            const memberItem = document.createElement('div');
            memberItem.className = 'modal-user-item selected-member-item';
            memberItem.innerHTML = `
                <img src="${avatarUrl}" alt="${username}'s Avatar" class="modal-user-avatar">
                <span>${username}</span>
                <button type="button" class="remove-member-btn" data-user-id="${userId}">Видалити</button>
            `;
            selectedMembersContainer.appendChild(memberItem);
        });
    }

    const groupPkElement = document.getElementById('groupPk');
    if (groupPkElement) {
        const groupPk = groupPkElement.value;
        const messagesContainer = document.getElementById('messages');
        const messageForm = document.getElementById('message-form');
        const messageInput = document.getElementById('message-input');
        const currentUsername = JSON.parse(document.getElementById('current-username').textContent);
        
        const addPhotoButton = document.getElementById('add-photo-btn');
        const imageUploadInput = document.getElementById('image-upload-input');
        const csrfToken = document.querySelector('#message-form [name=csrfmiddlewaretoken]').value;

        addPhotoButton.addEventListener('click', () => imageUploadInput.click());

        imageUploadInput.addEventListener('change', () => {
            const file = imageUploadInput.files[0];
            if (file) {
                const formData = new FormData();
                formData.append('image', file);
                formData.append('group_pk', groupPk);
                fetch('/chat/upload_image/', { method: 'POST', headers: { 'X-CSRFToken': csrfToken }, body: formData })
                .then(response => response.json()).then(data => { if (!data.success) alert('Помилка: ' + data.error); })
                .catch(error => console.error('Error uploading image:', error));
                imageUploadInput.value = '';
            }
        });

        const webSocket = new WebSocket(`ws://${window.location.host}/ws/chat/${groupPk}/`);
        if (messagesContainer) { messagesContainer.scrollTop = messagesContainer.scrollHeight; }

        webSocket.onmessage = function(event) {
            const data = JSON.parse(event.data);
            if (data.type !== 'chat') return;
            const isSentByMe = data.username === currentUsername;
            const messageClass = isSentByMe ? 'sent' : 'received';
            let messageContentHtml = '';
            if (data.message) { messageContentHtml += `${data.message.replace(/\n/g, '<br>')}`; }
            if (data.image_url) { messageContentHtml += `<a href="${data.image_url}" target="_blank"><img src="${data.image_url}" alt="Attached image"></a>`; }
            let authorHtml = '';
            if (!isSentByMe && document.querySelector('.message-author')) { authorHtml = `<div class="message-author">${data.username}</div>`; }
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('message', messageClass);
            messageDiv.innerHTML = `<div class="message-body"><div class="message-content">${messageContentHtml}</div><span class="message-time">${formatTime(data.sent_at)}</span></div>`;
            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        };

        webSocket.onerror = (error) => console.error('WebSocket Error:', error);

        messageForm.addEventListener('submit', function(event) {
            event.preventDefault();
            if (messageInput.value.trim()) {
                webSocket.send(JSON.stringify({ 'message': messageInput.value }));
                messageInput.value = '';
                messageInput.focus();
            }
        });
    }

    document.querySelectorAll('.contacts-list-users-1').forEach(contact => {
        contact.addEventListener('click', function() {
            const userId = this.getAttribute('data-user-id');
            if (userId) { window.location.href = `/to_personal_chat/${userId}/`; }
        });
    });
});