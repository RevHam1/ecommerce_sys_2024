import { mountStoreDevtool } from 'simple-zustand-devtools';
import { create } from 'zustand';

// Create a Zustand store named 'useAuthStore' using the 'create' function.
const useAuthStore = create((set, get) => ({
    // Define 'allUserData' & 'loading' state variables and initialize them to null & false.
    allUserData: null,
    loading: false,

    // Define 'user' function that returns an object with user-related data.
    user: () => ({
        user_id: get().allUserData?.user_id || null,
        username: get().allUserData?.username || null,
        // vendor_id: get().allUserData?.vendor_id || null,
    }),
    
    // Define 'setUser' & 'setLoading' functions; setting the state for'allUserData' & 'loading'.
    setUser: (user) => set({ allUserData: user }),
    setLoading: (loading) => set({ loading }),
    // Define 'isLoggedIn' function that checks if 'allUserData' is not null.
    isLoggedIn: () => get().allUserData !== null,
    // setLoggedIn: () => get().allUserData !== null,
}))

// Conditionally attach the DevTools only in a development environment.
if(import.meta.env.DEV) {
    mountStoreDevtool('Store', useAuthStore)
}

// Export the 'useAuthStore' for use in other parts of the application.
export { useAuthStore };

