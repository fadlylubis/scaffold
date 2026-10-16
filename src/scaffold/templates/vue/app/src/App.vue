<script setup lang="ts">
import { ref } from 'vue'
import AppShell from './components/AppShell.vue'
import UiButton from './components/UiButton.vue'
import UiCard from './components/UiCard.vue'

const page = ref('Overview')
const stats = [
  { label: 'Active jobs', value: '128' },
  { label: 'Success rate', value: '99.2%' },
  { label: 'p95 latency', value: '184 ms' },
]
const rows = [
  { id: 'job-0142', name: 'ingest-orders', status: 'running', updated: '12:04:11' },
  { id: 'job-0141', name: 'train-model', status: 'succeeded', updated: '11:58:40' },
  { id: 'job-0140', name: 'sync-crm', status: 'failed', updated: '11:51:02' },
]
</script>

<template>
  <AppShell v-model="page" title="__PROJECT__" :nav="['Overview', 'Jobs', 'Settings']">
    <div class="stats">
      <UiCard v-for="s in stats" :key="s.label">
        <div class="muted stat-label">{{ s.label }}</div>
        <div class="stat-value mono">{{ s.value }}</div>
      </UiCard>
    </div>

    <UiCard title="Recent jobs">
      <template #actions><UiButton variant="primary">New job</UiButton></template>
      <table class="table">
        <thead>
          <tr><th>ID</th><th>Name</th><th>Status</th><th>Updated</th></tr>
        </thead>
        <tbody>
          <tr v-for="r in rows" :key="r.id">
            <td class="mono">{{ r.id }}</td>
            <td>{{ r.name }}</td>
            <td><span :class="['tag', r.status]">{{ r.status }}</span></td>
            <td class="mono muted">{{ r.updated }}</td>
          </tr>
        </tbody>
      </table>
    </UiCard>
  </AppShell>
</template>

<style scoped>
.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-4);
  margin-bottom: var(--space-4);
}
.stat-label { font-size: var(--text-sm); }
.stat-value { font-size: var(--text-2xl); font-weight: 600; margin-top: var(--space-1); }
.table { width: 100%; border-collapse: collapse; }
.table th {
  text-align: left;
  font-size: var(--text-xs);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--text-muted);
}
.table th, .table td { padding: var(--space-2) var(--space-3); border-bottom: 1px solid var(--border); }
.table tbody tr:hover { background: var(--surface-hover); }
.tag {
  display: inline-block;
  padding: 1px var(--space-2);
  border-radius: 999px;
  font-size: var(--text-xs);
  font-weight: 500;
  border: 1px solid currentColor;
}
.tag.running { color: var(--accent); }
.tag.succeeded { color: var(--success); }
.tag.failed { color: var(--danger); }
</style>
