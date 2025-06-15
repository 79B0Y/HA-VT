<template>
  <div>
    <h2 class="text-2xl font-bold mb-4">运行日志</h2>
    <div class="bg-black text-white text-sm font-mono p-4 rounded-xl h-[500px] overflow-y-scroll">
      <div v-for="(line, index) in logs" :key="index">
        {{ line }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const logs = ref<string[]>([])

onMounted(async () => {
  try {
    const res = await fetch('/api/logs')
    const text = await res.text()
    logs.value = text.split('\n').filter(line => line.trim() !== '')
  } catch (e) {
    logs.value = ['无法加载日志']
  }
})
</script>

<style scoped>
</style>
