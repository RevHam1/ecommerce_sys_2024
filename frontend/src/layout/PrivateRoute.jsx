/* eslint-disable react/prop-types */
import { Navigate } from 'react-router-dom';
import { useAuthStore } from '../store/auth';

const PrivateRoute = ({ children }) => {
    const loggedIn = useAuthStore((state) => state.isLoggedIn)();

    // Conditionally render the children if the user is authenticated.
    // If the user is not authenticated, redirect them to the login page.
    return loggedIn ? <>{children}</> : <Navigate to="/login" />;
};

export default PrivateRoute;
