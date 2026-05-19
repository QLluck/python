# ML 模式切换问题调试指南

## 问题描述
无法切换到智能模式和点击模式

## 调试步骤

### 1. 打开浏览器开发者工具

1. 访问 http://localhost:8000
2. 按 `F12` 或 `Cmd+Option+I` (Mac) 打开开发者工具
3. 切换到 **Console** 标签

### 2. 检查初始化日志

页面加载后，应该看到以下日志：

```
Initializing ML mode...
ML elements found: {
  modeTabs: 3,
  modeDescription: true,
  smartPanel: true,
  clickPanel: true,
  predictBtn: true,
  clearClicksBtn: true,
  paramGrid: true,
  advancedSections: 2
}
ML 模式功能已初始化
```

**如果没有看到这些日志：**
- 检查是否有 JavaScript 错误
- 刷新页面 (Ctrl+R 或 Cmd+R)
- 清除缓存后刷新 (Ctrl+Shift+R 或 Cmd+Shift+R)

### 3. 测试模式切换

点击 "智能模式" 或 "点击模式" 标签，应该看到：

```
Mode tab clicked: smart
Switching to mode: smart
Toggling panels: {smartPanel: true, clickPanel: true}
Smart panel hidden: false
Click panel hidden: true
Show params: false mode: smart lastPrediction: false
切换到智能模式
Mode switch complete
```

### 4. 常见问题排查

#### 问题 A: 点击没有反应

**检查：**
```javascript
// 在 Console 中运行
document.querySelectorAll('.mode-tab').length
// 应该返回 3
```

**如果返回 0：**
- HTML 没有正确加载
- 清除浏览器缓存
- 检查 HTML 文件是否正确保存

#### 问题 B: 点击有反应但面板不显示

**检查元素：**
```javascript
// 在 Console 中运行
document.getElementById('smartModePanel')
document.getElementById('clickModePanel')
// 应该返回 DOM 元素，不是 null
```

**如果返回 null：**
- HTML 元素 ID 不匹配
- 检查 index.html 是否包含这些元素

#### 问题 C: CSS 样式问题

**检查样式：**
```javascript
// 在 Console 中运行
const panel = document.getElementById('smartModePanel');
console.log(panel.hidden);
console.log(window.getComputedStyle(panel).display);
```

**如果 display 是 'none' 但 hidden 是 false：**
- CSS 冲突
- 检查 style.css 是否正确加载

### 5. 手动测试切换

在 Console 中手动执行：

```javascript
// 切换到智能模式
const smartPanel = document.getElementById('smartModePanel');
const clickPanel = document.getElementById('clickModePanel');
smartPanel.hidden = false;
clickPanel.hidden = true;
console.log('Manually switched to smart mode');

// 切换到点击模式
smartPanel.hidden = true;
clickPanel.hidden = false;
console.log('Manually switched to click mode');
```

如果手动切换有效，说明是事件监听器的问题。

### 6. 检查事件监听器

```javascript
// 在 Console 中运行
const tabs = document.querySelectorAll('.mode-tab');
tabs.forEach((tab, i) => {
  console.log(`Tab ${i}:`, tab.dataset.mode, 'has listeners:', 
    getEventListeners(tab).click ? 'yes' : 'no');
});
```

### 7. 强制重新初始化

如果一切都失败了，在 Console 中运行：

```javascript
// 重新初始化 ML 模式
if (typeof initMLMode === 'function') {
  initMLMode();
  console.log('ML mode re-initialized');
} else {
  console.error('initMLMode function not found');
}
```

## 快速修复方案

### 方案 1: 清除缓存

1. 按 `Ctrl+Shift+Delete` (或 Mac 上 `Cmd+Shift+Delete`)
2. 选择 "缓存的图像和文件"
3. 点击 "清除数据"
4. 刷新页面

### 方案 2: 硬刷新

- Windows/Linux: `Ctrl+Shift+R`
- Mac: `Cmd+Shift+R`

### 方案 3: 无痕模式测试

1. 打开无痕/隐私浏览窗口
2. 访问 http://localhost:8000
3. 测试模式切换

如果无痕模式下正常，说明是缓存问题。

## 预期行为

### 手动模式（默认）
- 显示所有参数控制
- 显示高级选项折叠面板
- 不显示智能/点击面板

### 智能模式
- 显示 "预测最优参数" 按钮
- 隐藏参数控制（预测前）
- 显示参数控制（预测后）
- 显示预测结果面板

### 点击模式
- 显示点击说明
- 显示 "清除点击" 按钮
- 隐藏所有参数控制
- 显示点击计数

## 检查清单

- [ ] 服务器正在运行 (http://localhost:8000)
- [ ] 页面正常加载（能看到标题）
- [ ] 能看到三个模式标签
- [ ] 浏览器控制台没有错误
- [ ] 看到 "ML 模式功能已初始化" 日志
- [ ] 点击标签时有 "Mode tab clicked" 日志
- [ ] 清除了浏览器缓存

## 如果问题仍然存在

请提供以下信息：

1. **浏览器版本：** (Chrome/Firefox/Safari 及版本号)
2. **控制台错误：** (截图或复制错误信息)
3. **初始化日志：** (是否看到 "ML 模式功能已初始化")
4. **元素检查结果：**
   ```javascript
   console.log({
     tabs: document.querySelectorAll('.mode-tab').length,
     smartPanel: !!document.getElementById('smartModePanel'),
     clickPanel: !!document.getElementById('clickModePanel')
   });
   ```

## 临时解决方案

如果模式切换仍然有问题，可以直接在 Console 中手动切换：

```javascript
// 切换到智能模式
document.getElementById('smartModePanel').hidden = false;
document.getElementById('clickModePanel').hidden = true;
document.querySelector('.param-grid').style.display = 'none';

// 切换到点击模式
document.getElementById('smartModePanel').hidden = true;
document.getElementById('clickModePanel').hidden = false;
document.querySelector('.param-grid').style.display = 'none';

// 切换回手动模式
document.getElementById('smartModePanel').hidden = true;
document.getElementById('clickModePanel').hidden = true;
document.querySelector('.param-grid').style.display = 'grid';
```

---

**更新时间：** 2026-05-11  
**调试版本：** 已添加详细日志
