import axios from 'axios';
export const api = axios.create({ 
    baseURL: 'http://localhost:8000',
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
});
export function setAuth(token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}
