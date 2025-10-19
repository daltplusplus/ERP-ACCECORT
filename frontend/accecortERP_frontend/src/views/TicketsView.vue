<!-- src/views/TicketsView.vue -->
<template>
  <div class="p-6 max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-6">Tickets</h1>

    <!-- Botón para abrir el modal ->
    <button
      @click="modalOpen = true"
      class="mb-6 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
    >
      Nuevo Ticket
    </button> -->

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

        <div class="flex gap-2">
          <RouterLink
            :to="`/editar-ticket/${ticket.id}`"
            class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
          >
            ver
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { getClientTickets } from '../api/Tickets'

const tickets = ref([])
const route = useRoute()
const clientId = route.params.id

onMounted(async () => {
  try {
    tickets.value = await getClientTickets(clientId)
  } catch (err) {
    console.error('Error cargando tickets:', err)
  }
})

</script>
