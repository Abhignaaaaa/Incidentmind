import React, { useState } from 'react';
import axios from 'axios';

const AgentPage: React.FC = () => {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState<any>(null);

  const sendMessage = async () => {
    try {
      const res = await axios.post('http://localhost:8001/api/agent/chat', { message });
      setResponse(res.data);
    } catch (err) {
      console.error(err);
      setResponse({ error: "Failed to connect to agent" });
    }
  };

  return (
    <div>
      <h2>Agent Chat</h2>
      <div className="mb-3">
        <textarea 
          className="form-control" 
          rows={3} 
          value={message} 
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask the agent about an incident..."
        />
      </div>
      <button className="btn btn-primary mb-4" onClick={sendMessage}>Send</button>

      {response && !response.error && (
        <div className="card">
          <div className="card-body">
            <h5 className="card-title">Agent Response</h5>
            <p className="card-text">{response.response}</p>
            <p className="text-muted"><small>Memory Used: {response.memory_used ? 'Yes' : 'No'}</small></p>
          </div>
        </div>
      )}
      
      {response && response.error && (
        <div className="alert alert-danger">{response.error}</div>
      )}
    </div>
  );
};

export default AgentPage;
