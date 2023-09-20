import { createStore } from 'vuex';
import { login, logout } from '../services/api.js';
import router from '../router'

const store = createStore({
  actions: {
    async login({ commit }, data) {
      try {
        const response = await login(data);
        const token = response.data.token;
        const email = response.data.email;
        const username = response.data.username;
        const name = response.data.name;
        const isSuperUser = response.data.is_superuser;
        const isStaff = response.data.is_staff;

        commit('setToken', token);
        commit('setEmail', email);
        commit('setUsername', username);
        commit('setName', name);
        commit('setIsSuperUser', isSuperUser);
        commit('setIsStaff', isStaff);
        commit('setLoggedIn', true);

        if (store.state.loggedIn) {
          router.push('/trades');
        }

      } catch (error) {
        console.log('Login error:', error);
      }
    },
    async logout({ commit }) {
      try {
        await logout();

        commit('setToken', null);
        commit('setLoggedIn', false);
        commit('setEmail', null);
        commit('setUsername', null);
        commit('setName', null);
        commit('setIsSuperUser', null);
        commit('setIsStaff', null);

        localStorage.removeItem('user');

        router.push('/login');
      } catch (error) {
        console.log('Logout error:', error);
      }
    },
  },
  mutations: {
    setToken(state, token) {
      state.token = token;
    },
    setLoggedIn(state, loggedIn) {
      state.loggedIn = loggedIn;
    },
    setEmail(state, email) {
      state.email = email;
    },
    setUsername(state, username) {
      state.username = username;
    },
    setName(state, name) {
      state.name = name;
    },
    setIsSuperUser(state, isSuperUser) {
      state.isSuperUser = isSuperUser;
    },
    setIsStaff(state, isStaff) {
      state.isStaff = isStaff;
    }
  },
});

store.subscribe((mutation, state) => {
  localStorage.setItem('user', JSON.stringify(state));
});

export default store;