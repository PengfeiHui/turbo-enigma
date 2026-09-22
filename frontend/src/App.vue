<template>
  <router-view />
</template>

<script setup lang="ts">
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --bg-color: #ffffff;
  --text-color: #333333;
  --border-color: #e5e5e5;
  --sidebar-bg: #ffffff;
  --message-bg: #f5f5f5;
}

:root[data-theme="dark"] {
  --bg-color: #1a1a1a;
  --text-color: #e5e5e5;
  --border-color: #333333;
  --sidebar-bg: #252525;
  --message-bg: #2a2a2a;
}

html {
  font-size: 16px;
}

html[data-font-size="small"] {
  font-size: 14px;
}

html[data-font-size="large"] {
  font-size: 18px;
}

#app {
  height: 100vh;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background: var(--bg-color);
  color: var(--text-color);
}

body {
  margin: 0;
  padding: 0;
  background: var(--bg-color);
  color: var(--text-color);
}
</style>
