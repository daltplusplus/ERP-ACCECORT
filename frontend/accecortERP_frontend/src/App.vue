<template>
  <div class="flex min-h-screen bg-gray-50 text-gray-900 font-sans">
    <aside class="w-64 bg-blue-900 text-white flex flex-col p-6 shadow-lg">
      <h2 class="text-2xl font-bold mb-8 tracking-wide flex items-center gap-2">
        <img src="/logo.png" alt="Logo ACCECORT" class="w-15 h-15 object-contain" />ACCECORT
      </h2>
      <nav class="flex flex-col gap-3">
        <RouterLink to="/crear-ticket" v-slot="{ isActive }">
          <div
            :class="[
              'flex items-center gap-2 rounded px-3 py-2 font-medium transition-colors duration-200',
              isActive ? 'bg-blue-600' : 'hover:bg-blue-600'
            ]"
          >
            <FilePlus class="w-5 h-5" /> Nueva boleta
          </div>
        </RouterLink>
        <RouterLink to="/clientes" v-slot="{ isActive }">
          <div
            :class="[
              'flex items-center gap-2 rounded px-3 py-2 font-medium transition-colors duration-200',
              isActive ? 'bg-blue-600' : 'hover:bg-blue-600'
            ]"
          >
           <Users class="w-5 h-5" /> Clientes
          </div>
        </RouterLink>
        <RouterLink to="/listas" v-slot="{ isActive }">
          <div
            :class="[
              'flex items-center gap-2 rounded px-3 py-2 font-medium transition-colors duration-200',
              isActive ? 'bg-blue-600' : 'hover:bg-blue-600'
            ]"
          >
            <Tag class="w-5 h-5" /> Listas de precios
          </div>
        </RouterLink>
        <RouterLink to="/productos" v-slot="{ isActive }">
          <div
            :class="[
              'flex items-center gap-2 rounded px-3 py-2 font-medium transition-colors duration-200',
              isActive ? 'bg-blue-600' : 'hover:bg-blue-600'
            ]"
          >
            <Package class="w-5 h-5" /> Productos
          </div>
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
import { BarChart, FilePlus, Users, Tag, Package } from 'lucide-vue-next'

</script>
