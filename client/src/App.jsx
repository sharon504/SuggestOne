import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import Component from './Home';
import SearchResults from './SearchResult';
import Navbar from './Navbar';
import { AuthProvider } from './AuthContext';
function App() {
  return (
      <AuthProvider>
      <Router>
      <Navbar/>
      
        <Routes>
        <Route path="/" element={<Component />}/>
        <Route path="/search" element={<SearchResults />} />
        </Routes>
      </Router>
      </AuthProvider>
      
  
  );
}

export default App;
