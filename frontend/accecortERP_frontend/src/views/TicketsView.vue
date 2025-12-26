<!-- src/views/TicketsView.vue -->
<template>
  <div class="p-6 max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-6">Ventas</h1>

    <!-- Filtros -->
    <div class="flex flex-col md:flex-row gap-4 mb-6">
      <RouterLink
        to="/crear-ticket"
        
        class="bg-blue-700 text-white px-4 py-2 rounded-lg hover:bg-green-900"
      >
        Nueva boleta
      </RouterLink>
      <!-- Filtro por mes -->
      <select
        v-model="selectedMonth"
        class="px-3 py-2 border rounded-lg"
      >
        <option
          v-for="month in months"
          :key="month.value"
          :value="month.value"
        >
          {{ month.label }}
        </option>
      </select>

      <!-- Filtro por cliente -->
      <select
        v-model="selectedClient"
        class="px-3 py-2 border rounded-lg"
      >
        <option value="all">Todos los clientes</option>
        <option
          v-for="client in clients"
          :key="client.id"
          :value="client.id"
        >
          {{ client.name }}
        </option>
      </select>
    </div>


    <!-- Lista de tickets -->
    <div class="grid gap-4">
      <div
        v-for="ticket in tickets"
        :key="ticket.id"
        class="flex justify-between items-center p-4 border rounded-xl shadow-sm bg-white hover:shadow-md transition"
      >
        <div>
          <h2 class="text-x font-semibold">{{ ticket.date }}</h2>
          <p class="text-x text-gray-500">{{ ticket.client_name }}</p>
          <p class="text-sm text-gray-500">ID: {{ ticket.id }}</p>
          
        </div>

        <div class="flex items-center gap-3">
          <select
            v-model="ticket.state"
            @change="updateTicketState(ticket)"
            :class="[ 
              'px-3 py-1 rounded-lg font-semibold border focus:ring focus:ring-opacity-50 transition',
              {
                'bg-blue-100 text-blue-800 border-blue-300 focus:ring-blue-200': ticket.state === 'ISSUED',
                'bg-green-100 text-green-800 border-green-300 focus:ring-green-200': ticket.state === 'PAID',
                'bg-red-100 text-red-800 border-red-300 focus:ring-red-200': ticket.state === 'CANCELED',
              }
            ]"
          >
            <option
              v-for="estado in estadosTicket"
              :key="estado.value"
              :value="estado.value"
            >
              {{ estado.label }}
            </option>
          </select>

          <RouterLink
            :to="`/editar-ticket/${ticket.id}`"
            class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
          >
            Ver
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { RouterLink } from 'vue-router'
import { getTickets, changeTicket } from '../api/Tickets'
import { getClients } from '../api/Clientes'

const tickets = ref([])
const clients = ref([])

/* ======================
   Meses disponibles
====================== */

const months = ref([])

const buildMonths = (count = 12) => {
  const result = []
  const now = new Date()

  for (let i = 0; i < count; i++) {
    const date = new Date(now.getFullYear(), now.getMonth() - i, 1)

    result.push({
      value: date.toISOString().slice(0, 7), // YYYY-MM
      label: date.toLocaleDateString('es-AR', {
        month: 'long',
        year: 'numeric'
      }).replace(/^./, c => c.toUpperCase())
    })
  }

  months.value = result
}

/* ======================
   Filtros
====================== */

const selectedMonth = ref(null)
const selectedClient = ref('all')

/* ======================
   Estados
====================== */

const estadosTicket = [
  { value: 'ISSUED', label: 'Emitido' },
  { value: 'PAID', label: 'Pagado' },
  { value: 'CANCELED', label: 'Cancelado' }
]

/* ======================
   Carga de tickets
====================== */

const loadTickets = async () => {
  if (!selectedMonth.value) return

  try {
    const clientId =
      selectedClient.value === 'all'
        ? null
        : Number(selectedClient.value)

    tickets.value = await getTickets(
      selectedMonth.value,
      clientId
    )

    tickets.value.forEach(t => {
      if (t.state?.startsWith('TicketState.')) {
        t.state = t.state.replace('TicketState.', '')
      }
    })
  } catch (err) {
    console.error('Error cargando tickets:', err)
  }
}

/* ======================
   Init
====================== */

onMounted(async () => {
  buildMonths()
  selectedMonth.value = months.value[0].value

  clients.value = await getClients()
  await loadTickets()
})


/* ======================
   Watch filtros
====================== */

const updateTicketState = async (ticket) => {
  try {
    await changeTicket(ticket.id, { state: ticket.state })
    console.log(`Estado del ticket ${ticket.id} cambiado a ${ticket.state}`)
  } catch (err) {
    console.error('Error actualizando estado:', err)
    alert('No se pudo actualizar el estado del ticket')
  }
}

watch([selectedMonth, selectedClient], loadTickets)
</script>

