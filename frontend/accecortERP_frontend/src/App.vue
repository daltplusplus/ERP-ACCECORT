<template>
  <div class="flex min-h-screen bg-gray-50 text-gray-900 font-sans">
    <aside class="w-64 bg-blue-900 text-white flex flex-col p-6 shadow-lg">
      <h2 class="text-2xl font-bold mb-8 tracking-wide">📊 Panel</h2>
      <nav class="flex flex-col gap-3">
        <RouterLink
          to="/crear-ticket"
          class="rounded px-3 py-2 font-medium transition-colors duration-200 hover:bg-blue-800"
        >
          nueva boleta
        </RouterLink>
        <RouterLink
          to="/clientes"
          class="rounded px-3 py-2 font-medium transition-colors duration-200 hover:bg-blue-800"
        >
          👥 Clientes
        </RouterLink>
        <RouterLink
          to="/productos"
          class="rounded px-3 py-2 font-medium transition-colors duration-200 hover:bg-blue-800"
        >
          🧾 Productos
        </RouterLink>

      </nav>
    </aside>

    <main class="flex-1 p-8 bg-gray-100 overflow-y-auto">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>
