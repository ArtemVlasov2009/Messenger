
document.addEventListener('DOMContentLoaded', function() {
    const messagesDisplay = document.getElementById('messages-display');
    if (messagesDisplay) {
        messagesDisplay.scrollTop = messagesDisplay.scrollHeight;
    }

    const textarea = document.querySelector('.message-input-area .message-textarea');
    if (textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto'; 
            this.style.height = (this.scrollHeight) + 'px'; 
        });
        textarea.style.height = (textarea.scrollHeight) + 'px';
    }

    if (textarea) {
        textarea.focus();
    }
});