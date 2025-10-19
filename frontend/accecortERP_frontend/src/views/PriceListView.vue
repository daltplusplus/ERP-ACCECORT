<template>
  <div class="p-6 max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-6">Precios para {{client.name}} </h1>

    <div v-if="loading" class="text-gray-500">Cargando precios...</div>

    <div v-else-if="precios.length === 0" class="text-gray-500">Este cliente no tiene precios asignados.</div>

    <div v-else class="grid gap-4">
      <div
        v-for="(item, index) in precios"
        :key="item.id"
        class="p-4 border rounded-xl bg-white shadow-sm hover:shadow-md transition"
      >
        <div class="flex justify-between items-center">
          <span class="font-medium">{{ item.product }}</span>

          <div class="flex items-center gap-2">
            <input
              v-if="editIndex === index"
              type="number"
              v-model.number="editablePrice"
              class="border rounded px-2 py-1 w-24"
            />
            <span v-else class="text-blue-600 font-semibold">${{ item.price.toFixed(2) }}</span>

            <div>
              <!-- Botón EDITAR -->
              <button
                v-if="editIndex !== index"
                @click="startEditing(index, item.price)"
                class="text-sm px-3 py-1 rounded-full bg-blue-100 text-blue-700 hover:bg-blue-200 transition"
              >
                Editar
              </button>

              <!-- Botones GUARDAR y CANCELAR -->
              <template v-else>
                <button
                  @click="savePrice(index)"
                  class="text-sm px-3 py-1 rounded-full bg-green-100 text-green-700 hover:bg-green-200 transition"
                >
                  Guardar
                </button>
                <button
                  @click="cancelEdit"
                  class="text-sm px-3 py-1 rounded-full bg-red-100 text-red-700 hover:bg-red-200 transition ml-2"
                >
                  Cancelar
                </button>
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getClientPrices, getClient} from '../api/Clientes'
import { updateItemPrice } from '../api/PriceList' 

const route = useRoute()
const clientId = route.params.id
const client = ref('')

const precios = ref([])
const loading = ref(true)

const editIndex = ref(null)
const editablePrice = ref(0)

function startEditing(index, currentPrice) {
  editIndex.value = index
  editablePrice.value = currentPrice
}

function cancelEdit() {
  editIndex.value = null
  editablePrice.value = 0
}

async function savePrice(index) {
  const newPrice = editablePrice.value
  precios.value[index].price = newPrice
  editIndex.value = null
  editablePrice.value = 0

  try {
    await updateItemPrice(precios.value[index].id, newPrice)
  } catch (error) {
    console.error('Error al guardar el precio:', error)
  }
  
}

onMounted(async () => {
  try {
    const data = await getClientPrices(clientId)
    precios.value = data
  } catch (error) {
    console.error('Error al cargar precios:', error)
  } finally {
    loading.value = false
  }

  try {
    const data = await getClient(clientId)
    client.value = data
  } catch (error) {
    console.error('Error al cargar cliente:', error)
  } finally {
    loading.value = false
  }
})
</script>
