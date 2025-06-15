<template>
  <div>
    <h2 class="text-2xl font-bold mb-4">设备总览</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div
        v-for="device in devices"
        :key="device.did"
        class="p-4 bg-white shadow rounded-2xl border border-gray-200"
      >
        <p class="text-sm text-gray-500">{{ device.device_type }}</p>
        <p class="text-lg font-semibold">{{ device.did }}</p>
        <pre class="text-xs bg-gray-100 p-2 rounded mt-2">{{ device.data }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const devices = ref<any[]>([])

onMounted(async () => {
  try {
    const res = await fetch('/api/devices')
    devices.value = await res.json()
  } catch (e) {
    console.error('获取设备失败', e)
  }
})
</script>

<style scoped>
</style>
