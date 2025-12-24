<template>
  <div class="p-6 max-w-5xl mx-auto">
    <h1 class="text-3xl font-bold">Estadisticas</h1>
      <p class="text-gray-500 mb-6">
        <strong>{{ currentMonth }}</strong>
      </p>

    <!-- KPIs -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <!-- Sumatoria -->
      <div class="bg-white p-4 rounded shadow-sm">
        <h2 class="text-sm text-gray-500 mb-1">total facturado</h2>
        <p class="text-2xl font-bold">
          {{ formatCurrency(stats.total) }}
        </p>
      </div>
      <!-- Venta promedio -->
      <div class="bg-white p-4 rounded shadow-sm">
        <h2 class="text-sm text-gray-500 mb-1">Venta promedio</h2>
        <p class="text-2xl font-bold">
          {{ formatCurrency(stats.average) }}
        </p>
      </div>

      <!-- Total de ventas -->
      <div class="bg-white p-4 rounded shadow-sm">
        <h2 class="text-sm text-gray-500 mb-1">cantidad ventas</h2>
        <p class="text-2xl font-bold">
          {{ stats.ticketsAmount }}
        </p>
      </div>

      <!-- Crecimiento último mes -->
      <div class="bg-white p-4 rounded shadow-sm">
        <h2 class="text-sm text-gray-500 mb-1">Crecimiento último mes</h2>
        <p
          class="text-2xl font-bold"
          :class="stats.grow >= 0 ? 'text-green-600' : 'text-red-600'"
        >
          {{ stats.grow }}%
        </p>
      </div>
    </div>

    <!-- Top clientes -->
    <div class="bg-white p-4 rounded shadow-sm">
      <h2 class="text-lg font-semibold mb-4">Top 5 clientes</h2>

      <div v-if="stats.top_clients.length === 0" class="text-gray-500">
        No hay datos todavía
      </div>

      <table v-else class="w-full border-collapse">
        <thead>
          <tr class="border-b">
            <th class="text-left py-2 text-sm text-gray-500">#</th>
            <th class="text-left py-2 text-sm text-gray-500">Cliente</th>
            <th class="text-right py-2 text-sm text-gray-500">Total facturado</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(cliente, index) in stats.top_clients"
            :key="cliente.id || cliente.name"
            class="border-b last:border-b-0"
          >
            <td class="py-2">{{ index + 1 }}</td>
            <td class="py-2">{{ cliente.name }}</td>
            <td class="py-2 text-right font-medium">
              {{ formatCurrency(cliente.total) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed} from 'vue'
import { getDashboard } from '../api/Dashboard'

const stats = ref({
  average: 0,
  total: 0,
  ticketsAmount: 0,
  grow: 0,
  top_clients: []
})

onMounted(async () => {
  try {
    const data = await getDashboard()
    stats.value = data
  } catch (error) {
    console.error('Error cargando dashboard:', error)
  }
})

function formatCurrency(value) {
  return new Intl.NumberFormat('es-AR', {
    style: 'currency',
    currency: 'ARS'
  }).format(value)
}

const currentMonth = computed(() => {
  const now = new Date()
  return now.toLocaleDateString('es-AR', {
    month: 'long',
    year: 'numeric'
  })
})

</script>
