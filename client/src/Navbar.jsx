import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Menu, X, Home, User, Mail, Settings, Book } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

export default function EnhancedNavbar() {
  const [isOpen, setIsOpen] = useState(false)
  const navigate=useNavigate();
  const navItems = [
    { icon: Home, label: 'Home', path: '/' },            // Navigates to Home
    { icon: Book, label: 'Wiki', path: '/' },        // Navigates to Wiki
    { icon: User, label: 'Profile', path: '/' },  // Navigates to Profile
    { icon: Mail, label: 'Contact', path: '/' },  // Navigates to Contact
    { icon: Settings, label: 'Settings', path: '/' }, 
  ];

  return (
    <nav className="bg-gray-900 text-white p-4">
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        <motion.div
          className="text-2xl font-bold"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
        >
          Re-Wiki
        </motion.div>
        <div className="hidden md:flex space-x-4">
          {navItems.map((item, index) => (
            <motion.a
              key={item.label}
              onClick={() =>{navigate(item.path);setIsOpen(false);}}
              className="flex items-center px-3 py-2 rounded-md text-sm font-medium hover:bg-purple-700 transition-colors duration-300"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <item.icon className="mr-2" size={18} />
              {item.label}
            </motion.a>
          ))}
        </div>
        <div className="md:hidden">
          <motion.button
            onClick={() => setIsOpen(!isOpen)}
            className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-white focus:outline-none"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            {isOpen ? <X size={24} /> : <Menu size={24} />}
          </motion.button>
        </div>
      </div>
      <AnimatePresence>
        {isOpen && (
          <motion.div
            className="md:hidden"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
          >
            <div className="px-2 pt-2 pb-3 space-y-1">
              {navItems.map((item, index) => (
                <motion.a
                  key={item.label}
                  href="#"
                  className="flex items-center px-3 py-2 rounded-md text-base font-medium hover:bg-purple-700 transition-colors duration-300"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.1 }}
                >
                  <item.icon className="mr-2" size={18} />
                  {item.label}
                </motion.a>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  )
}