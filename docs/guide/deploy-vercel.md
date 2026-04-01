# 部署到 Vercel

这个仓库已经预置好了 VitePress 和 `vercel.json`，后续部署到 Vercel 时只需要确认项目设置即可。

## 本地先验证

```bash
pnpm install
pnpm docs:build
pnpm docs:preview
```

## 在 Vercel 中的推荐设置

- Install Command: `pnpm install`
- Build Command: `pnpm docs:build`
- Output Directory: `docs/.vitepress/dist`

## 部署步骤

1. 将仓库导入 Vercel。
2. 如果框架预设没有自动识别到 VitePress，可以选择 `Other`。
3. 确认安装、构建和输出目录与上面的参数一致。
4. 点击 Deploy，等待静态站点构建完成。

## 后续可做的事

- 绑定正式域名
- 配置仓库自动预览部署
- 为文档站补充 Open Graph 图和更多品牌素材
- 随着 Skill 增长继续扩展侧边栏和信息架构
