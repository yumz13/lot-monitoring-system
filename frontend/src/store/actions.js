import api from '../services/api';
import * as authService from '../services/auth';

// Auth Actions
export const loginEmployee = (credentials) => async (dispatch) => {
  try {
    const { employee, token, session } = await authService.login(
      credentials.cardNumber,
      credentials.areaId,
      credentials.processId
    );
    
    dispatch({
      type: 'LOGIN_SUCCESS',
      payload: { employee, token, session }
    });
    
    return Promise.resolve();
  } catch (error) {
    dispatch({
      type: 'LOGIN_FAILURE',
      payload: error
    });
    return Promise.reject(error);
  }
};

export const logoutEmployee = () => async (dispatch) => {
  try {
    await authService.logout();
    dispatch({ type: 'LOGOUT' });
  } catch (error) {
    console.error('Logout error:', error);
  }
};

// Area Actions
export const fetchAreas = () => async (dispatch) => {
  dispatch({ type: 'FETCH_AREAS_REQUEST' });
  try {
    const response = await api.get('/areas');
    dispatch({
      type: 'FETCH_AREAS_SUCCESS',
      payload: response.data
    });
  } catch (error) {
    dispatch({
      type: 'FETCH_AREAS_FAILURE',
      payload: error.response?.data?.error || 'Failed to fetch areas'
    });
  }
};

// Process Actions
export const fetchProcesses = () => async (dispatch) => {
  dispatch({ type: 'FETCH_PROCESSES_REQUEST' });
  try {
    const response = await api.get('/processes');
    dispatch({
      type: 'FETCH_PROCESSES_SUCCESS',
      payload: response.data
    });
  } catch (error) {
    dispatch({
      type: 'FETCH_PROCESSES_FAILURE',
      payload: error.response?.data?.error || 'Failed to fetch processes'
    });
  }
};

// System Actions
export const selectArea = (areaId) => ({
  type: 'SELECT_AREA',
  payload: areaId
});

export const selectProcess = (processId) => ({
  type: 'SELECT_PROCESS',
  payload: processId
});