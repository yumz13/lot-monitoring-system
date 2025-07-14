import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link, useNavigate } from 'react-router-dom';
import { logoutEmployee } from '../store/actions/authActions';

const Navbar = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { employee } = useSelector(state => state.auth);
  const { currentArea, currentProcess } = useSelector(state => state.system);

  const handleLogout = () => {
    dispatch(logoutEmployee());
    navigate('/');
  };

  return (
    <nav className="bg-blue-800 text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-xl font-bold">Traveler Slip System</Link>
        
        <div className="flex items-center space-x-4">
          {currentArea && (
            <span className="bg-blue-700 px-3 py-1 rounded">
              Area: {currentArea}
            </span>
          )}
          {currentProcess && (
            <span className="bg-blue-700 px-3 py-1 rounded">
              Process: {currentProcess}
            </span>
          )}
          {employee && (
            <>
              <span>Welcome, {employee.name}</span>
              <button 
                onClick={handleLogout}
                className="bg-red-600 px-3 py-1 rounded hover:bg-red-700"
              >
                Logout
              </button>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;