/* eslint-disable react/prop-types */
import { useEffect, useState } from 'react';
import { setUser } from '../utils/auth';

const MainWrapper = ({ children }) => {
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const handler = async () => {
            setLoading(true);                  
            await setUser(); // Perform an asynchronous user authentication action           
            setLoading(false);
        };
              
        handler(); // Call 'handler' function immediately after the component is mounted
    }, []);
    
    return <>{loading ? null : children}</>; // Render content conditionally based on the 'loading' state
};

export default MainWrapper;
