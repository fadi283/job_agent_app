import React, { useState } from 'react';
import axios from 'axios';
import { Send, Bot, User } from 'lucide-react';

const AgentChat = () => {
  const [messages, setMessages] = useState([
    { role: 'agent', content: 'Hello! I am your AI Job Agent. You can ask me to help you build a resume or prepare for an interview. (Make sure you provide a job_id if you want me to use your tracked job context!)' }
  ]);
  const [input, setInput] = useState('');
  const [jobId, setJobId] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const payload = { user_input: userMsg.content };
      if (jobId) payload.job_id = parseInt(jobId);

      const response = await axios.post('http://localhost:8000/api/v1/agent/', payload);
      
      setMessages(prev => [...prev, { role: 'agent', content: response.data.output }]);
    } catch (error) {
      console.error('Agent error:', error);
      setMessages(prev => [...prev, { role: 'agent', content: 'Sorry, I encountered an error. Please try again.' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="animate-fade-in" style={{ paddingTop: '2rem', display: 'flex', flexDirection: 'column', height: 'calc(100vh - 120px)' }}>
      <h1>AI Agent Chat</h1>
      <p>Interact with the LangGraph AI ecosystem.</p>

      <div style={{ marginBottom: '1rem', display: 'flex', gap: '1rem', alignItems: 'center' }}>
        <label style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Attach Context (Job ID):</label>
        <input 
          type="number" 
          value={jobId} 
          onChange={(e) => setJobId(e.target.value)}
          placeholder="e.g., 1"
          style={{ 
            background: 'var(--bg-tertiary)', border: '1px solid var(--border-color)', 
            color: 'white', padding: '0.5rem', borderRadius: 'var(--radius-md)'
          }}
        />
      </div>
      
      <div className="glass-panel" style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        <div style={{ flex: 1, overflowY: 'auto', padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {messages.map((msg, i) => (
            <div key={i} style={{ 
              display: 'flex', 
              gap: '1rem', 
              alignItems: 'flex-start',
              flexDirection: msg.role === 'user' ? 'row-reverse' : 'row'
            }}>
              <div style={{ 
                background: msg.role === 'user' ? 'var(--accent-primary)' : 'var(--bg-tertiary)',
                padding: '0.75rem',
                borderRadius: '50%',
                display: 'flex', alignItems: 'center', justifyContent: 'center'
              }}>
                {msg.role === 'user' ? <User size={20} /> : <Bot size={20} />}
              </div>
              <div style={{ 
                background: msg.role === 'user' ? 'var(--accent-primary)' : 'var(--bg-secondary)',
                padding: '1rem',
                borderRadius: 'var(--radius-lg)',
                maxWidth: '75%',
                whiteSpace: 'pre-wrap',
                boxShadow: 'var(--shadow-sm)'
              }}>
                {msg.content}
              </div>
            </div>
          ))}
          {loading && (
            <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
              <div style={{ background: 'var(--bg-tertiary)', padding: '0.75rem', borderRadius: '50%' }}>
                <Bot size={20} />
              </div>
              <div style={{ color: 'var(--text-tertiary)' }}>Thinking...</div>
            </div>
          )}
        </div>
        
        <form onSubmit={handleSend} style={{ display: 'flex', gap: '1rem', padding: '1.5rem', borderTop: '1px solid var(--border-color)', background: 'rgba(15, 23, 42, 0.5)' }}>
          <input 
            type="text" 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            style={{ 
              flex: 1, background: 'var(--bg-primary)', border: '1px solid var(--border-color)', 
              color: 'white', padding: '1rem', borderRadius: 'var(--radius-md)',
              outline: 'none'
            }}
          />
          <button type="submit" className="btn btn-primary" disabled={loading || !input.trim()} style={{ padding: '0 1.5rem' }}>
            <Send size={20} />
            Send
          </button>
        </form>
      </div>
    </div>
  );
};

export default AgentChat;
