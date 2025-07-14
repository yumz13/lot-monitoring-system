import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { loginEmployee } from '../store/actions/authActions';

const Login = () => {
  const [cardNumber, setCardNumber] = useState('');
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { loading, error } = useSelector(state => state.auth);
  const { selectedArea, selectedProcess } = useSelector(state => state.system);

  const handleLogin = () => {
    if (!cardNumber || !selectedArea || !selectedProcess) {
      alert('Please select area and process first');
      return;
    }
    
    dispatch(loginEmployee({
      cardNumber,
      areaId: selectedArea,
      processId: selectedProcess
    })).then(() => {
      navigate('/material-prep');
    });
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded shadow">
      <h2 className="text-xl font-semibold mb-4">Employee Login</h2>
      
      {error && <div className="text-red-500 mb-4">{error}</div>}
      
      <div className="mb-4">
        <label className="block text-gray-700 mb-2">Card Number</label>
        <input
          type="text"
          value={cardNumber}
          onChange={(e) => setCardNumber(e.target.value)}
          className="w-full p-2 border rounded"
          placeholder="Tap your employee card"
        />
      </div>
      
      <button
        onClick={handleLogin}
        disabled={loading}
        className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
      >
        {loading ? 'Logging in...' : 'Login'}
      </button>
    </div>
  );
};

export default Login;