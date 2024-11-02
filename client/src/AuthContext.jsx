import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

// Create a context
const AuthContext = createContext();

// Provider component
export const AuthProvider = ({ children }) => {
  const [apiKey, setApiKey] = useState({ api: null, userId: null }); // Initial state is null

  // Fetch the API key once when the component mounts
  useEffect(() => {
    const fetchApiKey = async () => {
      try {
        const response = await axios.get("http://localhost:5000/auth/key", {
          headers: {
            'Content-Type': 'application/json',
          }
        });
        // Update state properly
        setApiKey({
          api: response.data.key,
          userId: response.data.userId // Assuming you also get userId from the response
        });

        console.log(response.data.key); // Log the fetched API key
      } catch (error) {
        console.error("Error fetching the API key:", error);
      }
    };

    fetchApiKey();
  }, []); // Empty dependency array to run only on mount

  return (
    <AuthContext.Provider value={apiKey}>
      {children}
    </AuthContext.Provider>
  );
};

// Hook to use the auth context
export const useAuth = () => useContext(AuthContext);
