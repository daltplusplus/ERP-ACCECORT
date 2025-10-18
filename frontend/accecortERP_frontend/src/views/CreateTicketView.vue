<template>
  <div class="max-w-md mx-auto p-6 space-y-6">
    <h1 class="text-2xl font-bold">Seleccionar Cliente</h1>

    <div>
      <label class="block text-sm font-semibold mb-1">Cliente</label>
      <select
        v-model="clienteSeleccionado"
        class="w-full rounded-lg border p-2"
      >
        <option disabled value="">Seleccionar cliente</option>
        <option
          v-for="cliente in clientes"
          :key="cliente.id"
          :value="cliente.id"
        >
          {{ cliente.name }}
        </option>
      </select>
    </div>

    <button
      class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
      :disabled="!clienteSeleccionado"
      @click="irAEditarBoleta"
    >
      Continuar
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getClients } from '../api/Clientes'
import { createTicket } from '../api/Tickets'

const clientes = ref([])
const clienteSeleccionado = ref('')
const router = useRouter()

onMounted(async () => {
  try {
    clientes.value = await getClients()
  } catch (err) {
    console.error('Error cargando clientes', err)
  }
})

async function irAEditarBoleta() {
  if (!clienteSeleccionado.value) return

  try {
    const data = await createTicket(clienteSeleccionado.value)
    router.push(`/editar-ticket/${data.id}`)
  } catch (err) {
    console.error('Error al crear boleta:', err)
  }
}
</script>
