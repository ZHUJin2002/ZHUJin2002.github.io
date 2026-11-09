# Jin Zhu · Personal homepage

适合 GitHub Pages 的静态学术主页。无 npm 依赖；Python 标准库生成页面。

## 日常更新

1. 打开 `editor.html`，修改介绍、论文、新闻或教学经历。
2. 点击“下载更新后的 content.json”。此操作不会直接发布网站。
3. 在 GitHub 仓库中替换根目录的 `content.json` 并提交。
4. GitHub Actions 自动生成页面并发布，网址保持 https://zhujin2002.github.io/ 。

浏览器草稿只保存在当前浏览器。可导入 JSON 继续编辑。公开编辑页没有仓库写入权限，访客不能修改线上内容。

## 本地预览

```
python3 build.py
python3 -m http.server 8080 --directory dist
```

访问 http://localhost:8080 ，编辑页为 http://localhost:8080/editor.html 。

## 首次迁移到现有仓库

先备份当前仓库，在新分支合入本目录内容。仓库 Settings → Pages → Build and deployment 选择 GitHub Actions。发布流程先生成原站全部页面，再覆盖新版首页，因此保留现有画廊与旧链接。

根目录 `content.json` 是内容源，`dist/content.json` 是给编辑器读取的副本。修改布局用 `build.py`，样式用 `dist/style.css`，交互用 `dist/app.js`。替换头像或简历直接更新 `dist/assets/` 下的对应文件。

现有公开主页内容迁入，未自动补写新经历或改变论文状态。
