import axios from 'axios'
import api from './axios';

export async function createTicket(clientId) {
  const ticket = {
    "client_id": clientId
  }
  try {
    const response = await api.post('/tickets',ticket)
    return response.data
  } catch (error) {
    console.error('Error al crear el ticket:', error)
    throw error
  }
}

export async function getTicket(ticketId) {
  try {
    const response = await api.get(`/tickets/${ticketId}`)
    return response.data
  } catch (error) {
    console.error('Error al obtener el ticket:', error)
    throw error
  }
}

export async function getClientTickets(clientId) {
  try {
    const response = await api.get(`/tickets/client/${clientId}`)
    return response.data
  } catch (error) {
    console.error('Error al obtener el ticket:', error)
    throw error
  }
}

export async function changeTicket(ticketId, changes) {
  try {
    const response = await api.patch(`/tickets/${ticketId}`, changes)
    return response.data
  } catch (error) {
    console.error('Error al obtener el ticket:', error)
    throw error
  }
} 