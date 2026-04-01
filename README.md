<p align="center">
  <img src="./docs/public/logo.png" alt="小火炉播客 Logo" width="136" />
</p>

# 小火炉播客 Skills

小火炉播客（XHLFM）Skills 是一个围绕播客创作、分发与传播构建的公开 Skills 仓库。

我们希望把 AI 真正放进播客工作流，而不是只停留在一句口号里。从选题策划、嘉宾准备、录音协作，到转写整理、标题摘要、平台分发、社媒切片和增长复盘，这个仓库会逐步沉淀一套可复用、可协作、可持续迭代的技能体系。

## 愿景

借助 AI，帮助更多播客创作者：

- 更快开始一档节目或一期内容
- 更稳完成从录制到发布的交付流程
- 更广触达听众、社群与分发渠道
- 更持续复盘内容效果并优化下一期创作

## 这个仓库会包含什么

- 围绕播客创作链路沉淀的公开 Skills
- 对应的文档、示例、方法论和协作约定
- 面向小火炉播客与社区贡献者的共建入口
- 一个可直接部署到 Vercel 的 VitePress 文档站

## 本地开发

```bash
pnpm install
pnpm docs:dev
```

生产构建：

```bash
pnpm docs:build
pnpm docs:preview
```

## 目录结构

```text
.
├─ docs/                    VitePress 文档站
├─ docs/.vitepress/         站点配置与主题样式
├─ docs/guide/              项目指南、技能体系、共建与部署文档
├─ docs/public/logo.png     小火炉播客品牌资源
├─ skills/                  后续逐步开放的 Skills 目录
├─ README.md                仓库说明
└─ vercel.json              Vercel 构建配置
```

## 推荐的 Skill 组织方式

建议每个 Skill 独立放在 `skills/<skill-name>/` 下，并至少包含一个 `SKILL.md` 作为入口文档。随着仓库增长，可以继续补充：

- `examples/`：输入输出示例
- `assets/`：模版、提示片段、配套资源
- `references/`：必要的背景说明与链接

## 文档入口

- [项目概览](./docs/guide/index.md)
- [愿景与方法](./docs/guide/vision.md)
- [技能体系](./docs/guide/skills.md)
- [共建方式](./docs/guide/contributing.md)
- [部署到 Vercel](./docs/guide/deploy-vercel.md)

## 部署

仓库已经预置 `vercel.json`，后续导入到 Vercel 后即可按文档中的构建参数直接部署：

- Install Command: `pnpm install`
- Build Command: `pnpm docs:build`
- Output Directory: `docs/.vitepress/dist`

## License

[MIT](./LICENSE)
