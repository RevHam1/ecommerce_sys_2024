import axios from 'axios';

const apiInstance = axios.create({
    // baseURL: API_BASE_URL, // http://127.0.0.1:8000/api/v1/
    baseURL: 'http://127.0.0.1:8000/api/v1/',
    timeout: 5000, // timeout after 5 seconds
    
    // Define headers to be included in request made. This is common to specify content type & accepted response type.
    headers: {
        'Content-Type': 'application/json', // The request will be sending data in JSON format.
        Accept: 'application/json', // The request expects a response in JSON format.
    },
});

export default apiInstance;
