
import React, { useState } from 'react';
import MessageList from './MessageList';
import UserInput from './UserInput';
import ConversationHistory from './ConversationHistory';

// Initial conversations for demonstration
const initialConversations = [
  {
    id: 1,
    messages: [
      { id: 1, sender: 'user', text: 'Hello!' },
      { id: 2, sender: 'ai', text: 'Hi, how can I help you?' },
    ],
  },
  {
    id: 2,
    messages: [
      { id: 1, sender: 'user', text: 'What is React?' },
      { id: 2, sender: 'ai', text: 'React is a JavaScript library for building UIs.' },
    ],
  },
];

const ChatWindow = () => {
  // State for all conversations
  const [conversations, setConversations] = useState(initialConversations);
  // State for selected conversation
  const [selectedId, setSelectedId] = useState(conversations[0].id);

  // Get the currently selected conversation
  const selectedConversation = conversations.find(conv => conv.id === selectedId);

  // Add a new message to the selected conversation
  const handleSendMessage = (text) => {
    setConversations(conversations.map(conv =>
      conv.id === selectedId
        ? {
            ...conv,
            messages: [
              ...conv.messages,
              { id: conv.messages.length + 1, sender: 'user', text },
            ],
          }
        : conv
    ));
  };

  // Handle selecting a conversation
  const handleSelectConversation = (id) => {
    setSelectedId(id);
  };

  return (
    <div style={{ display: 'flex', width: 600, border: '1px solid #ccc', borderRadius: 8 }}>
      <ConversationHistory
        conversations={conversations}
        onSelect={handleSelectConversation}
        selectedId={selectedId}
      />
      <div style={{ flex: 1, padding: 16 }}>
        <h2>Chat</h2>
        <MessageList messages={selectedConversation.messages} />
        <UserInput onSend={handleSendMessage} />
      </div>
    </div>
  );
};

export default ChatWindow;
