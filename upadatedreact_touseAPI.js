fetch(`http://localhost:8000/conversations/${selectedId}/messages`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ text: input }),
})
  .then(res => res.json())
  .then(data => setMessages(data));
