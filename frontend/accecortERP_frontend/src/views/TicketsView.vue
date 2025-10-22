<!-- src/views/TicketsView.vue -->
<template>
  <div class="p-6 max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-6">Tickets</h1>

    <!-- Lista de tickets -->
    <div class="grid gap-4">
      <div
        v-for="ticket in tickets"
        :key="ticket.id"
        class="flex justify-between items-center p-4 border rounded-xl shadow-sm bg-white hover:shadow-md transition"
      >
        <div>
          <h2 class="text-xl font-semibold">{{ ticket.date }}</h2>
          <p class="text-sm text-gray-500">ID: {{ ticket.id }}</p>
        </div>

        <div class="flex items-center gap-3">
          <!-- Desplegable de estado con color dinámico -->
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
import { ref, onMounted } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { getClientTickets, changeTicket } from '../api/Tickets'

const tickets = ref([])
const route = useRoute()
const clientId = route.params.id

// Lista con traducción visible
const estadosTicket = ref([
  { value: 'ISSUED', label: 'Emitido' },
  { value: 'PAID', label: 'Pagado' },
  { value: 'CANCELED', label: 'Cancelado' }
])

onMounted(async () => {
  try {
    tickets.value = await getClientTickets(clientId)
    // limpiar el prefijo "TicketState." si el backend lo envía así
    tickets.value.forEach(t => {
      if (t.state?.startsWith("TicketState.")) {
        t.state = t.state.replace("TicketState.", "")
      }
    })
  } catch (err) {
    console.error('Error cargando tickets:', err)
  }
})

// Cambiar el estado del ticket
const updateTicketState = async (ticket) => {
  try {
    await changeTicket(ticket.id, { state: ticket.state })
    console.log(`Estado del ticket ${ticket.id} cambiado a ${ticket.state}`)
  } catch (err) {
    console.error('Error actualizando estado:', err)
    alert('No se pudo actualizar el estado del ticket')
  }
}
</script>
