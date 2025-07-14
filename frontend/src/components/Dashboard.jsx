import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchDashboardData } from '../store/actions/dashboardActions';

const Dashboard = () => {
  const dispatch = useDispatch();
  const { summary, loading, error } = useSelector(state => state.dashboard);

  useEffect(() => {
    dispatch(fetchDashboardData());
  }, [dispatch]);

  if (loading) return <div>Loading dashboard...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">Production Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white p-4 rounded shadow">
          <h3 className="text-gray-500">Total Lots</h3>
          <p className="text-3xl font-bold">{summary?.total_lots || 0}</p>
        </div>
        <div className="bg-white p-4 rounded shadow">
          <h3 className="text-gray-500">Completed Lots</h3>
          <p className="text-3xl font-bold text-green-600">{summary?.completed_lots || 0}</p>
        </div>
        <div className="bg-white p-4 rounded shadow">
          <h3 className="text-gray-500">Active Lots</h3>
          <p className="text-3xl font-bold text-blue-600">{summary?.active_lots || 0}</p>
        </div>
        <div className="bg-white p-4 rounded shadow">
          <h3 className="text-gray-500">Defect Rate</h3>
          <p className="text-3xl font-bold text-red-600">{summary?.defect_rate ? `${summary.defect_rate}%` : '0%'}</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;