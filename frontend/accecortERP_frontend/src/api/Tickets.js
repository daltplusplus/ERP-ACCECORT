import axios from 'axios'

export async function createTicket(clientId) {
  const ticket = {
    "client_id": clientId
  }
  try {
    const response = await axios.post('http://localhost:5000/tickets',ticket)
    return response.data
  } catch (error) {
    console.error('Error al crear el ticket:', error)
    throw error
  }
}

export async function getTicket(ticketId) {
  try {
    const response = await axios.get(`http://localhost:5000/tickets/${ticketId}`)
    return response.data
  } catch (error) {
    console.error('Error al obtener el ticket:', error)
    throw error
  }
}

export async function getClientTickets(clientId) {
  try {
    const response = await axios.get(`http://localhost:5000/tickets/client/${clientId}`)
    return response.data
  } catch (error) {
    console.error('Error al obtener el ticket:', error)
    throw error
  }
}

export async function changeTicket(ticketId, changes) {
  try {
    const response = await axios.patch(`http://localhost:5000/tickets/${ticketId}`, changes)
    return response.data
  } catch (error) {
    console.error('Error al obtener el ticket:', error)
    throw error
  }
} 