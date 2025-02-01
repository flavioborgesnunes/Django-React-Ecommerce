import axios from 'axios'

const apiInstance = axios.create({
    baseURL: 'http://http://127.0.0.1:8000/api/v1/',
    timeout: 5000,
    headers: {
        'content-type': 'application/json',
        Accept: 'application/json',
    }
})

export default apiInstance