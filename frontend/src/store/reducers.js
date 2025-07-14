const initialState = {
  auth: {
    employee: null,
    token: null,
    loading: false,
    error: null
  },
  areas: {
    list: [],
    loading: false,
    error: null
  },
  processes: {
    list: [],
    loading: false,
    error: null
  },
  system: {
    selectedArea: null,
    selectedProcess: null,
    currentArea: null,
    currentProcess: null
  }
};

export const authReducer = (state = initialState.auth, action) => {
  switch (action.type) {
    case 'LOGIN_REQUEST':
      return { ...state, loading: true, error: null };
    case 'LOGIN_SUCCESS':
      return { 
        ...state, 
        loading: false,
        employee: action.payload.employee,
        token: action.payload.token
      };
    case 'LOGIN_FAILURE':
      return { ...state, loading: false, error: action.payload };
    case 'LOGOUT':
      return { ...state, employee: null, token: null };
    default:
      return state;
  }
};

export const areaReducer = (state = initialState.areas, action) => {
  switch (action.type) {
    case 'FETCH_AREAS_REQUEST':
      return { ...state, loading: true, error: null };
    case 'FETCH_AREAS_SUCCESS':
      return { ...state, loading: false, list: action.payload };
    case 'FETCH_AREAS_FAILURE':
      return { ...state, loading: false, error: action.payload };
    default:
      return state;
  }
};

export const processReducer = (state = initialState.processes, action) => {
  switch (action.type) {
    case 'FETCH_PROCESSES_REQUEST':
      return { ...state, loading: true, error: null };
    case 'FETCH_PROCESSES_SUCCESS':
      return { ...state, loading: false, list: action.payload };
    case 'FETCH_PROCESSES_FAILURE':
      return { ...state, loading: false, error: action.payload };
    default:
      return state;
  }
};

export const systemReducer = (state = initialState.system, action) => {
  switch (action.type) {
    case 'SELECT_AREA':
      return { ...state, selectedArea: action.payload };
    case 'SELECT_PROCESS':
      return { ...state, selectedProcess: action.payload };
    case 'LOGIN_SUCCESS':
      return {
        ...state,
        currentArea: action.payload.session.area_id,
        currentProcess: action.payload.session.process_id
      };
    case 'LOGOUT':
      return {
        ...state,
        currentArea: null,
        currentProcess: null
      };
    default:
      return state;
  }
};