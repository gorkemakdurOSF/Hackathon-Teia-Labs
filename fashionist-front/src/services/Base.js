import axios from 'axios';

const client = axios.create({
    baseURL: 'http://192.168.1.121:8080/',
    timeout: 1000,
});

export default client;
