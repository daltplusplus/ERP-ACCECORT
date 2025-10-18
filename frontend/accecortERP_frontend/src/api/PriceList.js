import axios from 'axios'

export async function updateItemPrice(itemId, newPrice) {
  const price = {
    price: newPrice
  }

  try {
    const response = await axios.patch(`http://localhost:5000/items/${itemId}`,price)
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
    const response = await axios.patch(`http://localhost:5000/items`,data)
    return response.data
  } catch (error) {
    console.error('Error al obtener clientes:', error)
    throw error
  }
}