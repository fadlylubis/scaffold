<script setup lang="ts">
defineProps<{ title?: string }>()
</script>

<template>
  <section class="card">
    <header v-if="title || $slots.actions" class="card-header">
      <h2>{{ title }}</h2>
      <slot name="actions" />
    </header>
    <slot />
  </section>
</template>

<style scoped>
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow);
  padding: var(--space-4);
}
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-3);
}
.card-header h2 { font-size: var(--text-lg); }
</style>
