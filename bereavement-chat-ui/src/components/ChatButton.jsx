import React, { useState, useRef, useEffect } from 'react';
import ChatWindow from './ChatWindow';

const ChatButton = () => {
  const [isChatOpen, setIsChatOpen] = useState(false);
  const chatContainerRef = useRef(null);

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  // Auto-scroll to bottom when chat opens or content changes
  useEffect(() => {
    if (isChatOpen && chatContainerRef.current) {
      const container = chatContainerRef.current;
      container.scrollTop = container.scrollHeight;
    }
  }, [isChatOpen]);

  return (
    <div>
      {/* Floating button with dynamic padding */}
      <button
        className={`fixed bottom-4 right-4 bg-blue-600 text-white p-4 rounded-full shadow-lg hover:bg-blue-700 transition-all z-50 ${isChatOpen ? 'pt-12' : ''}`}
        onClick={toggleChat}
      >
        
        <img src="src\helping_6834048.png" className="w-10 h-10"/>
      </button>

      {/* Chat Window */}
      {isChatOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-end items-center z-50">
          <div className="relative bg-white w-full sm:max-w-md md:w-1/3 h-full rounded-2xl shadow-lg p-6 flex flex-col">
            <button
              className="absolute top-2 right-2 bg-red-600 text-white rounded-full p-2"
              onClick={toggleChat}
            >
              X
            </button>
            <div 
              ref={chatContainerRef}
              className="flex-1 overflow-y-auto pr-2"
            >
              <ChatWindow />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatButton;
