import Cookies from 'js-cookie';
import jwt_decode from 'jwt-decode';
import Swal from 'sweetalert2';

import { useAuthStore } from '../store/auth';
import axios from './axios';

// Configuring global toast notifications using Swal.mixin
const Toast = Swal.mixin({
    toast: true,
    position: 'top',
    showConfirmButton: false,
    timer: 1500,
    timerProgressBar: true,
});

// Function to handle user login
export const login = async (email, password) => {
    try {
        const { data, status } = await axios.post('user/token/', {
            email,
            password,
        });

        if (status === 200) {
            setAuthUser(data.access, data.refresh);

            Toast.fire({
                icon: 'success',
                title: 'Signed in successfully'
            });
        }

        return { data, error: null };
    } catch (error) {
        return {
            data: null,
            error: error.response.data?.detail || 'Something went wrong',
        };
    }
};

// Function to handle user registration
export const register = async (full_name, email, phone, password, password2) => {
    try {
        const { data } = await axios.post('user/register/', {
            full_name,
            email,
            phone,
            password,
            password2,
        });

        await login(email, password); // Logging in the newly registered user 

        // Displaying a success toast notification
        Toast.fire({
            icon: 'success',
            title: 'Signed Up Successfully'
        });

        return { data, error: null };
    } catch (error) {
        return {
            data: null,
            error: error.response.data || 'Something went wrong',
        };
    }
};

// Function to handle user logout
export const logout = () => {
    Cookies.remove('access_token');
    Cookies.remove('refresh_token');
    useAuthStore.getState().setUser(null);

    // Displaying a success toast notification
    Toast.fire({
        icon: 'success',
        title: 'You have been logged out.'
    });
};

// Function to set the authenticated user on page load
export const setUser = async () => {
    const accessToken = Cookies.get('access_token');
    const refreshToken = Cookies.get('refresh_token');

    if (!accessToken || !refreshToken) {
        return;
    }

    // If access token is expired, refresh it; otherwise, set the authenticated user
    if (isAccessTokenExpired(accessToken)) {
        const response = await getRefreshToken(refreshToken);
        setAuthUser(response.access, response.refresh);
    } else {
        setAuthUser(accessToken, refreshToken);
    }
};

// Function to set the authenticated user and update user state
export const setAuthUser = (access_token, refresh_token) => {
    Cookies.set('access_token', access_token, {
        expires: 1,  // Access token expires in 1 day
        secure: true,
    });

    Cookies.set('refresh_token', refresh_token, {
        expires: 7, 
        secure: true,
    });

    const user = jwt_decode(access_token) ?? null;

    // If user update user state; otherwise, set loading state to false
    if (user) {
        useAuthStore.getState().setUser(user);
    }
    useAuthStore.getState().setLoading(false);
};

// Function to refresh the access token using the refresh token
export const getRefreshToken = async () => {
    const refresh_token = Cookies.get('refresh_token');
    const response = await axios.post('user/token/refresh/', {
        refresh: refresh_token,
    });

    return response.data;
};

// Function to check if the access token is expired
export const isAccessTokenExpired = (accessToken) => {
    try {
        const decodedToken = jwt_decode(accessToken);
        return decodedToken.exp < Date.now() / 1000;
    } catch (error) {
        console.log(error);
        return true;
    }
};
