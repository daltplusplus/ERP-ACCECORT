import axios from 'axios'
import api from './axios';

export async function updateItemPrice(itemId, newPrice) {
  const price = {
    price: newPrice
  }

  try {
    const response = await api.patch(`/items/${itemId}`,price)
    return response.data
  } catch (error) {
    console.error('Error al obtener clientes:', error)
    throw error
  }
}

export async function itemGlobalIncrease(increase) {
  const data = {
    percentage: increase
  }

  try {
    const response = await api.patch(`/items`,data)
    return response.data
  } catch (error) {
    console.error('Error al obtener clientes:', error)
    throw error
  }
}