import axios from 'axios'
import api from './axios';

export async function getClients() {
  try {
    const response = await api.get('/clients')
    return response.data
  } catch (error) {
    console.error('Error al obtener clientes:', error)
    throw error
  }
}

export async function getClient(clientId) {
  try {
    const response = await api.get(`/clients/${clientId}`)
    return response.data
  } catch (error) {
    console.error('Error al obtener clientes:', error)
    throw error
  }
}

export async function createClient(client) {
  try {
    const response = await api.post('/clients',client)
    return response.data
  } catch (error) {
    console.error('Error al obtener clientes:', error)
    throw error
  }
}

export async function getClientPrices(clientId) {
  try {
    const response = await api.get(`/clients/${clientId}/prices`);
    return response.data
  } catch (error) {
    console.error('Error al obtener clientes:', error)
    throw error
  }
}

export async function updateClient(clientId, data) {
  try {
    const response = await api.patch(`/clients/${clientId}`,data);
    return response.data
  } catch (error) {
    console.error('Error al obtener clientes:', error)
    throw error
  }
}