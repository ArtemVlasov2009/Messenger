document.addEventListener('DOMContentLoaded', function() {
    const loginInput = document.getElementById('id_login');
    const firstVisitModal = document.getElementById('firstVisitModal');
    const modalActionForm = document.getElementById('modalActionForm');
    const modal = document.getElementById('modal');
    const deleteModal = document.getElementById('delete-modal');
    const closeButton = document.querySelector('.close-button');
    const publishButton = document.querySelector('.publish-button');
    const deleteConfirmButton = document.querySelector('.delete-confirm-button');
    const editPostButton = document.querySelector('.edit-post-button');
    const postForm = document.getElementById('post-form');
    const modalTitle = document.getElementById('modal-title');
    const postIdInput = document.getElementById('post-id-input');
    const submitPostButton = document.getElementById('submit-post-button');
    const questionInput = document.querySelector('.question-input');
    const modalTextInput = document.getElementById('id_text');
    const imageInputs = [];
    const maxImages = 9;

    for (let i = 1; i <= maxImages; i++) {
        const input = document.getElementById('id_image' + i);
        if (input) {
            imageInputs.push(input);
        }
    }

    const imagePreviewContainer = document.getElementById('image-preview-container');
    const trashIconUrl = "/static/images/trash_img.svg";
    const addTagIcon = document.querySelector('.add-tag-icon');
    const tagContainer = document.querySelector('.tag-checkbox-list');
    let currentPostId = null;

    if (!localStorage.getItem('visited')) {
        firstVisitModal.style.display = 'flex';
        setTimeout(() => {
            firstVisitModal.style.opacity = '1';
        }, 10);
        localStorage.setItem('visited', 'true');
    }

    if (loginInput) {
        function applyLoginInputStyles() {
            loginInput.style.fontFamily = 'GT Walsheim Pro, sans-serif';
            loginInput.style.fontWeight = '400';
            loginInput.style.fontSize = '16px';
            loginInput.style.lineHeight = '22px';
            loginInput.style.letterSpacing = '-0.007em';
            loginInput.style.color = '#81818D';
        }

        function ensureAtSymbolAndApplyStyles() {
            if (!loginInput.value.startsWith('@')) {
                loginInput.value = '@' + loginInput.value;
            }
            applyLoginInputStyles();
        }

        loginInput.addEventListener('focus', ensureAtSymbolAndApplyStyles);
        loginInput.addEventListener('input', function() {
            if (!loginInput.value.startsWith('@')) {
                loginInput.value = '@' + loginInput.value.substring(1);
            }
            applyLoginInputStyles();
        });

        if (loginInput.value && !loginInput.value.startsWith('@')) {
            loginInput.value = '@' + loginInput.value;
            applyLoginInputStyles();
        } else if (!loginInput.value) {
            loginInput.value = '@';
            applyLoginInputStyles();
        } else {
            applyLoginInputStyles();
        }
    }

    window.addEventListener('click', function(event) {
        if (event.target == firstVisitModal) {
            firstVisitModal.style.opacity = '0';
            setTimeout(() => {
                firstVisitModal.style.display = 'none';
            }, 300);
        }
    });

    modalActionForm.addEventListener('submit', function(event) {
    });

    if (questionInput && modalTextInput) {
        questionInput.addEventListener('input', function() {
            modalTextInput.value = questionInput.value;
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function clearFormErrors() {
        document.querySelectorAll('.errorlist').forEach(el => el.remove());
    }

    function clearImagePreviews() {
        while (imagePreviewContainer.firstChild) {
            imagePreviewContainer.removeChild(imagePreviewContainer.firstChild);
        }
    }

    function addImagePreview(file, index) {
        const previewWrapper = document.createElement('div');
        previewWrapper.style.position = 'relative';
        previewWrapper.style.width = '217.67px';
        previewWrapper.style.height = '265px';
        previewWrapper.style.borderRadius = '16px';

        const img = document.createElement('img');
        img.style.width = '217.67px';
        img.style.height = '265px';
        img.style.borderRadius = '16px';
        img.style.objectFit = 'cover';
        img.file = file;

        previewWrapper.appendChild(img);

        const trashIcon = document.createElement('img');
        trashIcon.src = trashIconUrl;
        trashIcon.alt = 'Видалити зображення';
        trashIcon.style.position = 'absolute';
        trashIcon.style.top = '8px';
        trashIcon.style.right = '8px';
        trashIcon.style.width = '24px';
        trashIcon.style.height = '24px';
        trashIcon.style.cursor = 'pointer';

        trashIcon.addEventListener('click', () => {
            if (imageInputs[index]) {
                imageInputs[index].value = '';
            }
            previewWrapper.remove();
        });

        previewWrapper.appendChild(trashIcon);
        imagePreviewContainer.appendChild(previewWrapper);

        const reader = new FileReader();
        reader.onload = (function(aImg) { return function(e) { aImg.src = e.target.result; }; })(img);
        reader.readAsDataURL(file);
    }

    imageInputs.forEach((input, index) => {
        input.addEventListener('change', (event) => {
            clearImagePreviews();
            imageInputs.forEach((inp, i) => {
                if (inp.files && inp.files[0]) {
                    addImagePreview(inp.files[0], i);
                }
            });
        });
    });

    function openModal(isEditing = false, postData = {}) {
        clearFormErrors();
        modal.style.display = 'flex';

        if (isEditing) {
            modalTitle.textContent = 'Редагування публікації';
            submitPostButton.textContent = 'Зберегти зміни';
            postForm.action = `/posts/edit/${currentPostId}/`;
            postIdInput.value = currentPostId;

            document.getElementById('id_title').value = postData.title || '';
            document.getElementById('id_theme').value = postData.theme || '';
            modalTextInput.value = postData.text || '';
            document.getElementById('id_article_link').value = postData.article_link || '';

            const tagCheckboxes = document.querySelectorAll('.tag-buttons input[type="checkbox"]');
            tagCheckboxes.forEach(checkbox => {
                checkbox.checked = postData.tags && postData.tags.includes(checkbox.value);
            });

            const customTagInput = document.getElementById('id_custom_tag');
            if (customTagInput) {
                customTagInput.value = postData.custom_tag || '';
            }

            imageInputs.forEach(input => {
                input.value = '';
            });
            clearImagePreviews();

        } else {
            modalTitle.textContent = 'Створення публікації';
            submitPostButton.textContent = 'Публікація';
            postForm.action = '/posts/';
            postIdInput.value = '';
            postForm.reset();
            clearImagePreviews();

            if (questionInput.value.trim() !== '') {
                modalTextInput.value = questionInput.value.trim();
                questionInput.value = '';
            }
        }
    }

    function closeModal() {
        modal.style.display = 'none';
        deleteModal.style.display = 'none';
        postForm.reset();
        postIdInput.value = '';
        questionInput.value = '';
        clearFormErrors();
        clearImagePreviews();
        const customTagContainer = document.querySelector('.custom-tag-container');
        if (customTagContainer) {
            customTagContainer.remove();
        }
    }

    publishButton.addEventListener('click', function() {
        openModal(false);
    });

    closeButton.addEventListener('click', closeModal);

    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            closeModal();
        }
    });

    document.querySelectorAll('.dots-icon').forEach(icon => {
        icon.addEventListener('click', function(event) {
            event.stopPropagation();
            currentPostId = this.dataset.postId;
            const rect = this.getBoundingClientRect();
            deleteModal.style.display = 'flex';
            deleteModal.style.top = `${rect.bottom + window.scrollY + 5}px`;
            deleteModal.style.left = `${rect.left + window.scrollX - deleteModal.offsetWidth + 20}px`;
            deleteModal.style.position = 'absolute';
        });
    });

    window.addEventListener('click', function(event) {
        if (event.target === deleteModal || (!deleteModal.contains(event.target) && !event.target.classList.contains('dots-icon'))) {
            deleteModal.style.display = 'none';
            currentPostId = null;
        }
    });

    deleteConfirmButton.addEventListener('click', function() {
        if (currentPostId) {
            fetch(`/posts/delete/${currentPostId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    location.reload();
                } else {
                    alert('Помилка видалення публікації: ' + (data.message || 'Невідома помилка.'));
                }
                closeModal();
            })
            .catch(error => {
                alert('Виникла помилка при спробі видалити публікацію. Перевірте консоль розробника.');
                closeModal();
            });
        }
    });

    editPostButton.addEventListener('click', function() {
        if (currentPostId) {
            fetch(`/posts/edit/${currentPostId}/`)
                .then(response => {
                    if (!response.ok) {
                        return response.json().then(errorData => {
                            const error = new Error(`HTTP error! status: ${response.status}`);
                            error.data = errorData;
                            throw error;
                        }).catch(() => {
                            throw new Error(`HTTP error! status: ${response.status}`);
                        });
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.status === 'success') {
                        openModal(true, data);
                        deleteModal.style.display = 'none';
                    } else {
                        alert('Помилка отримання даних для редагування: ' + (data.message || 'Невідома помилка.'));
                        closeModal();
                    }
                })
                .catch(error => {
                    let errorMessage = 'Виникла помилка при спробі отримати дані для редагування публікації.';
                    if (error.response && error.response.status === 403) {
                        errorMessage = 'Ви не маєте права редагувати цей пост.';
                    } else if (error.data && error.data.message) {
                        errorMessage = 'Помилка сервера: ' + error.data.message;
                    } else if (error.message) {
                        errorMessage += ` (${error.message})`;
                    }
                    alert(errorMessage);
                    closeModal();
                });
        }
    });

    postForm.addEventListener('submit', function(event) {
        event.preventDefault();
        clearFormErrors();
        const formData = new FormData(postForm);

        fetch(postForm.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(errorData => {
                    const error = new Error('Server responded with an error status.');
                    error.response = response;
                    error.data = errorData;
                    throw error;
                }).catch(() => {
                    throw new Error(`HTTP error! status: ${response.status}`);
                });
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'success') {
                location.reload();
            } else {
                alert('Помилка збереження публікації: ' + (data.message || 'Невідома помилка.'));
                if (data.errors) {
                    displayFormErrors(data.errors);
                }
            }
        })
        .catch(error => {
            let errorMessage = 'Виникла невідома помилка при спробі зберегти публікацію.';
            if (error.data && error.data.errors) {
                errorMessage = "Помилки при збереженні:\n";
                for (const field in error.data.errors) {
                    errorMessage += `  ${field}: ${error.data.errors[field].join(', ')}\n`;
                }
                displayFormErrors(error.data.errors);
            } else if (error.data && error.data.message) {
                errorMessage = 'Помилка сервера: ' + error.data.message;
            } else if (error.message) {
                errorMessage += ` (${error.message})`;
            }
            alert(errorMessage);
        });
    });

    function displayFormErrors(errors) {
        clearFormErrors();
        for (const fieldName in errors) {
            const errorList = errors[fieldName];
            const fieldElement = document.getElementById(`id_${fieldName}`);
            if (fieldElement) {
                const errorDiv = document.createElement('div');
                errorDiv.className = 'errorlist';
                errorDiv.style.color = 'red';
                errorDiv.style.fontSize = '0.9em';
                errorDiv.style.marginTop = '5px';
                errorDiv.innerHTML = errorList.map(err => `${err}`).join('<br>');
                fieldElement.parentNode.insertBefore(errorDiv, fieldElement.nextSibling);
            } else if (fieldName === 'non_field_errors') {
                const form = document.getElementById('post-form');
                if (form) {
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'errorlist';
                    errorDiv.style.color = 'red';
                    errorDiv.style.fontSize = '0.9em';
                    errorDiv.style.marginBottom = '10px';
                    errorDiv.innerHTML = errorList.map(err => `${err}`).join('<br>');
                    form.prepend(errorDiv);
                }
            }
        }
    }

    const ukrainianTagMap = {
        'vacation': 'Відпочинок',
        'inspiration': 'Натхнення',
        'life': 'Життя',
        'nature': 'Природа',
        'reading': 'Читання',
        'calm': 'Спокій',
        'harmony': 'Гармонія',
        'music': 'Музика',
        'movies': 'Фільми',
        'travel': 'Подорожі',
    };

    function updateTextWithTags() {
        const selectedTags = [];
        const allCheckboxes = document.querySelectorAll('.tag-checkbox-list input[type="checkbox"]');
        allCheckboxes.forEach(cb => {
            if (cb.checked) {
                const tagLabel = ukrainianTagMap[cb.value] || cb.value;
                selectedTags.push(`#${tagLabel}`);
            }
        });
        const currentText = modalTextInput.value.split('#')[0].trim();
        modalTextInput.value = currentText + (selectedTags.length > 0 ? ' ' + selectedTags.join(' ') : '');
    }

    document.querySelectorAll('.tag-checkbox-list input[type="checkbox"]').forEach(checkbox => {
        checkbox.addEventListener('change', updateTextWithTags);
    });

    if (addTagIcon) {
        addTagIcon.addEventListener('click', function() {
            if (document.querySelector('.custom-tag-container')) {
                document.getElementById('id_custom_tag').focus();
                return;
            }

            const customTagContainer = document.createElement('div');
            customTagContainer.style.display = 'inline-flex';
            customTagContainer.style.alignItems = 'center';
            customTagContainer.style.marginRight = '5px';
            customTagContainer.className = 'custom-tag-container';

            const customTagInput = document.createElement('input');
            customTagInput.type = 'text';
            customTagInput.id = 'id_custom_tag';
            customTagInput.name = 'custom_tag';
            customTagInput.placeholder = 'Введіть тег';
            customTagInput.className = 'form-control';
            customTagInput.style.marginRight = '8px';
            customTagInput.style.width = '150px';

            const saveTagButton = document.createElement('button');
            saveTagButton.type = 'button';
            saveTagButton.textContent = 'Зберегти';

            Object.assign(saveTagButton.style, {
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                width: 'auto',
                height: '40px',
                borderRadius: '1234px',
                padding: '10px 16px',
                background: '#543C52',
                color: '#FFFFFF',
                fontFamily: "'GT Walsheim Pro', sans-serif",
                fontWeight: '500',
                fontSize: '14px',
                lineHeight: '20px',
                letterSpacing: '-0.006em',
                border: 'none',
                cursor: 'pointer',
                boxSizing: 'border-box'
            });

            const handleSave = () => {
                const newTagValue = customTagInput.value.trim();
                if (newTagValue) {
                    const existingTags = Array.from(document.querySelectorAll('.tag-checkbox-list input[type="checkbox"]'));
                    if (existingTags.some(cb => cb.value.toLowerCase() === newTagValue.toLowerCase())) {
                        alert('Тег з такою назвою вже існує.');
                        return;
                    }

                    const newIndex = existingTags.length;
                    const newTagDiv = document.createElement('div');
                    newTagDiv.style.display = 'inline-block';
                    newTagDiv.style.marginRight = '5px';

                    const newTagLabel = document.createElement('label');
                    newTagLabel.setAttribute('for', `id_tags_${newIndex}`);

                    const newTagCheckbox = document.createElement('input');
                    newTagCheckbox.type = 'checkbox';
                    newTagCheckbox.name = 'tags';
                    newTagCheckbox.value = newTagValue;
                    newTagCheckbox.id = `id_tags_${newIndex}`;
                    newTagCheckbox.className = 'tag-checkbox-list';
                    newTagCheckbox.checked = true;

                    newTagCheckbox.addEventListener('change', updateTextWithTags);

                    newTagLabel.appendChild(newTagCheckbox);
                    newTagLabel.appendChild(document.createTextNode(` #${newTagValue}`));
                    newTagDiv.appendChild(newTagLabel);

                    tagContainer.insertBefore(newTagDiv, addTagIcon);
                    updateTextWithTags();
                    customTagContainer.remove();
                }
            };

            saveTagButton.addEventListener('click', handleSave);
            customTagInput.addEventListener('keydown', (event) => {
                if (event.key === 'Enter') {
                    event.preventDefault();
                    handleSave();
                }
            });

            customTagContainer.appendChild(customTagInput);
            customTagContainer.appendChild(saveTagButton);
            tagContainer.appendChild(customTagContainer);
            customTagInput.focus();
        });
    }

    const linkIcon = document.getElementById('focus-link-icon');
    const linkInput = document.getElementById('id_article_link');

    if (linkIcon && linkInput) {
        linkIcon.addEventListener('click', function() {
            linkInput.focus();
        });
    }
});