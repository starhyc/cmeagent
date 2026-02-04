import { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import LogUpload from './components/LogUpload';
import SSHServers from './components/SSHServers';
import AnalysisResults from './components/AnalysisResults';
import ReportHistory from './components/ReportHistory';
import UserManagement from './components/UserManagement';
import axios from 'axios';

axios.defaults.baseURL = 'http://localhost:8000';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));

  if (!token) {
    return <Login onLogin={setToken} />;
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" />} />
        <Route path="/dashboard" element={<Dashboard />}>
          <Route index element={<div><h2>Welcome to Problem Diagnosis Assistant</h2></div>} />
          <Route path="logs" element={<LogUpload />} />
          <Route path="ssh-servers" element={<SSHServers />} />
          <Route path="analysis" element={<AnalysisResults />} />
          <Route path="reports" element={<ReportHistory />} />
          <Route path="users" element={<UserManagement />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;

