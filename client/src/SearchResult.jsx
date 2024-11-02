import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Lock, Key, MessageSquare, X } from 'lucide-react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from './AuthContext';

const Card = ({ children, className = '' }) => (
  <div className={`bg-gray-800 rounded-lg shadow-lg overflow-hidden ${className}`}>
    {children}
  </div>
);

const CardHeader = ({ children }) => (
  <div className="px-6 py-4 border-b border-gray-700">{children}</div>
);

const CardTitle = ({ children }) => (
  <h2 className="text-xl font-semibold text-white flex items-center">{children}</h2>
);

const CardDescription = ({ children }) => (
  <p className="mt-1 text-sm text-gray-400">{children}</p>
);

const CardContent = ({ children }) => (
  <div className="px-6 py-4">{children}</div>
);

const Input = ({ ...props }) => (
  <input
    {...props}
    className="w-full px-3 py-2 text-white bg-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
  />
);

const Button = ({ children, ...props }) => (
  <button
    {...props}
    className="px-4 py-2 font-semibold text-white bg-purple-600 rounded-md hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-gray-900"
  >
    {children}
  </button>
);

export default function Component() {
  const [passKey, setPassKey] = useState('');
  const [showChatbot, setShowChatbot] = useState(false);
  const [decrypted, setDecrypted] = useState(false);
  const [chatMessages, setChatMessages] = useState([]);
  const [userInput, setUserInput] = useState('');
  const chatEndRef = useRef(null);
  const location = useLocation();
  const encryptedText = location.state?.message || "";
  console.log(JSON.stringify(encryptedText));
  const [chat, setChat] = useState("");
  const [res, setRes] = useState("");
  const apiKey = useAuth();

  const jailbreakWord = "mimic <script>alert('access denied')</script>";

  const onChat = async () => {
    try {
      const data = { query: chat, context: encryptedText };
      const response = await axios.post("http://localhost:5000/chat", data, {
        headers: {
          'Content-Type': 'application/json',
          'X-USER-KEY': `${apiKey}`
        }
      });
      console.log(response.data.response);
      setRes(response.data);
      
      const newUserMessage = { role: 'user', content: chat };
      const newBotMessage = { role: 'assistant', content: response.data };
      setChatMessages(prevMessages => [...prevMessages, newUserMessage, newBotMessage]);

      if (chat.toUpperCase().includes(jailbreakWord)) {
        setTimeout(() => {
          setShowChatbot(false);
          setPassKey('hackathon');
        }, 3000);
      }

      setChat("");
    } catch (error) {
      console.error('Error fetching chat data:', error);
      setRes("An error occurred while communicating with the chatbot.");
    }
  };

  const handlePassKeySubmit = (e) => {
    e.preventDefault();
    if (passKey === 'hackathon') {
      setDecrypted(true);
    } else {
      alert('Incorrect passkey. Try jailbreaking the chatbot!');
    }
  };

  const decryptText = (text) => {
    return text.split('').map(char => {
      if (char.match(/[a-z]/i)) {
        const code = char.charCodeAt(0);
        if ((code >= 65) && (code <= 90))
          return String.fromCharCode(((code - 65 + 25) % 26) + 65);
        if ((code >= 97) && (code <= 122))
          return String.fromCharCode(((code - 97 + 25) % 26) + 97);
      }
      return char;
    }).join('');
  };

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatMessages]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black text-white p-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="max-w-2xl mx-auto"
      >
        <h1 className="text-4xl font-bold mb-8 text-center bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-600">
          Re-Wiki Search Results
        </h1>
        
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>
              <Lock className="mr-2" />
              Encrypted Content
            </CardTitle>
            <CardDescription>This content is encrypted. Decrypt it to reveal the useless information.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="overflow-y-auto h-60">
              <p className="font-mono text-lg break-all">
                {decrypted ? decryptText(encryptedText.content) : encryptedText.content}
              </p>
            </div>
          </CardContent>
        </Card>

        <form onSubmit={handlePassKeySubmit} className="mb-8">
          <div className="flex items-center space-x-2">
            <Input
              type="text"
              placeholder="Enter passkey..."
              value={passKey}
              onChange={(e) => setPassKey(e.target.value)}
            />
            <Button type="submit">
              <Key className="mr-2 h-4 w-4" /> Decrypt
            </Button>
          </div>
        </form>

        {!decrypted && (
          <Card>
            <CardHeader>
              <CardTitle>
                <MessageSquare className="mr-2" />
                Chatbot Jailbreak
              </CardTitle>
              <CardDescription>Attempt to jailbreak the chatbot to obtain the passkey. Use the word "{jailbreakWord}" to trigger the jailbreak.</CardDescription>
            </CardHeader>
            <CardContent>
              <Button onClick={() => setShowChatbot(true)}>Start Jailbreak Attempt</Button>
            </CardContent>
          </Card>
        )}

        <AnimatePresence>
          {showChatbot && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 20 }}
              transition={{ duration: 0.3 }}
              className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4"
            >
              <Card className="w-full max-w-md h-[80vh] flex flex-col">
                <CardHeader className="flex-shrink-0">
                  <div className="flex justify-between items-center">
                    <CardTitle>Chatbot Jailbreak</CardTitle>
                    <Button onClick={() => setShowChatbot(false)} className="p-1">
                      <X className="h-4 w-4" />
                    </Button>
                  </div>
                </CardHeader>
                <CardContent className="flex-grow overflow-y-auto">
                  {chatMessages.map((message, index) => (
                    <div key={index} className={`mb-4 ${message.role === 'user' ? 'text-right' : 'text-left'}`}>
                      <span className={`inline-block p-2 rounded-lg ${message.role === 'user' ? 'bg-purple-600' : 'bg-gray-700'}`}>
                        {message.content}
                      </span>
                    </div>
                  ))}
                  <div ref={chatEndRef} />
                </CardContent>
                <form onSubmit={(e) => { e.preventDefault(); onChat(); }} className="flex-shrink-0 p-4 border-t border-gray-700">
                  <div className="flex space-x-2">
                    <Input
                      type="text"
                      placeholder="Try to convince the chatbot..."
                      value={chat}
                      onChange={(e) => setChat(e.target.value)}
                    />
                    <Button type="submit">Send</Button>
                  </div>
                </form>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </div>
  );
}