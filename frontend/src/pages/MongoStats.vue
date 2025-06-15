<template>
  <div>
    <h2 class="text-2xl font-bold mb-4">MongoDB 状态</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div class="bg-white shadow rounded-xl p-4">
        <p class="text-gray-600 text-sm">数据库连接</p>
        <p class="text-xl font-semibold">{{ status.connected ? '已连接' : '未连接' }}</p>
      </div>
      <div class="bg-white shadow rounded-xl p-4">
        <p class="text-gray-600 text-sm">数据库名</p>
        <p class="text-xl font-semibold">{{ status.db_name }}</p>
      </div>
      <div class="bg-white shadow rounded-xl p-4">
        <p class="text-gray-600 text-sm">集合统计</p>
        <ul class="list-disc ml-4">
          <li v-for="(count, name) in status.collections" :key="name">
            {{ name }}：{{ count }} 条
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const status = ref({
  connected: false,
  db_name: '-',
  collections: {}
})

onMounted(async () => {
  try {
    const res = await fetch('/api/mongo/stats')
    status.value = await res.json()
  } catch (e) {
    status.value.connected = false
  }
})
</script>

<style scoped>
</style>
