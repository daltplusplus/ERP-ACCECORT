<!-- src/views/ProductosView.vue -->
<template>
  <div class="p-6 max-w-md mx-auto">
    <h1 class="text-3xl font-bold mb-6">Productos</h1>

    <!-- Botón para nuevo producto -->
    <button
      @click="modalNewProductOpen = true"
      class="mb-6 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
    >
      Nuevo Producto
    </button>

    <!-- Modal nuevo producto -->
    <div
      v-if="modalNewProductOpen"
      class="fixed inset-0 bg-black/50 flex justify-center items-center z-50"
    >
      <div class="bg-white rounded-lg p-6 w-full max-w-sm shadow-lg relative">
        <h2 class="text-xl font-semibold mb-4">Agregar nuevo producto</h2>

        <form @submit.prevent="addProducto">
          <input
            v-model="nuevoProductoNombre"
            type="text"
            placeholder="Nombre del producto"
            class="border rounded px-3 py-2 w-full mb-4"
            required
            autofocus
          />

          <div class="flex justify-end gap-3">
            <button
              type="button"
              @click="closeModal"
              class="px-4 py-2 rounded border border-gray-300 hover:bg-gray-100"
            >
              Cancelar
            </button>
            <button
              type="submit"
              class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
            >
              Agregar
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Lista de productos -->
    <div class="flex flex-col gap-3 mb-6">
      <div
        v-for="producto in productos"
        :key="producto.id"
        class="p-3 border rounded shadow-sm bg-white flex justify-between items-center"
      >
        <span>{{ producto.name }}</span>

        <div class="flex gap-2">
          <!-- Botón editar -->
          <button
            @click="abrirModalEditar(producto)"
            class="bg-yellow-500 text-white px-3 py-1 rounded hover:bg-yellow-600 transition"
          >
            Editar
          </button>

          <!-- Botón borrar -->
          <button
            @click="confirmarBorrado(producto)"
            class="bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700 transition"
          >
            Borrar
          </button>
        </div>
      </div>
    </div>

    <!-- Botón para aumento -->
    <button
      @click="modalIncreaseOpen = true"
      class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition"
    >
      Aumentar todo
    </button>

    <!-- Modal aumento -->
    <div
      v-if="modalIncreaseOpen"
      class="fixed inset-0 bg-black/50 flex justify-center items-center z-50"
    >
      <div class="bg-white rounded-lg p-6 w-full max-w-sm shadow-lg relative">
        <h2 class="text-xl font-semibold mb-4">Aumentar todos los precios</h2>

        <form @submit.prevent="confirmarAumento">
          <input
            v-model.number="increase"
            type="number"
            placeholder="Porcentaje de aumento (%)"
            class="border rounded px-3 py-2 w-full mb-4"
            min="1"
            required
          />

          <!-- Primera confirmación -->
          <div v-if="confirmStep === 1" class="flex justify-end gap-3">
            <button
              type="button"
              @click="closeModal"
              class="px-4 py-2 rounded border border-gray-300 hover:bg-gray-100"
            >
              Cancelar
            </button>
            <button
              type="button"
              @click="goToConfirmation"
              class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
            >
              Continuar
            </button>
          </div>

          <!-- Segunda confirmación -->
          <div v-else-if="confirmStep === 2" class="text-center space-y-4">
            <p>¿Seguro que deseas aumentar <strong>{{ increase }}%</strong> todos los precios?</p>
            <div class="flex justify-center gap-3">
              <button
                type="button"
                @click="confirmStep = 1"
                class="px-4 py-2 rounded border border-gray-300 hover:bg-gray-100"
              >
                Volver
              </button>
              <button
                type="submit"
                class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition"
              >
                Confirmar
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal editar producto -->
    <div
      v-if="modalEditOpen"
      class="fixed inset-0 bg-black/50 flex justify-center items-center z-50"
    >
      <div class="bg-white rounded-lg p-6 w-full max-w-sm shadow-lg relative">
        <h2 class="text-xl font-semibold mb-4">Editar producto</h2>

        <form @submit.prevent="actualizarProducto">
          <input
            v-model="productoEditando.name"
            type="text"
            placeholder="Nuevo nombre del producto"
            class="border rounded px-3 py-2 w-full mb-4"
            required
          />

          <div class="flex justify-end gap-3">
            <button
              type="button"
              @click="closeModal"
              class="px-4 py-2 rounded border border-gray-300 hover:bg-gray-100"
            >
              Cancelar
            </button>
            <button
              type="submit"
              class="bg-yellow-500 text-white px-4 py-2 rounded hover:bg-yellow-600 transition"
            >
              Guardar
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { createProduct, getProducts, deleteProduct, updateProduct } from '../api/Products'
import { itemGlobalIncrease } from '../api/PriceList'

const productos = ref([])
const modalNewProductOpen = ref(false)
const modalIncreaseOpen = ref(false)
const modalEditOpen = ref(false)
const confirmStep = ref(1)
const increase = ref(0)
const nuevoProductoNombre = ref('')
const productoEditando = ref(null)

onMounted(async () => {
  try {
    const data = await getProducts()
    productos.value = data.sort((a, b) => a.name.localeCompare(b.name))
  } catch (error) {
    console.error('Error cargando productos:', error)
  }
})

function closeModal() {
  modalIncreaseOpen.value = false
  modalNewProductOpen.value = false
  modalEditOpen.value = false
  confirmStep.value = 1
  increase.value = 0
  nuevoProductoNombre.value = ''
  productoEditando.value = null
}

async function addProducto() {
  if (!nuevoProductoNombre.value.trim()) return
  try {
    const productoCreado = await createProduct({ name: nuevoProductoNombre.value.trim() })
    productos.value.push(productoCreado)
    productos.value.sort((a, b) => a.name.localeCompare(b.name))
    closeModal()
  } catch (error) {
    console.error('Error creando producto:', error)
  }
}

function goToConfirmation() {
  if (increase.value < 1) {
    alert('El aumento debe ser al menos 1%.')
    return
  }
  confirmStep.value = 2
}

function confirmarAumento() {
  itemGlobalIncrease(increase.value)
  alert(`✅ Se aumentaron todos los precios en ${increase.value}%`)
  closeModal()
}

function abrirModalEditar(producto) {
  productoEditando.value = { ...producto }
  modalEditOpen.value = true
}

async function actualizarProducto() {
  if (!productoEditando.value.name.trim()) return
  try {
    await updateProduct(productoEditando.value.id, { name: productoEditando.value.name.trim() })
    const p = productos.value.find(p => p.id === productoEditando.value.id)
    if (p) p.name = productoEditando.value.name.trim()
    productos.value.sort((a, b) => a.name.localeCompare(b.name))
    closeModal()
  } catch (error) {
    console.error('Error actualizando producto:', error)
  }
}

async function confirmarBorrado(producto) {
  const confirmado = confirm(`¿Seguro que deseas eliminar "${producto.name}"?`)
  if (!confirmado) return
  try {
    await deleteProduct(producto.id)
    productos.value = productos.value.filter(p => p.id !== producto.id)
  } catch (error) {
    console.error('Error eliminando producto:', error)
  }
}
</script>
