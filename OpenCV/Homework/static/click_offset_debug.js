// 点击偏移可视化调试工具
// 在浏览器控制台运行此脚本

console.log('=== 点击偏移调试工具 ===\n');

const img = document.getElementById('previewOrig');
const container = img.parentElement;

// 获取所有尺寸信息
const naturalWidth = img.naturalWidth;
const naturalHeight = img.naturalHeight;
const clientWidth = img.clientWidth;
const clientHeight = img.clientHeight;
const offsetWidth = img.offsetWidth;
const offsetHeight = img.offsetHeight;
const boundingRect = img.getBoundingClientRect();
const containerRect = container.getBoundingClientRect();

console.log('📐 图像尺寸对比:');
console.log('  naturalWidth/Height:', naturalWidth, 'x', naturalHeight);
console.log('  clientWidth/Height:', clientWidth, 'x', clientHeight);
console.log('  offsetWidth/Height:', offsetWidth, 'x', offsetHeight);
console.log('  boundingRect:', boundingRect.width.toFixed(1), 'x', boundingRect.height.toFixed(1));
console.log('  容器尺寸:', containerRect.width.toFixed(1), 'x', containerRect.height.toFixed(1));

// 计算偏移（当前代码的方法）
const offsetX_current = (containerRect.width - clientWidth) / 2;
const offsetY_current = (containerRect.height - clientHeight) / 2;

console.log('\n🎯 偏移计算 (当前方法):');
console.log('  offsetX:', offsetX_current.toFixed(2));
console.log('  offsetY:', offsetY_current.toFixed(2));

// 计算偏移（使用 boundingRect）
const offsetX_bounding = (containerRect.width - boundingRect.width) / 2;
const offsetY_bounding = (containerRect.height - boundingRect.height) / 2;

console.log('\n🎯 偏移计算 (boundingRect 方法):');
console.log('  offsetX:', offsetX_bounding.toFixed(2));
console.log('  offsetY:', offsetY_bounding.toFixed(2));

// 检查差异
const diffX = Math.abs(offsetX_current - offsetX_bounding);
const diffY = Math.abs(offsetY_current - offsetY_bounding);

if (diffX > 1 || diffY > 1) {
  console.log('\n⚠️ 警告: 两种方法计算的偏移不一致！');
  console.log('  差异:', diffX.toFixed(2), ',', diffY.toFixed(2));
  console.log('  建议使用 boundingRect 方法');
}

// 计算缩放比例
const scaleX_client = naturalWidth / clientWidth;
const scaleY_client = naturalHeight / clientHeight;
const scaleX_bounding = naturalWidth / boundingRect.width;
const scaleY_bounding = naturalHeight / boundingRect.height;

console.log('\n📏 缩放比例:');
console.log('  使用 clientWidth:', scaleX_client.toFixed(3), ',', scaleY_client.toFixed(3));
console.log('  使用 boundingRect:', scaleX_bounding.toFixed(3), ',', scaleY_bounding.toFixed(3));

if (Math.abs(scaleX_client - scaleY_client) > 0.01) {
  console.log('  ❌ clientWidth 方法: X 和 Y 缩放比例不一致（图像变形）');
}
if (Math.abs(scaleX_bounding - scaleY_bounding) > 0.01) {
  console.log('  ❌ boundingRect 方法: X 和 Y 缩放比例不一致（图像变形）');
} else {
  console.log('  ✅ boundingRect 方法: 缩放比例一致');
}

// 模拟点击测试
console.log('\n🖱️ 模拟点击测试:');

// 点击容器中心
const clickX = containerRect.width / 2;
const clickY = containerRect.height / 2;

console.log('  点击容器中心:', clickX.toFixed(1), ',', clickY.toFixed(1));

// 方法 1: 使用 clientWidth
const imageX1 = clickX - offsetX_current;
const imageY1 = clickY - offsetY_current;
const actualX1 = Math.round(imageX1 * scaleX_client);
const actualY1 = Math.round(imageY1 * scaleY_client);

console.log('\n  方法 1 (clientWidth):');
console.log('    图像坐标:', imageX1.toFixed(1), ',', imageY1.toFixed(1));
console.log('    原始坐标:', actualX1, ',', actualY1);
console.log('    预期中心:', Math.round(naturalWidth/2), ',', Math.round(naturalHeight/2));
console.log('    偏差:', Math.abs(actualX1 - naturalWidth/2).toFixed(1), ',', Math.abs(actualY1 - naturalHeight/2).toFixed(1));

// 方法 2: 使用 boundingRect
const imageX2 = clickX - offsetX_bounding;
const imageY2 = clickY - offsetY_bounding;
const actualX2 = Math.round(imageX2 * scaleX_bounding);
const actualY2 = Math.round(imageY2 * scaleY_bounding);

console.log('\n  方法 2 (boundingRect):');
console.log('    图像坐标:', imageX2.toFixed(1), ',', imageY2.toFixed(1));
console.log('    原始坐标:', actualX2, ',', actualY2);
console.log('    预期中心:', Math.round(naturalWidth/2), ',', Math.round(naturalHeight/2));
console.log('    偏差:', Math.abs(actualX2 - naturalWidth/2).toFixed(1), ',', Math.abs(actualY2 - naturalHeight/2).toFixed(1));

// 推荐方案
console.log('\n💡 推荐方案:');
const method1Error = Math.abs(actualX1 - naturalWidth/2) + Math.abs(actualY1 - naturalHeight/2);
const method2Error = Math.abs(actualX2 - naturalWidth/2) + Math.abs(actualY2 - naturalHeight/2);

if (method1Error < method2Error) {
  console.log('  ✅ 使用方法 1 (clientWidth) - 误差更小');
} else if (method2Error < method1Error) {
  console.log('  ✅ 使用方法 2 (boundingRect) - 误差更小');
} else {
  console.log('  ✅ 两种方法误差相同');
}

console.log('\n=== 调试完成 ===');
console.log('\n💡 提示: 如果偏差 > 5px，说明坐标计算有问题');
