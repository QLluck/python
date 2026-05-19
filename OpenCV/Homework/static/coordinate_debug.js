// 完整的坐标诊断脚本
// 在浏览器控制台运行此脚本

console.log('=== 坐标诊断工具 ===\n');

const img = document.getElementById('previewOrig');
const container = img.parentElement;

// 1. 图像信息
console.log('📐 图像信息:');
console.log('  原始尺寸:', img.naturalWidth, 'x', img.naturalHeight);
console.log('  原始宽高比:', (img.naturalWidth / img.naturalHeight).toFixed(3));
console.log('  显示尺寸:', img.clientWidth, 'x', img.clientHeight);
console.log('  显示宽高比:', (img.clientWidth / img.clientHeight).toFixed(3));

// 2. 容器信息
console.log('\n📦 容器信息:');
console.log('  容器尺寸:', container.clientWidth, 'x', container.clientHeight);
console.log('  容器宽高比:', (container.clientWidth / container.clientHeight).toFixed(3));

// 3. 计算偏移（object-fit: contain 的效果）
const containerRect = container.getBoundingClientRect();
const displayWidth = img.clientWidth;
const displayHeight = img.clientHeight;
const offsetX = (containerRect.width - displayWidth) / 2;
const offsetY = (containerRect.height - displayHeight) / 2;

console.log('\n🎯 偏移计算:');
console.log('  水平偏移 (offsetX):', offsetX.toFixed(2), 'px');
console.log('  垂直偏移 (offsetY):', offsetY.toFixed(2), 'px');

if (offsetX > 1) {
  console.log('  ⚠️ 左右有黑边');
}
if (offsetY > 1) {
  console.log('  ⚠️ 上下有黑边');
}

// 4. 验证宽高比
const originalRatio = img.naturalWidth / img.naturalHeight;
const displayRatio = img.clientWidth / img.clientHeight;
const ratioDiff = Math.abs(originalRatio - displayRatio);

console.log('\n✅ 宽高比验证:');
if (ratioDiff < 0.01) {
  console.log('  ✅ 图像未变形 (差异:', ratioDiff.toFixed(4), ')');
} else {
  console.log('  ❌ 图像被拉伸了 (差异:', ratioDiff.toFixed(4), ')');
}

// 5. 模拟点击测试
console.log('\n🖱️ 模拟点击测试 (点击图像中心):');

// 模拟点击图像中心
const centerContainerX = containerRect.width / 2;
const centerContainerY = containerRect.height / 2;

const imageX = centerContainerX - offsetX;
const imageY = centerContainerY - offsetY;

console.log('  容器中心:', centerContainerX.toFixed(1), ',', centerContainerY.toFixed(1));
console.log('  图像坐标:', imageX.toFixed(1), ',', imageY.toFixed(1));

// 检查是否在图像内
if (imageX >= 0 && imageX < displayWidth && imageY >= 0 && imageY < displayHeight) {
  console.log('  ✅ 在图像内');
  
  // 转换到原始坐标
  const scaleX = img.naturalWidth / displayWidth;
  const scaleY = img.naturalHeight / displayHeight;
  const actualX = Math.round(imageX * scaleX);
  const actualY = Math.round(imageY * scaleY);
  
  console.log('  缩放比例:', scaleX.toFixed(3), ',', scaleY.toFixed(3));
  console.log('  原始坐标:', actualX, ',', actualY);
  console.log('  预期中心:', Math.round(img.naturalWidth/2), ',', Math.round(img.naturalHeight/2));
  
  const centerDiffX = Math.abs(actualX - img.naturalWidth/2);
  const centerDiffY = Math.abs(actualY - img.naturalHeight/2);
  
  if (centerDiffX < 2 && centerDiffY < 2) {
    console.log('  ✅ 坐标计算准确！');
  } else {
    console.log('  ⚠️ 坐标有偏差:', centerDiffX.toFixed(1), ',', centerDiffY.toFixed(1), 'px');
  }
} else {
  console.log('  ❌ 不在图像内（计算错误！）');
}

// 6. 后端缩放信息
console.log('\n🔄 后端缩放预测:');
const maxSide = parseInt(document.getElementById('max_side').value) || 1280;
const maxOriginalDim = Math.max(img.naturalWidth, img.naturalHeight);

if (maxOriginalDim > maxSide) {
  const scaleFactor = maxSide / maxOriginalDim;
  const scaledWidth = Math.round(img.naturalWidth * scaleFactor);
  const scaledHeight = Math.round(img.naturalHeight * scaleFactor);
  
  console.log('  max_side:', maxSide);
  console.log('  缩放比例:', scaleFactor.toFixed(3));
  console.log('  后端图像尺寸:', scaledWidth, 'x', scaledHeight);
  console.log('  ⚠️ 图像会被缩放');
} else {
  console.log('  ✅ 图像不会被缩放');
}

console.log('\n=== 诊断完成 ===');
