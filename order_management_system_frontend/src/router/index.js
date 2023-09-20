import { createRouter, createWebHistory } from 'vue-router';
import store from '../store'; // Import your Vuex store
// import { useStore } from 'vuex';
import Login from '../views/Account/Login.vue';
import Register from '../views/Account/Register.vue';
import Users from '../views/Account/Users.vue';
import MyAccount from '../views/Account/MyAccount.vue';
import ChangePassword from '../views/Account/ChangePassword.vue';

import Summary from '../views/Trades/Summary.vue';
import CreateTrade from '../views/Trades/CreateTrade.vue';
import UpdateTrade from '../views/Trades/UpdateTrade.vue';

import NotFound from '../views/Misc/NotFound.vue';

const routes = [
  {
    name: 'Root',
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
  },
  {
    path: '/users',
    name: 'Users',
    component: Users,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/trades',
    name: 'Summary',
    component: Summary,
    meta: { requiresAuth: true },
  },
  {
    path: '/trades/add',
    name: 'CreateTrade',
    component: CreateTrade,
    meta: { requiresAuth: true },
  },
  {
    path: '/trades/update/:id',
    name: 'UpdateTrade',
    component: UpdateTrade,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/account',
    name: 'MyAccount',
    component: MyAccount,
    meta: { requiresAuth: true },
  },
  {
    path: '/change_password',
    name: 'ChangePassword',
    component: ChangePassword,
    meta: { requiresAuth: true },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.matched.some((route) => route.meta.requiresAuth)) {
    if (localStorage.getItem('user')) {
      const persistedState = JSON.parse(localStorage.getItem('user'));
      if (persistedState) {
        store.replaceState(persistedState);
      }
      if (!persistedState && !persistedState.token && !persistedState.loggedIn) {
        next('/login');
      }
      else {
        next();
      }
    }
    else {
      next('/login');
    }
  } else {
    next(); // Route doesn't require authentication, proceed
  }
  if (to.matched.some((route) => route.meta.requiresAdmin)) {
    next({ name: 'NotFound' });
  }
});

export default router;
