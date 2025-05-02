import React, { useState } from 'react';

const ChatWindow = () => {
  const [messages, setMessages] = useState([
    { from: 'bot', text: 'Hello, I am your Bereavement Assistant. How can I help you today?' }
  ]);
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (!input.trim()) return;

    setMessages([...messages, { from: 'user', text: input }]);
    setInput('');
    // Simulate bot response
    setTimeout(() => {
      setMessages(prev => [
        ...prev,
        { from: 'user', text: input },
        { from: 'bot', text: `You said: "${input}"` }
      ]);
    }, 500);
  };

  return (
    <div className="flex flex-col h-full">
      <h1 className="text-2xl font-bold mb-4 text-center">Bereavement Assistant</h1>

      <div className="flex-1 overflow-y-auto space-y-2 mb-4 px-2">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`max-w-[75%] p-2 rounded-xl ${
              msg.from === 'user'
                ? 'bg-blue-600 text-white self-end ml-auto'
                : 'bg-gray-200 text-black self-start'
            }`}
          >
            {msg.text}
          </div>
        ))}
      </div>

      <div className="flex gap-2">
        <input
          className="flex-1 border rounded-lg px-4 py-2"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Type your message..."
        />
        <button
          className="bg-blue-600 text-white px-4 py-2 rounded-lg"
          onClick={handleSend}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatWindow;
