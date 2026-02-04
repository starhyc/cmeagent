import { useState, useEffect } from 'react';
import axios from 'axios';

export default function AnalysisResults({ sessionId }) {
  const [taskId, setTaskId] = useState(null);
  const [status, setStatus] = useState(null);
  const [results, setResults] = useState(null);

  const startAnalysis = async () => {
    const token = localStorage.getItem('token');
    const response = await axios.post('/api/analysis/trigger', { session_id: sessionId }, {
      headers: { Authorization: `Bearer ${token}` }
    });
    setTaskId(response.data.task_id);
    pollStatus(response.data.task_id);
  };

  const pollStatus = async (id) => {
    const token = localStorage.getItem('token');
    const interval = setInterval(async () => {
      const response = await axios.get(`/api/analysis/status/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setStatus(response.data);
      if (response.data.status === 'completed') {
        clearInterval(interval);
        loadResults(id);
      }
    }, 2000);
  };

  const loadResults = async (id) => {
    const token = localStorage.getItem('token');
    const response = await axios.get(`/api/analysis/results/${id}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    setResults(response.data);
  };

  return (
    <div>
      <h2>Analysis Results</h2>
      <button onClick={startAnalysis}>Start Analysis</button>
      {status && <p>Status: {status.status} ({status.progress}%)</p>}
      {results && (
        <div>
          <h3>Root Cause</h3>
          <p>{results.root_cause?.analysis}</p>
          <h3>Issues</h3>
          <ul>
            {results.ranked_issues?.map((issue, i) => (
              <li key={i}>{issue.severity}: {issue.message}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
