import axios from 'axios';
import store from '../store/';

const API_BASE_URL = import.meta.env.VITE_BACKEND_BASE_PATH;

const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

// Add an interceptor to set the "Authorization" header with the token
apiClient.interceptors.request.use(config => {
  const token = store.state.token;
  if (token) {
    config.headers['Authorization'] = `Token ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

export const login = async (loginData) => {
  return apiClient.post('/login/', loginData);
};

export const register = async (registerData) => {
  return apiClient.post('/register/', registerData);
};

export const logout = async () => {
  return apiClient.post('/logout/')
};

export const getTrades = async (page, user, startDate, endDate, buySell, symbol) => {
  const config = {
    params: {
      page: page,
      user: user,
      start_date: startDate,
      end_date: endDate,
      buy_sell: buySell,
      symbol: symbol,
    },
  };

  return apiClient.get('/trades/', config)
    .then((response) => {
      const trades = response.data;
      return trades;
    })
    .catch((error) => {
      console.error('Error fetching trades:', error);
      throw error;
    });
};

export const getTradeById = async (id) => {
  return apiClient.get(`/trades/${id}`)
    .then((response) => {
      const trades = response.data;
      return trades;
    })
    .catch((error) => {
      console.error('Error fetching trades:', error);
      throw error;
    });
};

export const createTrade = async (tradeData) => {
  return apiClient.post('/trades/', tradeData);
};

export const updateTrade = async (tradeData, id) => {
  return apiClient.put(`/trades/${id}/update/`, tradeData);
}

export const getUsers = async (page, age, startDate, endDate, keyword) => {
  const config = {
    params: {
      page: page,
      age: age,
      start_date: startDate,
      end_date: endDate,
      keyword: keyword,
    },
  };
  return apiClient.get('/users/', config)
    .then((response) => {
      const users = response.data;
      return users;
    })
    .catch((error) => {
      console.error('Error fetching users:', error);
      throw error;
    });
};

export const getProfile = async () => {
  return apiClient.get(`/profile/`)
  .then((response) => {
    const profile = response.data;
    return profile;
  })
  .catch((error) => {
    console.error('Error fetching profile:', error);
    throw error;
  });
}

export const changePassword = async (formData)=> {
  return apiClient.post('/change-password/', formData);
}