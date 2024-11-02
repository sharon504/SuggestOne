import React, { useState, useEffect,createContext,useContext } from 'react';
import { motion } from 'framer-motion';
import { Search, TrendingUp, Clock } from 'lucide-react';
import axios from 'axios'; // Commented out since you don't have the API key
import { useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';
import { v4 as uuid } from 'uuid';

const Searched = ({ heading, description }) => (
  <motion.div
    className="flex flex-col justify-between border border-purple-500 space-y-4 mt-6 z-50 w-64 mx-auto p-4 bg-gray-900 rounded-lg shadow-lg transition-all duration-300 ease-in-out hover:scale-105"
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    exit={{ opacity: 0, y: 20 }}
    transition={{ duration: 0.5 }}
  >
    <h2 className="text-2xl font-semibold text-left text-purple-300">{heading}</h2>
    <p className="text-left text-gray-400 mb-5">{description}</p>
    <button className="w-full bg-purple-700 mt-auto text-white hover:bg-purple-600 py-2 px-4 rounded transition-colors duration-300">
      More Info
    </button>
  </motion.div>
);

export default function Component() {
  const [searchTerm, setSearchTerm] = useState("");
  const [isSearching, setIsSearching] = useState(false);
  const apiKey=useAuth();
  
  console.log(apiKey.api);
  
  const navigate = useNavigate();
 
  const handleSearch = async (e) => {
    e.preventDefault();
    setIsSearching(true); // Set the loading state
    const userId="";
    // Simulated API response
    const data = { query: searchTerm ,key:userId}
    await axios.post('http://localhost:5000/', { // http://localhost:2000/auth/regenkey
      headers: {
        'Content-Type': 'application/json',
        'X-USER-KEY': `${apiKey.api}`
      }, data
    })
    .then(response => {
      console.log(response.data);
      navigate(
       '/search',
        {state: { message: response.data} }
      );
    })
    .catch(error => {
      console.error('Error fetching data:', error);
    })
    .finally(() => {
      setIsSearching(false);
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black text-white font-sans">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <main className="pt-16">
          <motion.div
            className="max-w-3xl mx-auto py-6 sm:px-6 lg:px-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <motion.h1 
              className="text-4xl md:text-5xl w-auto font-bold mb-8 text-center bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-600"
              initial={{ scale: 0.9 }}
              animate={{ scale: 1 }}
              transition={{ duration: 0.5, type: "spring" }}
            >
              Welcome to Re-Wiki
            </motion.h1>
            <motion.form 
              onSubmit={handleSearch}
              className="mb-12"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
            >
              <div className="flex items-center">
                <input
                  type="text"
                  placeholder="Search..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full bg-gray-800 text-white border border-purple-500 focus:border-pink-500 rounded-l px-4 py-2 outline-none transition-colors duration-300"
                  aria-label="Search"
                />
                <button 
                  type="submit"
                  className="ml-2 bg-purple-600 hover:bg-purple-700 text-white py-2 px-4 rounded-r transition-colors duration-300 flex items-center justify-center"
                  disabled={isSearching}
                >
                  {isSearching ? (
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                    >
                      <Clock className="h-5 w-5" />
                    </motion.div>
                  ) : (
                    <Search className="h-5 w-5" />
                  )}
                </button>
              </div>
            </motion.form>
          </motion.div>
        </main>
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <h2 className='font-semibold text-3xl mb-6 flex items-center'>
            <TrendingUp className="mr-2 text-pink-500" />
            Most Searched
          </h2>
          <div className='flex flex-col md:flex-nowrap md:flex-row gap-4 justify-between'>
            <Searched 
              heading="Quantum Computing" 
              description="Explore the fascinating world of quantum mechanics."
            />
            <Searched
              heading="Artificial Intelligence" 
              description="Discover the latest advancements in AI, machine learning, and neural networks."
            />
            <Searched 
              heading="Renewable Energy" 
              description="Learn about sustainable energy sources and their impact on global climate change."
            />
            <Searched 
              heading="Renewable Energy" 
              description="Learn about sustainable energy sources and their impact on global climate change."
            />
          </div>
        </motion.div>
      </div>
    </div>
  );
}
