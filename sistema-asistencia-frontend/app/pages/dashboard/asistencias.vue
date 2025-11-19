<template>
  <div>
    <div class="container">
      <h1 class="title">Asistencias</h1>
      <p class="subtitle">Registros de asistencia (próximamente)</p>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'dashboard',
  middleware: 'auth'
})
</script>