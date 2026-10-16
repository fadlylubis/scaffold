<script setup lang="ts">
withDefaults(defineProps<{ variant?: 'primary' | 'default' | 'minimal'; type?: 'button' | 'submit' }>(), {
  variant: 'default',
  type: 'button',
})
</script>

<template>
  <button :type="type" :class="['btn', `btn-${variant}`]"><slot /></button>
</template>

<style scoped>
.btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  height: 30px;
  padding: 0 var(--space-3);
  font: inherit;
  font-weight: 500;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background: var(--surface);
  color: var(--text);
  cursor: pointer;
  transition: background var(--dur) var(--ease), transform var(--dur) var(--ease);
}
.btn:hover { background: var(--surface-hover); }
.btn:active { transform: scale(0.98); }
.btn:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-primary { background: var(--accent); border-color: transparent; color: var(--accent-text); }
.btn-primary:hover { background: var(--accent-hover); }
.btn-minimal { background: transparent; border-color: transparent; }
</style>
