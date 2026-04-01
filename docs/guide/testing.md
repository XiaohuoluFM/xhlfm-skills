# Skills 测试

小火炉播客 Skills 仓库采用一套偏“仓库级约定 + Skill 级实现”的测试方案。

目标不是为了追求复杂的工程堆栈，而是为了让未来有更多 Skill 之后，大家仍然能快速回答下面几个问题：

- 这个 Skill 的目录结构是否合格
- 它的关键脚本有没有把字段映射对
- 它会不会在边界条件下失控
- 文档站还能不能正常构建

## 当前测试分层

### 1. 仓库级契约测试

这层测试不关心某个 Skill 的业务细节，只关心它是不是一个“像样的 Skill”。

当前会检查：

- 每个 `skills/<skill-id>/` 是否都有 `SKILL.md`
- `SKILL.md` frontmatter 是否包含 `name` 和 `description`
- frontmatter 里的 `name` 是否和目录名一致
- 如果存在 `agents/openai.yaml`，它是否包含基本字段
- `scripts/` 里的 `.py` 或 `.sh` 是否可执行

这类测试的价值在于：

- 新 Skill 一接进来就能被统一校验
- 仓库不会慢慢长成“有文件但没约定”的状态

### 2. Skill 级 fixture 测试

这层测试开始进入具体 Skill。

以 `podcast-radar-cn` 为例，当前会验证：

- 《中文播客榜》字段归一化是否稳定
- 标题信号提取是否符合预期
- `min_subscription` 过滤不会误伤没有订阅字段的播客对象
- 小宇宙 `__NEXT_DATA__` 解析是否稳定
- 富化输出是否能正确映射 `pid`、`podcastUrl`、`shownotesText`
- 超量富化时是否会严格拒绝

fixture 文件放在：

```text
tests/fixtures/<skill_id>/
```

对应测试放在：

```text
tests/skills/<skill_id>/
```

这样做的好处是：

- 每个 Skill 的测试样本和测试代码都能就近维护
- 未来新增 Skill 时，不需要改动整套测试结构

### 3. 可选 live smoke

这层测试会访问真实外部服务，因此默认不进入常规本地测试命令。

当前 `podcast-radar-cn` 的 live smoke 只做极小规模验证：

- 榜单 API 是否还能拿到 1 条热门播客
- 小宇宙播客页富化是否还能拿到 `pid`

这类测试的定位不是回归测试，而是：

- 确认外部接口还活着
- 发现页面结构是否发生了明显变化

由于它会访问真实站点，所以我们默认把它和普通测试分开。

## 当前目录约定

```text
tests/
  fixtures/
    podcast_radar_cn/
      xyzrank_episode_item.json
      xyzrank_podcast_item.json
      xiaoyuzhou_episode_page.html
      xiaoyuzhou_podcast_page.html
  live/
    test_podcast_radar_cn_live.py
  skills/
    podcast_radar_cn/
      test_enrich_xiaoyuzhou.py
      test_fetch_xyz_rank.py
  test_skill_contract.py
```

## 本地命令

先安装依赖：

```bash
pnpm install
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

跑默认测试：

```bash
source .venv/bin/activate
pnpm test
```

这会执行：

- `pnpm test:skills`
- `pnpm test:docs`

只跑 Skill 测试：

```bash
source .venv/bin/activate
pnpm test:skills
```

只跑 live smoke：

```bash
source .venv/bin/activate
pnpm test:skills:live
```

只跑文档构建校验：

```bash
source .venv/bin/activate
pnpm test:docs
```

## 新增 Skill 时怎么接入测试

推荐按这个顺序来：

1. 先让 Skill 满足仓库级契约
2. 再为这个 Skill 补一组最小 fixture
3. 再写 2 到 5 个最关键的行为测试
4. 如果它依赖外部 API，再补一个极小规模的 live smoke

经验上，第一批最值得测的是：

- 字段映射
- 输入筛选
- 输出结构
- 限流/拒绝逻辑
- 容易误解的业务边界

## 为什么这里先不用 JS

不是不能用 JS，而是当前这个仓库里，真正“需要被严肃测试”的执行逻辑主要在 Python 脚本里。

拿 `podcast-radar-cn` 来说：

- 榜单抓取与归一化在 Python
- 小宇宙详情富化在 Python
- 标题信号提取在 Python

如果测试层强行改用 JS，会出现两个问题：

- 只能把 Python 脚本当黑盒子测，很多字段映射和边界逻辑不容易细测
- 要么跨进程调用 Python，要么把一部分解析逻辑再写一遍，反而更绕

所以当前默认方案是：

- 文档站和站点构建继续用 Node / pnpm
- Skill 执行逻辑如果是 Python，就优先用 `pytest`
- 未来如果某个 Skill 的核心逻辑是 JS / TS，再为那个 Skill 增加 `vitest` 或其他 Node 测试也完全没问题

也就是说，这个仓库不是“拒绝 JS”，而是“测试语言跟着 Skill 的执行语言走”。

## 推荐原则

- 默认先写 fixture 测试，再考虑 live 测试
- live 测试永远保持少量、克制、可跳过
- 不把外部平台的实时结果写死成断言
- 不为了追求覆盖率，把测试写成另一个实现
- 一个 Skill 至少要有一条能防回归的关键边界测试
