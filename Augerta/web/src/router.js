import { createRouter, createWebHistory } from 'vue-router';
import CallAuction from './call_auction.vue';

const routes = [
  { path: '/call_auction', name: 'CallAuction', component: CallAuction },
];

const router = createRouter({ 
  history: createWebHistory(), 
  routes 
});

export default router;