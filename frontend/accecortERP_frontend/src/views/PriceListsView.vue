<template>
  <div class="p-6 max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-6">Listas de Precios </h1>

    <div v-if="loading" class="text-gray-500">Cargando precios...</div>

    <div v-else-if="listasPrecios.length === 0" class="text-gray-500">no hay listas aun.</div>

    <button
      @click="modalNuevoOpen = true"
      class="mb-6 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
    >
      Nueva Lista
    </button>

   
    <div
      v-if="modalNuevoOpen"
      class="fixed inset-0 bg-black/40 flex justify-center items-center z-50"
    >
      <div class="bg-white rounded-lg p-6 w-full max-w-md shadow-lg relative">
        <h2 class="text-xl font-semibold mb-4">Agregar nueva lista</h2>

        <form @submit.prevent="addLista">
          <input
            v-model="nuevaListaNombre"
            type="text"
            placeholder="Nombre de la lista"
            class="border rounded px-3 py-2 w-full mb-4"
            required
            autofocus
          />

          <div class="flex justify-end gap-3">
            <button
              type="button"
              @click="modalNuevoOpen = false; nuevaListaNombre = ''"
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

    <div v-else class="grid gap-4">
      <div
        v-for="(item, index) in listasPrecios"
        :key="item.id"
        class="p-4 border rounded-xl bg-white shadow-sm hover:shadow-md transition"
      >
        <div class="flex justify-between items-center">
          <span class="font-medium">{{ item.name }}</span>
          <div class="flex gap-2">
          <RouterLink
            :to="`/listas/${item.id}`"
            class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
          >
            ver
          </RouterLink>
          
        </div>
          
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getPriceLists, createPricelist} from '../api/PriceList' 

const route = useRoute()


const listasPrecios = ref([])
const loading = ref(true)
const modalNuevoOpen = ref(false)
const nuevaListaNombre = ref('')

async function addLista() {
  if (!nuevaListaNombre.value.trim()) return


  try {
    const clienteCreado = await createPricelist({ name: nuevaListaNombre.value.trim()})
    listasPrecios.value.push(clienteCreado)
    nuevaListaNombre.value = ''
    modalNuevoOpen.value = false
  } catch (err) {
    console.error('Error creando lista:', err)
  }
}

onMounted(async () => {
  try {
    const data = await getPriceLists()
    listasPrecios.value = data
  } catch (error) {
    console.error('Error al cargar precios:', error)
  } finally {
    loading.value = false
  }

})
</script>
