import { defineConfig } from 'vitepress'

export default defineConfig({
  lang: 'zh-CN',
  title: '小火炉播客 Skills',
  description: '借助 AI 助力播客创作和传播。',
  cleanUrls: true,
  lastUpdated: true,
  head: [
    ['link', { rel: 'icon', type: 'image/x-icon', href: '/favicon/favicon.ico' }],
    ['link', { rel: 'icon', type: 'image/png', sizes: '16x16', href: '/favicon/favicon-16x16.png' }],
    ['link', { rel: 'icon', type: 'image/png', sizes: '32x32', href: '/favicon/favicon-32x32.png' }],
    ['link', { rel: 'apple-touch-icon', sizes: '180x180', href: '/favicon/apple-touch-icon.png' }],
    ['link', { rel: 'manifest', href: '/favicon/site.webmanifest' }],
    ['meta', { name: 'theme-color', content: '#ff4d2e' }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:title', content: '小火炉播客 Skills' }],
    ['meta', { property: 'og:description', content: '借助 AI 助力播客创作和传播。' }],
    ['meta', { property: 'og:image', content: '/logo.png' }]
  ],
  themeConfig: {
    logo: '/logo.svg',
    siteTitle: '小火炉播客 Skills',
    nav: [
      { text: '首页', link: '/' },
      {
        text: 'Skills',
        items: [
          { text: 'Skills 总览', link: '/skills/' },
          { text: '中文播客雷达', link: '/skills/podcast-radar-cn' }
        ]
      },
      { text: '指南', link: '/guide/' },
      { text: '愿景', link: '/guide/vision' },
      { text: '共建', link: '/guide/contributing' }
    ],
    sidebar: {
      '/guide/': [
        {
          text: '开始',
          items: [
            { text: '项目概览', link: '/guide/' },
            { text: '愿景与方法', link: '/guide/vision' },
            { text: '技能体系', link: '/guide/skills' },
            { text: '共建方式', link: '/guide/contributing' },
            { text: '测试与验证', link: '/guide/testing' },
            { text: '部署到 Vercel', link: '/guide/deploy-vercel' }
          ]
        }
      ],
      '/skills/': [
        {
          text: 'Skill 文档',
          items: [
            { text: '总览', link: '/skills/' },
            { text: '中文播客雷达', link: '/skills/podcast-radar-cn' },
            { text: '使用剧本', link: '/skills/podcast-radar-cn-playbook' }
          ]
        }
      ]
    },
    search: {
      provider: 'local'
    },
    outline: {
      level: [2, 3],
      label: '本页导航'
    },
    docFooter: {
      prev: '上一页',
      next: '下一页'
    },
    lastUpdated: {
      text: '最近更新于',
      formatOptions: {
        dateStyle: 'medium',
        timeStyle: 'short',
        forceLocale: true
      }
    },
    footer: {
      message: '以 AI 为火，以播客为炉。',
      copyright: 'Copyright © 2026 小火炉播客'
    }
  }
})
