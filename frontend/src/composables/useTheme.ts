import { ref, watch } from 'vue'

export type Theme = 'light' | 'dark' | 'auto'
export type FontSize = 'small' | 'medium' | 'large'

const theme = ref<Theme>('light')
const fontSize = ref<FontSize>('medium')

// 加载主题设置
export const loadTheme = () => {
  const savedTheme = localStorage.getItem('theme') as Theme
  const savedFontSize = localStorage.getItem('fontSize') as FontSize

  if (savedTheme) {
    theme.value = savedTheme
    applyTheme(savedTheme)
  }

  if (savedFontSize) {
    fontSize.value = savedFontSize
    applyFontSize(savedFontSize)
  }
}

// 应用主题
const applyTheme = (themeValue: Theme) => {
  const html = document.documentElement

  if (themeValue === 'auto') {
    const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    html.setAttribute('data-theme', isDark ? 'dark' : 'light')
  } else {
    html.setAttribute('data-theme', themeValue)
  }
}

// 应用字体大小
const applyFontSize = (size: FontSize) => {
  const html = document.documentElement
  html.setAttribute('data-font-size', size)

  const fontSizeMap = {
    small: '14px',
    medium: '16px',
    large: '18px'
  }

  html.style.fontSize = fontSizeMap[size]
}

// 设置主题
export const setTheme = (newTheme: Theme) => {
  theme.value = newTheme
  localStorage.setItem('theme', newTheme)
  applyTheme(newTheme)
}

// 设置字体大小
export const setFontSize = (newSize: FontSize) => {
  fontSize.value = newSize
  localStorage.setItem('fontSize', newSize)
  applyFontSize(newSize)
}

// 监听系统主题变化
if (window.matchMedia) {
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (theme.value === 'auto') {
      applyTheme('auto')
    }
  })
}

export const useTheme = () => {
  return {
    theme,
    fontSize,
    setTheme,
    setFontSize,
    loadTheme
  }
}
