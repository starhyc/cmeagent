import { useState, useEffect } from 'react';
import axios from 'axios';

export default function ReportHistory() {
  const [reports, setReports] = useState([]);

  useEffect(() => {
    loadReports();
  }, []);

  const loadReports = async () => {
    const token = localStorage.getItem('token');
    const response = await axios.get('/api/reports/history', {
      headers: { Authorization: `Bearer ${token}` }
    });
    setReports(response.data);
  };

  const downloadReport = (id, format) => {
    const token = localStorage.getItem('token');
    window.open(`/api/reports/${id}/export/${format}?token=${token}`, '_blank');
  };

  return (
    <div>
      <h2>Report History</h2>
      <table>
        <thead>
          <tr><th>Title</th><th>Created</th><th>Actions</th></tr>
        </thead>
        <tbody>
          {reports.map(r => (
            <tr key={r.id}>
              <td>{r.title}</td>
              <td>{new Date(r.created_at).toLocaleString()}</td>
              <td>
                <button onClick={() => downloadReport(r.id, 'markdown')}>MD</button>
                <button onClick={() => downloadReport(r.id, 'pdf')}>PDF</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
