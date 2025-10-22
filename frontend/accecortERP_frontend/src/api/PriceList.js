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

export async function getPriceLists() {
  try {
    const response = await api.get(`/price-lists`)
    return response.data
  } catch (error) {
    console.error('Error al obtener clientes:', error)
    throw error
  }
}

export async function getPriceListItems(list_id) {
  try {
    const response = await api.get(`/price-lists/${list_id}/items`)
    return response.data
  } catch (error) {
    console.error('Error al obtener clientes:', error)
    throw error
  }
}

export async function createPricelist(data) {
  try {
    const response = await api.post(`/price-lists`, data)
    return response.data
  } catch (error) {
    console.error('Error al obtener clientes:', error)
    throw error
  }
}