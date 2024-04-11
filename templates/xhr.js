const requestURL = 'http://127.0.0.1:8000/users/note/get/'

const xhr = new XMLHttpRequest()

xhr.open('GET', requestURL)

xhr.onload = () => {
    console.log(JSON.parse(xhr.response))
}

xhr.send()