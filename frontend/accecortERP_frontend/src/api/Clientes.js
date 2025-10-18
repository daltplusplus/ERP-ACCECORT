import axios from 'axios'

export async function getClients() {
  try {
    const response = await axios.get('http://localhost:5000/clients')
    return response.data
  } catch (error) {
    console.error('Error al obtener clientes:', error)
    throw error
  }
}

export async function getClient(clientId) {
  try {
    const response = await axios.get(`http://localhost:5000/clients/${clientId}`)
    return response.data
  } catch (error) {
    console.error('Error al obtener clientes:', error)
    throw error
  }
}

export async function createClient(client) {
  try {
    const response = await axios.post('http://localhost:5000/clients',client)
    return response.data
  } catch (error) {
    console.error('Error al obtener clientes:', error)
    throw error
  }
}

export async function getClientPrices(clientId) {
  try {
    const response = await axios.get(`http://localhost:5000/clients/${clientId}/prices`);
    return response.data
  } catch (error) {
    console.error('Error al obtener clientes:', error)
    throw error
  }
}
