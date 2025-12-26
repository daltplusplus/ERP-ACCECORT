<template>
  <div class="p-6 max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-6">Clientes</h1>

    <!-- Botón para abrir el modal de nuevo cliente -->
    <button
      @click="modalNuevoOpen = true"
      class="mb-6 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
    >
      Nuevo Cliente
    </button>

    <!-- Modal para agregar nuevo cliente -->
    <div
      v-if="modalNuevoOpen"
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
          
          <select
            v-model="nuevoClienteLista"
            
            class="w-full rounded-lg border p-2"
            
          >
            <option disabled value="">Seleccionar lista de precios</option>
            <option
              v-for="lista in listasPrecio"
              :key="lista.id"
              :value="lista.id"
            >
              {{ lista.name }}
            </option>
          </select>
          

          <div class="flex justify-end gap-3">
            <button
              type="button"
              @click="modalNuevoOpen = false; nuevoClienteNombre = ''"
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

    <!-- Modal para editar cliente -->
    <div
      v-if="modalEditarOpen"
      class="fixed inset-0 bg-black/40 flex justify-center items-center z-50"
    >
      <div class="bg-white rounded-lg p-6 w-full max-w-md shadow-lg relative">
        <h2 class="text-xl font-semibold mb-4">Editar Cliente</h2>

        <form @submit.prevent="guardarEdicionCliente">
          <input
            v-model="clienteEditado.name"
            type="text"
            placeholder="Nombre"
            class="border rounded px-3 py-2 w-full mb-3"
            required
            autofocus
          />
          <input
            v-model="clienteEditado.phone"
            type="text"
            placeholder="Número"
            class="border rounded px-3 py-2 w-full mb-3"
          />
          <input
            v-model="clienteEditado.adress"
            type="text"
            placeholder="Dirección"
            class="border rounded px-3 py-2 w-full mb-3"
          />
          <select
            v-model="clienteEditado.pricelist_id"
            
            class="w-full rounded-lg border p-2"
            
          >
            <option disabled value="">Seleccionar lista de precios</option>
            <option
              v-for="lista in listasPrecio"
              :key="lista.id"
              :value="lista.id"
            >
              {{ lista.name }}
            </option>
          </select>
          <div class="flex justify-end gap-3">
            <button
              type="button"
              @click="modalEditarOpen = false; clienteEditado = {}"
              class="px-4 py-2 rounded border border-gray-300 hover:bg-gray-100"
            >
              Cancelar
            </button>
            <button
              type="submit"
              class="bg-green-800 text-white px-4 py-2 rounded hover:bg-green-900 transition"
            >
              Guardar
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
          <!--p class="text-sm text-gray-500">ID: {{ cliente.id }}</p-->
          <p class="text-sm text-gray-500">Número: {{ cliente.phone || '---' }}</p>
          <p class="text-sm text-gray-500">Dirección: {{ cliente.adress || '---' }}</p>
          <p class="text-sm text-gray-500">Lista: {{ listasPrecio.filter(function(list){ return list.id == cliente.pricelist_id}).map(function(list){return list.name}).at(0) || '---' }}</p>
        </div>

        <div class="flex gap-2">
          <!--RouterLink
            :to="`/clientes/${cliente.id}/ticket`"
            class="bg-green-700 text-white px-4 py-2 rounded-lg hover:bg-green-900"
          >
            Boletas
          </RouterLink-->
          <!-- Botón editar -->
          <button
            @click="abrirEditarCliente(cliente)"
            class="bg-yellow-600 text-white px-4 py-2 rounded-lg hover:bg-yellow-800"
          >
            Editar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { ref, onMounted } from 'vue'
import { getClients, createClient, updateClient } from '../api/Clientes'
import {getPriceLists} from '../api/PriceList'

const clientes = ref([])
const listasPrecio = ref([])
const modalNuevoOpen = ref(false)
const modalEditarOpen = ref(false)
const nuevoClienteNombre = ref('')
const clienteEditado = ref({})
const nuevoClienteLista = ref('')

onMounted(async () => {
  try {
    clientes.value = await getClients()
  } catch (err) {
    console.error('Error cargando clientes:', err)
  }

  try {
    listasPrecio.value = await getPriceLists()
  } catch (err) {
    console.error('Error cargando listas de precios:', err)
  }
})

async function addCliente() {
  if (!nuevoClienteNombre.value.trim()) return


  try {
    const clienteCreado = await createClient({ name: nuevoClienteNombre.value.trim(), pricelist_id: nuevoClienteLista.value })
    clientes.value.push(clienteCreado)
    nuevoClienteNombre.value = ''
    nuevoClienteLista.value = ''
    modalNuevoOpen.value = false
  } catch (err) {
    console.error('Error creando cliente:', err)
  }
}

// Abrir modal de edición
function abrirEditarCliente(cliente) {
  clienteEditado.value = { ...cliente } // copia para editar
  modalEditarOpen.value = true
}

// Guardar cambios de edición
async function guardarEdicionCliente() {
  try {
    console.log(clienteEditado.value)
    const actualizado = await updateClient(clienteEditado.value.id, clienteEditado.value)
    // Actualiza la lista local
    const index = clientes.value.findIndex(c => c.id === actualizado.id)
    if (index !== -1) clientes.value[index] = actualizado
    console.log(actualizado)
    modalEditarOpen.value = false
    clienteEditado.value = {}
  } catch (err) {
    console.error('Error actualizando cliente:', err)
  }
}
</script>
