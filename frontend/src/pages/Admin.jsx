import React from 'react';
import { useSelector } from 'react-redux';

const Admin = () => {
  const { employee } = useSelector(state => state.auth);
  
  if (!employee || employee.role !== 'admin') {
    return (
      <div className="container mx-auto p-4">
        <h2 className="text-xl font-semibold">Access Denied</h2>
        <p>You must be an administrator to access this page.</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">Administration Panel</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded shadow">
          <h3 className="text-lg font-semibold mb-4">Employee Management</h3>
          {/* Employee management components would go here */}
        </div>
        
        <div className="bg-white p-6 rounded shadow">
          <h3 className="text-lg font-semibold mb-4">Defect Code Management</h3>
          {/* Defect code management components would go here */}
        </div>
        
        <div className="bg-white p-6 rounded shadow">
          <h3 className="text-lg font-semibold mb-4">System Configuration</h3>
          {/* System configuration components would go here */}
        </div>
      </div>
    </div>
  );
};

export default Admin;