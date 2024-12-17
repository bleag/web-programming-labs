function registration() {
    const user = {

        username: document.getElementById('username').value,
        password: document.getElementById('password').value,
    }

    const url =`/rgz/rest-api/users/registration`;
    const method ='POST';

    fetch(url, {
        method: method,
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(user)
    })
    .then(function(resp) {
        if(resp.ok) {
            alert("Вы успешно зарегестрированы, теперь можете войти");
        }
        return resp.json();
    })
    .then(function(errors) {
        if(errors.username)
            document.getElementById('username-error').innerText = errors.username;
        if(errors.password)
            document.getElementById('password-error').innerText = errors.password;
        if(errors.exception)
            document.getElementById('username-error').innerText= errors.exception;
    });
}


function login() {
    const user = {
        username: document.getElementById('username').value,
        password: document.getElementById('password').value,
    };

    const url = `/rgz/rest-api/users/login`;
    const method = 'POST';

    fetch(url, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(user),
    })
    .then(function(resp) {
        if (resp.ok) {
            window.location.href = '/main'; 
        } else {
            return resp.json();
        }
    })
    .then(function(errors) {
        if (errors) {
            if (errors.username)
                document.getElementById('username-error').innerText = errors.username;
            if (errors.password)
                document.getElementById('password-error').innerText = errors.password;
            if (errors.exception)
                document.getElementById('username-error').innerText = errors.exception;
        }
    });
}

function openModal() {
    const modal = document.getElementById("profileModal");
    modal.style.display = "flex"; // Показываем модальное окно
}


function closeModal() {
    const modal = document.getElementById("profileModal");
    modal.style.display = "none"; // Скрываем модальное окно
}


function submitProfile() {
    const formData = new FormData();
    formData.append("name", document.getElementById("name").value);
    formData.append("age", document.getElementById("age").value);
    formData.append("gender", document.getElementById("gender").value);
    formData.append("looking_for", document.getElementById("looking_for").value);
    formData.append("about", document.getElementById("about").value || "");
    const photoInput = document.getElementById("photo");
    if (photoInput.files[0]) {
        formData.append("photo", photoInput.files[0]);
    }

    fetch("/rgz/rest-api/profiles", {
        method: "POST",
        body: formData,
    })
    .then((response) => {
        if (response.ok) {
            alert("Анкета успешно заполнена!");
            closeModal(); // Закрываем модальное окно
            window.location.href = "/main"; // Возвращаемся на главную страницу
        } else {
            return response.json();
        }
    })
    .then((errors) => {
        if (errors) {
            alert("Произошла ошибка: " + (errors.message || "Неизвестная ошибка"));
        }
    });
}



function openEditProfileModal() {
    const modal = document.getElementById("editProfileModal");
    modal.style.display = "flex"; // Показываем модальное окно
}

function closeEditProfileModal() {
    const modal = document.getElementById("editProfileModal");
    modal.style.display = "none"; // Скрываем модальное окно
}

function submitEditProfile() {
    const formData = new FormData();
    formData.append("name", document.getElementById("edit-name").value);
    formData.append("age", document.getElementById("edit-age").value);
    formData.append("gender", document.getElementById("edit-gender").value);
    formData.append("looking_for", document.getElementById("edit-looking_for").value);
    formData.append("about", document.getElementById("edit-about").value || "");
    const photoInput = document.getElementById("edit-photo");
    if (photoInput.files[0]) {
        formData.append("photo", photoInput.files[0]);
    }

    const isHidden = document.getElementById("edit-is_hidden").checked;
    formData.append("is_hidden", isHidden);

    fetch("/rgz/rest-api/profiles", {
        method: "PUT",
        body: formData,
    })
    .then((response) => {
        if (response.ok) {
            alert("Анкета успешно обновлена!");
            closeEditProfileModal(); // Закрываем модальное окно
            window.location.reload(); // Перезагружаем страницу для отображения обновленных данных
        } else {
            return response.json();
        }
    })
    .then((errors) => {
        if (errors) {
            alert("Произошла ошибка: " + (errors.message || "Неизвестная ошибка"));
        }
    });
}


function deleteAccount() {
    if (confirm('Вы уверены, что хотите удалить свой аккаунт? Это действие необратимо.')) {
        fetch('/rgz/rest-api/profiles/delete', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({})
        })
        .then(response => {
            if (response.ok) {
                alert('Ваш аккаунт был успешно удален.');
                window.location.href = '/rgz'; 
            } else {
                return response.json().then(data => { throw new Error(data.message); });
            }
        })
        .catch(error => {
            alert('Ошибка при удалении аккаунта: ' + error.message);
        });
    }
}



function logout() {
    if (confirm('Вы уверены, что хотите выйти из аккаунта?')) {
        window.location.href = '/rgz/rest-api/logout';
    }
}


let offset = 0;  // Смещение для пагинации
const limit = 3; // Количество анкет на одной странице

function searchProfiles(reset = true) {
    if (reset) offset = 0;  // Сброс пагинации при новом поиске

    const name = document.getElementById('search-name').value.trim();
    const age = document.getElementById('search-age').value.trim();

    const params = new URLSearchParams();
    if (name) params.append('name', name);
    if (age) params.append('age', age);
    params.append('offset', offset);

    fetch(`/rgz/rest-api/search?${params.toString()}`)
        .then(response => response.json())
        .then(data => {
            if (reset) {
                document.getElementById('search-results').innerHTML = ''; // Очищаем старые результаты
            }

            if (data.length > 0) {
                data.forEach(profile => {
                    document.getElementById('search-results').innerHTML += `
                        <div class="profile-card">
                            <p><strong>Имя:</strong> ${profile.name}</p>
                            <p><strong>Возраст:</strong> ${profile.age}</p>
                            <p><strong>Пол:</strong> ${profile.gender}</p>
                            <p><strong>О себе:</strong> ${profile.about || 'Не указано'}</p>
                            ${profile.photo_path ? `<img src="/static/${profile.photo_path}" alt="Фото">` : ''}
                        </div>
                    `;
                });
                offset += limit; // Увеличиваем смещение
                document.getElementById('load-more-btn').style.display = 'block'; // Показать кнопку "Следующие"
            } else if (reset) {
                document.getElementById('search-results').innerHTML = '<p>Анкеты не найдены</p>';
                document.getElementById('load-more-btn').style.display = 'none';
            } else {
                alert('Больше анкет не найдено');
                document.getElementById('load-more-btn').style.display = 'none';
            }
        })
        .catch(error => console.error('Ошибка:', error));
}

function loadMoreProfiles() {
    searchProfiles(false);
}