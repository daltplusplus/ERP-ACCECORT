import axios from 'axios'

export async function getProducts() {
  try {
    const response = await axios.get('http://localhost:5000/products')
    return response.data
  } catch (error) {
    console.error('Error al obtener clientes:', error)
    throw error
  }
}

export async function createProduct(product) {
  try {
    const response = await axios.post('http://localhost:5000/products', product)
    return response.data
  } catch (error) {
    console.error('Error al obtener clientes:', error)
    throw error
  }
}

export async function deleteProduct(productId) {
  try {
    const response = await axios.delete(`http://localhost:5000/products/${productId}`)
    return response.data
  } catch (error) {
    console.error('Error al borrar producto:', error)
    throw error
  }
}

export async function updateProduct(productId, newData) {
  const data = {
    name: newData.name
  }
  try {
    const response = await axios.patch(`http://localhost:5000/products/${productId}`, data)
    return response.data
  } catch (error) {
    console.error('Error al borrar producto:', error)
    throw error
  }
}