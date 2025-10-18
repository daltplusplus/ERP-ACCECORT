<!-- src/views/ClientesView.vue -->
<template>
  <div class="p-6 max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-6">Clientes</h1>

    <!-- Botón para abrir el modal -->
    <button
      @click="modalOpen = true"
      class="mb-6 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
    >
      Nuevo Cliente
    </button>

    <!-- Modal popup -->
    <div
      v-if="modalOpen"
      class="fixed inset-0 bg-black/40 flex justify-center items-center z-50"
    >
      <div class="bg-white rounded-lg p-6 w-full max-w-md shadow-lg relative">
        <h2 class="text-xl font-semibold mb-4">Agregar nuevo cliente</h2>

        <form @submit.prevent="addCliente">
          <input
            v-model="nuevoClienteNombre"
            type="text"
            placeholder="Nombre del cliente"
            class="border rounded px-3 py-2 w-full mb-4"
            required
            autofocus
          />

          <div class="flex justify-end gap-3">
            <button
              type="button"
              @click="modalOpen = false; nuevoClienteNombre = ''"
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

    <!-- Lista de clientes -->
    <div class="grid gap-4">
      <div
        v-for="cliente in clientes"
        :key="cliente.id"
        class="flex justify-between items-center p-4 border rounded-xl shadow-sm bg-white hover:shadow-md transition"
      >
        <div>
          <h2 class="text-xl font-semibold">{{ cliente.name }}</h2>
          <p class="text-sm text-gray-500">ID: {{ cliente.id }}</p>
        </div>

        <div class="flex gap-2">
          <RouterLink
            :to="`/clientes/${cliente.id}/lista`"
            class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
          >
            Lista de Precios
          </RouterLink>
          <RouterLink
            :to="`/clientes/${cliente.id}/ticket`"
            class="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600"
          >
            Boletas
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { ref, onMounted } from 'vue'
import { getClients, createClient } from '../api/Clientes'

const clientes = ref([])
const modalOpen = ref(false)
const nuevoClienteNombre = ref('')

onMounted(async () => {
  try {
    clientes.value = await getClients()
  } catch (err) {
    console.error('Error cargando clientes:', err)
  }
})

async function addCliente() {
  if (!nuevoClienteNombre.value.trim()) return

  try {
    const clienteCreado = await createClient({ name: nuevoClienteNombre.value.trim() })
    clientes.value.push(clienteCreado)
    nuevoClienteNombre.value = ''
    modalOpen.value = false
  } catch (err) {
    console.error('Error creando cliente:', err)
  }
}
</script>
