<script setup lang="ts">
import { ref } from 'vue'
import UiButton from './UiButton.vue'

defineProps<{ title: string; nav: string[] }>()
const active = defineModel<string>({ required: true })

const dark = ref(window.matchMedia('(prefers-color-scheme: dark)').matches)
function toggleTheme() {
  dark.value = !dark.value
  document.documentElement.dataset.theme = dark.value ? 'dark' : 'light'
}
</script>

<template>
  <div class="shell">
    <aside class="sidebar">
      <div class="brand">{{ title }}</div>
      <nav aria-label="Main">
        <a
          v-for="item in nav"
          :key="item"
          href="#"
          :class="['nav-item', { active: item === active }]"
          :aria-current="item === active ? 'page' : undefined"
          @click.prevent="active = item"
        >{{ item }}</a>
      </nav>
    </aside>
    <div class="main">
      <header class="topbar">
        <h1>{{ active }}</h1>
        <UiButton variant="minimal" :aria-label="dark ? 'Switch to light theme' : 'Switch to dark theme'" @click="toggleTheme">
          {{ dark ? '☀︎' : '☾' }}
        </UiButton>
      </header>
      <main class="content"><slot /></main>
    </div>
  </div>
</template>

<style scoped>
.shell { display: grid; grid-template-columns: 220px 1fr; height: 100%; }
.sidebar {
  border-right: 1px solid var(--border);
  background: var(--surface);
  padding: var(--space-4) var(--space-3);
}
.brand { font-weight: 600; font-size: var(--text-lg); padding: 0 var(--space-2) var(--space-4); }
.nav-item {
  display: block;
  padding: 6px var(--space-2);
  border-radius: var(--radius-sm);
  color: var(--text-muted);
  text-decoration: none;
  transition: background var(--dur) var(--ease), color var(--dur) var(--ease);
}
.nav-item:hover { background: var(--surface-hover); color: var(--text); }
.nav-item.active { background: var(--surface-hover); color: var(--text); font-weight: 500; }
.main { display: flex; flex-direction: column; min-width: 0; }
.topbar {
  position: sticky;
  top: 0;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 52px;
  padding: 0 var(--space-5);
  border-bottom: 1px solid var(--border);
  background: var(--surface-raised);
  backdrop-filter: saturate(180%) blur(20px);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
}
.topbar h1 { font-size: var(--text-lg); }
.content { padding: var(--space-5); overflow: auto; }

@media (max-width: 720px) {
  .shell { grid-template-columns: 1fr; }
  .sidebar { display: none; }
  .topbar, .content { padding-left: var(--space-4); padding-right: var(--space-4); }
}
</style>
