import api from './axios';

export async function getDashboard() {
  try {
    const response = await api.get('/dashboard')
    return response.data

  } catch (error) {
    console.error('Error al obtener clientes:', error)
    throw error
  }
}