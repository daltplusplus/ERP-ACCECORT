<template>
  <div class="min-h-screen flex justify-center items-start bg-gray-100 py-10">
    <div class="bg-white shadow-xl rounded-2xl p-8 w-full max-w-5xl space-y-8 border border-gray-200">
      <h1 class="text-3xl font-bold text-center text-gray-800">Editar Boleta</h1>

      

      <!-- Información general -->
      <div class="grid grid-cols-2 gap-4 border rounded-lg p-4 bg-gray-50">
        <div>
          <p class="text-sm text-gray-600 font-semibold">Cliente:</p>
          <p class="text-lg">{{ cliente.name || '---' }}</p>
        </div>
        <div>
          <p class="text-sm text-gray-600 font-semibold">Fecha de emisión:</p>
          <p class="text-lg">{{ ticket.date }}</p>
        </div>
      </div>

      <!-- Productos seleccionados -->
      <div class="border rounded-lg bg-gray-50 p-4">
        <h2 class="text-xl font-semibold mb-4">Productos</h2>

        <!-- Encabezados -->
        <div class="grid grid-cols-5 gap-4 text-sm font-semibold text-gray-600 border-b pb-2">
          <div>Producto</div>
          <div class="text-center">Cantidad</div>
          <div class="text-right">Precio Unitario</div>
          <div class="text-right">Subtotal</div>
          <div class="text-center"></div>
        </div>

        <!-- Filas -->
        <div
          v-for="(item, index) in productosSeleccionados"
          :key="index"
          class="grid grid-cols-5 gap-4 items-center py-3 border-b last:border-none"
        >
          <!-- Producto -->
          <div>
            <select
              v-model="item.producto"
              :disabled="!editable"
              class="w-full rounded-lg border p-2"
              @change="actualizarPrecioUnitario(index)"
            >
              <option disabled value="">Seleccionar producto</option>
              <option
                v-for="producto in productos"
                :key="producto.id"
                :value="producto"
              >
                {{ producto.product }}
              </option>
            </select>
          </div>

          <!-- Cantidad -->
          <div class="text-center">
            <input
              type="number"
              min="1"
              :disabled="!editable"
              class="w-20 rounded-lg border p-2 text-center"
              v-model.number="item.cantidad"
              @input="actualizarSubtotal(index)"
            />
          </div>

          <!-- Precio Unitario -->
          <div class="text-right">
            ${{ item.price?.toFixed(2) || '0.00' }}
          </div>

          <!-- Subtotal -->
          <div class="text-right">
            ${{ item.subtotal?.toFixed(2) || '0.00' }}
          </div>

          <!-- Botón quitar -->
          <div class="text-center">
            <button
              v-if="editable"
              @click="eliminarProducto(index)"
              :disabled="!editable"
              class="bg-red-300 text-white px-2 py-1 rounded-lg hover:bg-red-500 disabled:opacity-50"
            >
              Quitar
            </button>
          </div>
        </div>

        <button
          v-if="editable"
          @click="agregarProducto"
          :disabled="!editable"
          class="bg-blue-500 text-white px-2 py-1 rounded-lg hover:bg-blue-600 disabled:opacity-50 mt-2"
        >
          + Agregar producto
        </button>
      </div>

      <!-- Descuento -->
      <div class="w-48">
        <label class="block text-sm font-semibold mb-1">Descuento (%)</label>
        <input
          type="number"
          min="0"
          max="100"
          v-model.number="descuento"
          :disabled="!editable"
          class="w-full rounded-lg border p-2"
        />
      </div>

      <!-- Totales -->
      <div class="text-right space-y-1 border-t pt-4">
        <div>
          Total sin descuento:
          <strong>${{ totalSinDescuento.toFixed(2) }}</strong>
        </div>
        <div v-if="descuento > 0">
          Descuento aplicado:
          <strong>{{ descuento }}%</strong><br />
          Total con descuento:
          <strong>${{ totalConDescuento.toFixed(2) }}</strong>
        </div>
      </div>

      <!-- Botones -->
      <div class="flex justify-end gap-3">
        <!-- Botón Editar -->
      
        <button
          v-if="!editable"
          @click="editable = true"
          class="bg-yellow-500 text-white px-4 py-2 rounded-lg hover:bg-yellow-600"
        >
          Editar
        </button>
        <button
          v-if="editable"
          class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 disabled:opacity-50"
          @click="guardarBoleta"
          :disabled="!editable"
        >
          Guardar Boleta
        </button>
        <button
          class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
          @click="exportarPDF"
        >
          Exportar PDF
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getClientPrices, getClient } from '../api/Clientes'
import { getTicket, changeTicket } from '../api/Tickets'

const route = useRoute()
const router = useRouter()
const ticketId = route.params.id
const ticket = ref({})
const cliente = ref({})

const productos = ref([])
const productosSeleccionados = ref([])
const descuento = ref(0)

// Nuevo ref para controlar edición
const editable = ref(false)

function mapItem(item) {
  const productoEncontrado =
    productos.value.find(p => p.product === item.name) || null

  return {
    producto: productoEncontrado,
    cantidad: item.amount,
    price: item.unit_price,
    subtotal: item.subtotal,
  }
}

onMounted(async () => {
  try {
    ticket.value = await getTicket(ticketId)
    const clienteId = ticket.value.client_id
    cliente.value = await getClient(clienteId)

    productos.value = await getClientPrices(clienteId)
    if (Array.isArray(ticket.value.items)) {
      productosSeleccionados.value = ticket.value.items.map(mapItem)
    } else {
      productosSeleccionados.value = []
    }
    descuento.value = Number(ticket.value.discount) || 0
  } catch (error) {
    console.error('Error al cargar precios del cliente:', error)
  }
})

function agregarProducto() {
  productosSeleccionados.value.push({
    producto: '',
    cantidad: 1,
    price: 0,
    subtotal: 0,
  })
}

function eliminarProducto(index) {
  productosSeleccionados.value.splice(index, 1)
}

function actualizarPrecioUnitario(index) {
  const item = productosSeleccionados.value[index]
  item.price = item.producto?.price || 0
  actualizarSubtotal(index)
}

function actualizarSubtotal(index) {
  const item = productosSeleccionados.value[index]
  item.subtotal = item.cantidad * item.price
}

const totalSinDescuento = computed(() =>
  productosSeleccionados.value.reduce((acc, item) => acc + item.subtotal, 0)
)

const totalConDescuento = computed(() =>
  totalSinDescuento.value * (1 - descuento.value / 100)
)

function guardarBoleta() {
  if (productosSeleccionados.value.length === 0) {
    alert('Debes agregar al menos un producto.')
    return
  }

  const boleta = {
    items: productosSeleccionados.value.map((item) => ({
      name: item.producto.product,
      itemPriceListId: item.producto.id,
      amount: item.cantidad,
      unitPrice: item.price,
      subtotal: item.subtotal
    })),
    discount: descuento.value,
    total: totalConDescuento.value,
    subtotal: totalSinDescuento.value
  }

  console.log('Boleta generada:', boleta)
  changeTicket(ticketId, boleta)
  
  // Después de guardar, bloquea de nuevo
  editable.value = false
}

async function exportarPDF() {
  const response = await fetch(`http://localhost:5000/tickets/${ticketId}/pdf`)
  const blob = await response.blob()
  const url = window.URL.createObjectURL(blob)
  const link = document.createElement("a")
  link.href = url
  link.download = `boleta_${ticketId}.pdf`
  link.click()
  window.URL.revokeObjectURL(url)
}
</script>
