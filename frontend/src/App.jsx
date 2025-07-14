import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Provider } from 'react-redux';
import store from './store/store';
import Navbar from './components/Navbar';
import Login from './components/Login';
import AreaSelection from './components/AreaSelection';
import MaterialPrep from './pages/MaterialPrep';
import Assembly from './pages/Assembly';
import AssemblyInspection from './pages/AssemblyInspection';
import Oven from './pages/Oven';
import QCInspection from './pages/QCInspection';
import Dashboard from './components/Dashboard';
import Admin from './pages/Admin';

function App() {
  return (
    <Provider store={store}>
      <Router>
        <div className="min-h-screen bg-gray-100">
          <Navbar />
          <div className="container mx-auto px-4 py-8">
            <Routes>
              <Route path="/" element={<AreaSelection />} />
              <Route path="/login" element={<Login />} />
              <Route path="/material-prep" element={<MaterialPrep />} />
              <Route path="/assembly" element={<Assembly />} />
              <Route path="/assembly-inspection" element={<AssemblyInspection />} />
              <Route path="/oven" element={<Oven />} />
              <Route path="/qc-inspection" element={<QCInspection />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/admin" element={<Admin />} />
            </Routes>
          </div>
        </div>
      </Router>
    </Provider>
  );
}

export default App;