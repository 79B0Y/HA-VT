// frontend/utils/api.ts

// 示例：统一封装 fetch 请求（可用于后期错误处理、baseURL 管理等）

export async function fetchJson<T = any>(url: string): Promise<T> {
  const res = await fetch(url)
  if (!res.ok) throw new Error(`请求失败: ${res.status}`)
  return res.json()
}

export async function fetchText(url: string): Promise<string> {
  const res = await fetch(url)
  if (!res.ok) throw new Error(`请求失败: ${res.status}`)
  return res.text()
}
