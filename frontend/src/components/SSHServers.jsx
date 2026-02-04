import { useState, useEffect } from 'react';
import axios from 'axios';

export default function SSHServers() {
  const [servers, setServers] = useState([]);
  const [form, setForm] = useState({ name: '', host: '', port: 22, username: '', password: '', log_path: '' });

  useEffect(() => {
    loadServers();
  }, []);

  const loadServers = async () => {
    const token = localStorage.getItem('token');
    const response = await axios.get('/api/ssh-servers', {
      headers: { Authorization: `Bearer ${token}` }
    });
    setServers(response.data);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem('token');
    await axios.post('/api/ssh-servers', form, {
      headers: { Authorization: `Bearer ${token}` }
    });
    setForm({ name: '', host: '', port: 22, username: '', password: '', log_path: '' });
    loadServers();
  };

  const handleDelete = async (id) => {
    const token = localStorage.getItem('token');
    await axios.delete(`/api/ssh-servers/${id}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    loadServers();
  };

  return (
    <div>
      <h2>SSH Servers</h2>
      <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
        <input placeholder="Name" value={form.name} onChange={(e) => setForm({...form, name: e.target.value})} required />
        <input placeholder="Host" value={form.host} onChange={(e) => setForm({...form, host: e.target.value})} required />
        <input type="number" placeholder="Port" value={form.port} onChange={(e) => setForm({...form, port: e.target.value})} />
        <input placeholder="Username" value={form.username} onChange={(e) => setForm({...form, username: e.target.value})} required />
        <input type="password" placeholder="Password" value={form.password} onChange={(e) => setForm({...form, password: e.target.value})} required />
        <input placeholder="Log Path" value={form.log_path} onChange={(e) => setForm({...form, log_path: e.target.value})} />
        <button type="submit">Add Server</button>
      </form>
      <table>
        <thead>
          <tr><th>Name</th><th>Host</th><th>Port</th><th>Username</th><th>Actions</th></tr>
        </thead>
        <tbody>
          {servers.map(s => (
            <tr key={s.id}>
              <td>{s.name}</td><td>{s.host}</td><td>{s.port}</td><td>{s.username}</td>
              <td><button onClick={() => handleDelete(s.id)}>Delete</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
