import React, { useEffect, useRef } from 'react';
import { createDirectLine, renderWebChat } from 'botframework-webchat';

const BotChat = () => {
  const webchatRef = useRef(null);

  useEffect(() => {
    const directLine = createDirectLine({
      token: 'YOUR_DIRECT_LINE_TOKEN', // Replace this with your actual token
    });

    renderWebChat(
      {
        directLine,
        userID: 'user-' + Math.random().toString(36).substr(2, 9),
        username: 'User',
        locale: 'en-US',
        styleOptions: {
          bubbleBackground: '#e0e0e0',
          bubbleFromUserBackground: '#0078d4',
          bubbleFromUserTextColor: '#fff',
          rootHeight: '100%',
        },
      },
      webchatRef.current
    );
  }, []);

  return (
    <div className="h-screen p-4">
      <h1 className="text-xl font-bold mb-2">Bereavement Assistant</h1>
      <div ref={webchatRef} className="h-[80vh]" />
    </div>
  );
};

export default BotChat;
