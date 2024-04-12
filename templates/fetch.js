// URL для запиту до сервера
const requestURL = 'http://127.0.0.1:8000/users/note/get/';

// Функція для відправки запитів на сервер
function sendRequest(method, url, body = null) {
    const headers = {
        'Content-Type': 'application/json'
    };

    // Перевіряємо, чи метод запиту - GET
    if (method === 'GET') {
        // Якщо так, не передаємо тіло
        return fetch(url, {
            method: method,
            headers: headers
        }).then(response => {
            if (response.ok) {
                return response.json();
            }
            return response.json().then(error => {
                const e = new Error('Помилка');
                e.data = error;
                throw e;
            });
        });
    } else {
        // Для інших методів, як POST, PUT, PATCH, DELETE, використовуємо JSON.stringify(body)
        return fetch(url, {
            method: method,
            body: JSON.stringify(body),
            headers: headers
        }).then(response => {
            if (response.ok) {
                return response.json();
            }
            return response.json().then(error => {
                const e = new Error('Помилка');
                e.data = error;
                throw e;
            });
        });
    }
}

// Відправити запит методом GET до сервера
sendRequest('GET', requestURL)
    .then(data => {
        // Вивести усі отримані об'єкти у консоль
        console.log(data);

        // Перевірка, чи є дані та чи містить відповідь поле "title"
        if (data && data.length > 0 && data[0].title) {
            // Отримання першого об'єкта з масиву та вставка його заголовку на сторінку
            const noteTitle = data[0].title;
            const noteElement = document.createElement('p');
            noteElement.textContent = `Title: ${noteTitle}`;
            document.querySelector('.note_one').appendChild(noteElement);

            // Отримання ID автора
            const authorId = parseInt(data[0].author_id);
            console.log('ID користувача:', authorId);
            if (Number.isInteger(authorId)) {
                // Все гаразд, authorId є цілим числом
                sendRequest('GET', `http://127.0.0.1:8000/users/user/find/${authorId}`)
                    .then(userData => {
                        // Виведення імені користувача у консоль
                        console.log('Ім\'я користувача:', userData.username);

                        // Вставка імені користувача на HTML-сторінку
                        const authorNameElement = document.createElement('p');
                        authorNameElement.textContent = `Author: ${userData.username}`;
                        document.querySelector('.note_one').appendChild(authorNameElement);
                    })
                    .catch(err => console.error('Помилка під час отримання інформації про користувача:', err));
            }
        }
    })
    .catch(err => console.error('Помилка:', err));
