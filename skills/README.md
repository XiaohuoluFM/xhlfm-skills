# Skills Directory

这里会逐步收录小火炉播客相关的公开 Skills。

## 当前可用

### `podcast-radar-cn`

展示名：`中文播客雷达`

用途：

- 快速发现当下热门与新锐的中文播客
- 为播客创作者寻找可对标节目与热门样本
- 为策展、推荐和二创分发整理节目与单集线索

目录：

```text
skills/
  podcast-radar-cn/
    SKILL.md
    agents/
    references/
    scripts/
```

建议每个 Skill 使用独立目录，例如：

```text
skills/
  episode-outline/
    SKILL.md
    examples/
    assets/
```

最少应包含：

- `SKILL.md`：说明这个 Skill 解决什么问题、适用于什么场景
- `agents/`：放展示名、默认提示词等 agent 元信息
- 输入与输出约定：方便协作者复用和改进
- `references/`：沉淀字段说明、边界和输出模式
- `scripts/`：把稳定的抓取、清洗、富化逻辑沉淀成可复用工具
- 示例：帮助新贡献者快速理解效果边界

兼容性建议：

- 把每个 Skill 当成一个可独立搬运的目录，不要假设它一定运行在当前仓库根目录下
- 在 `SKILL.md` 中引用脚本或参考文件时，优先按 Skill 根目录组织；对 OpenClaw，推荐使用 `{baseDir}`
- 如果 Skill 依赖某个命令行工具、环境变量或配置，尽量在 frontmatter 的 `metadata.openclaw` 中声明，方便 OpenClaw / ClawHub 做安装资格判断
