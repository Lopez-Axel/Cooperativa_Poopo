<template>
  <div class="dashboard-layout">
    <DashboardHeader />
    
    <main class="dashboard-content">
      <slot />
    </main>
    
    <DashboardFooter />
  </div>
</template>

<script setup>
// Layout protegido por autenticación
definePageMeta({
  middleware: 'auth'
})
</script>

<style scoped>
.dashboard-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.dashboard-content {
  flex: 1;
  padding: 2rem 1rem;
  background: white;
}

@media screen and (min-width: 769px) {
  .dashboard-content {
    padding: 2.5rem;
  }
}
</style>