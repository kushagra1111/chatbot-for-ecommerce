import React, { useState } from 'react';

const UserInput = ({ onSend }) => {
  // State for the input field
  const [input, setInput] = useState('');

  // Handle form submission
  const handleSend = (e) => {
    e.preventDefault();
    if (input.trim() === '') return; // Prevent empty messages
    onSend(input); // Call the function passed from ChatWindow
    setInput(''); // Clear the input field
  };

  return (
    <form onSubmit={handleSend} style={{ display: 'flex', gap: 8 }}>
      <input
        type="text"
        value={input}
        onChange={e => setInput(e.target.value)}
        placeholder="Type your message..."
        style={{ flex: 1, padding: 8, borderRadius: 4, border: '1px solid #ccc' }}
      />
      <button type="submit" style={{ padding: '8px 16px' }}>Send</button>
    </form>
  );
};

export default UserInput;