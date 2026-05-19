// 诊断脚本 - 在浏览器控制台运行

console.log('=== Logger 诊断 ===');

// 1. 检查 Logger 对象
console.log('1. Logger 对象:', typeof Logger !== 'undefined' ? '✓ 存在' : '✗ 不存在');

// 2. 检查 debugLog 元素
const debugLog = document.getElementById('debugLog');
console.log('2. debugLog 元素:', debugLog ? '✓ 存在' : '✗ 不存在');

// 3. 检查 debugPanel 元素
const debugPanel = document.getElementById('debugPanel');
console.log('3. debugPanel 元素:', debugPanel ? '✓ 存在' : '✗ 不存在');

// 4. 测试 Logger 方法
if (typeof Logger !== 'undefined') {
  console.log('4. 测试 Logger 方法:');
  try {
    Logger.info('测试 INFO');
    console.log('   - Logger.info(): ✓');
  } catch (e) {
    console.error('   - Logger.info(): ✗', e);
  }
  
  try {
    Logger.success('测试 SUCCESS', '详细信息');
    console.log('   - Logger.success(): ✓');
  } catch (e) {
    console.error('   - Logger.success(): ✗', e);
  }
  
  try {
    Logger.warning('测试 WARNING');
    console.log('   - Logger.warning(): ✓');
  } catch (e) {
    console.error('   - Logger.warning(): ✗', e);
  }
  
  try {
    Logger.error('测试 ERROR', '错误详情');
    console.log('   - Logger.error(): ✓');
  } catch (e) {
    console.error('   - Logger.error(): ✗', e);
  }
}

// 5. 检查日志条目
if (debugLog) {
  const entries = debugLog.querySelectorAll('.debug-entry');
  console.log('5. 日志条目数量:', entries.length);
  if (entries.length > 0) {
    console.log('   第一条日志:', entries[0].textContent);
  }
}

// 6. 检查面板是否折叠
if (debugPanel) {
  console.log('6. 面板状态:', debugPanel.classList.contains('collapsed') ? '折叠' : '展开');
}

console.log('=== 诊断完成 ===');
