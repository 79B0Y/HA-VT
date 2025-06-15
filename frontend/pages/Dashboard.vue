<template>
  <div class="grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
    <div class="p-4 bg-white rounded-2xl shadow">
      <p class="text-lg font-semibold">设备总数</p>
      <p class="text-3xl mt-2">--</p>
    </div>
    <div class="p-4 bg-white rounded-2xl shadow">
      <p class="text-lg font-semibold">MQTT 状态</p>
      <p class="mt-2">未连接</p>
    </div>
    <div class="p-4 bg-white rounded-2xl shadow">
      <p class="text-lg font-semibold">MongoDB 状态</p>
      <p class="mt-2">--</p>
    </div>
  </div>
</template>

<script setup lang="ts">
// 后续可通过 websocket 或 API 获取状态动态更新
</script>

<style scoped>
</style>
