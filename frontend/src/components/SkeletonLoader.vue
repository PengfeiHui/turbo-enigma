<template>
  <div class="skeleton-card">
    <div class="skeleton-line skeleton-title"></div>
    <div class="skeleton-line skeleton-text"></div>
    <div class="skeleton-line skeleton-text short"></div>
  </div>
</template>

<style scoped>
.skeleton-card {
  padding: 20px;
  background: white;
  border-radius: 12px;
  animation: pulse 1.5s ease-in-out infinite;
}

.skeleton-line {
  height: 16px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  border-radius: 4px;
  margin-bottom: 12px;
  animation: shimmer 1.5s ease-in-out infinite;
}

.skeleton-title {
  height: 24px;
  width: 60%;
}

.skeleton-text {
  width: 100%;
}

.skeleton-text.short {
  width: 80%;
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.8;
  }
}
</style>
