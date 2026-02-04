import { Link, Outlet } from 'react-router-dom';

export default function Dashboard() {
  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/';
  };

  return (
    <div style={{ display: 'flex', height: '100vh' }}>
      <nav style={{ width: '200px', background: '#f5f5f5', padding: '20px' }}>
        <h3>Menu</h3>
        <ul style={{ listStyle: 'none', padding: 0 }}>
          <li style={{ marginBottom: '10px' }}>
            <Link to="/dashboard">Home</Link>
          </li>
          <li style={{ marginBottom: '10px' }}>
            <Link to="/dashboard/logs">Upload Logs</Link>
          </li>
          <li style={{ marginBottom: '10px' }}>
            <Link to="/dashboard/ssh-servers">SSH Servers</Link>
          </li>
          <li style={{ marginBottom: '10px' }}>
            <Link to="/dashboard/analysis">Analysis</Link>
          </li>
          <li style={{ marginBottom: '10px' }}>
            <Link to="/dashboard/reports">Reports</Link>
          </li>
          <li style={{ marginBottom: '10px' }}>
            <Link to="/dashboard/code">Code Search</Link>
          </li>
          <li style={{ marginBottom: '10px' }}>
            <Link to="/dashboard/users">Users</Link>
          </li>
        </ul>
        <button onClick={handleLogout} style={{ marginTop: '20px' }}>Logout</button>
      </nav>
      <main style={{ flex: 1, padding: '20px', overflow: 'auto' }}>
        <Outlet />
      </main>
    </div>
  );
}
