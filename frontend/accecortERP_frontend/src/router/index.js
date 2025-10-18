// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import ClientsView from '../views/ClientsView.vue'
import ProductsView from '../views/ProductsView.vue'
import PriceListView from '../views/PriceListView.vue'
import CreateTicketView from '../views/CreateTicketView.vue'
import EditTicketView from '../views/EditTicketView.vue'
import TicketsView from '../views/TicketsView.vue'

const routes = [
  { path: '/clientes', component: ClientsView },
  { path: '/productos', component: ProductsView },
  { path: '/clientes/:id/lista', component: PriceListView },
  { path: '/crear-ticket', component: CreateTicketView},
  { path: '/editar-ticket/:id', component: EditTicketView},
  { path: '/clientes/:id/ticket', component: TicketsView}
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})

