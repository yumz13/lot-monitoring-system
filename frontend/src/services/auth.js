import api from './api';

export const login = async (cardNumber, areaId, processId) => {
  try {
    const response = await api.post('/auth/login', {
      card_number: cardNumber,
      area_id: areaId,
      process_id: processId
    });
    localStorage.setItem('token', response.data.token);
    return response.data;
  } catch (error) {
    throw error.response?.data?.error || 'Login failed';
  }
};

export const logout = async () => {
  try {
    await api.post('/auth/logout');
    localStorage.removeItem('token');
  } catch (error) {
    throw error.response?.data?.error || 'Logout failed';
  }
};

export const validateToken = async () => {
  try {
    const token = localStorage.getItem('token');
    if (!token) return null;
    
    const response = await api.get('/auth/validate');
    return response.data;
  } catch (error) {
    localStorage.removeItem('token');
    return null;
  }
};