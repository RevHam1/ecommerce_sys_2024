import axios from 'axios';
import Cookies from 'js-cookie';
import { getRefreshToken, isAccessTokenExpired, setAuthUser } from './auth'; // Import authentication-related functions
import { API_BASE_URL } from './constants';

// Define a custom Axios instance creator function
const useAxios = () => {
    const accessToken = Cookies.get('access_token');
    const refreshToken = Cookies.get('refresh_token');

    const axiosInstance = axios.create({
        baseURL: API_BASE_URL,
        headers: { Authorization: `Bearer ${accessToken}` },
    });

    // Add an interceptor to the Axios instance
    axiosInstance.interceptors.request.use(async (req) => {
        if (!isAccessTokenExpired(accessToken)) {
            return req; // If not expired, return the original request
        }

        // If the access token is expired, refresh it
        const response = await getRefreshToken(refreshToken);
        // Update the application with the new access and refresh tokens
        setAuthUser(response.access, response.refresh);
        // Update the request's 'Authorization' header with the new access token
        req.headers.Authorization = `Bearer ${response.data.access}`;
        return req; // Return the updated request
    });

    return axiosInstance; // Return the custom Axios instance
};

export default useAxios; // Export the custom Axios instance creator function
