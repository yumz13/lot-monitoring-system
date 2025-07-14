import { configureStore } from '@reduxjs/toolkit';
import authReducer from './reducers/authReducer';
import areaReducer from './reducers/areaReducer';
import processReducer from './reducers/processReducer';
import lotReducer from './reducers/lotReducer';

const store = configureStore({
  reducer: {
    auth: authReducer,
    areas: areaReducer,
    processes: processReducer,
    lots: lotReducer
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false
    })
});

export default store;