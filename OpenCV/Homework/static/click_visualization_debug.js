// 可视化点击位置调试工具
// 在点击后运行此脚本

console.log('=== 点击位置可视化 ===\n');

// 获取最后一次点击的信息
if (typeof mlState !== 'undefined' && mlState.clickPoints && mlState.clickPoints.length > 0) {
  const lastClick = mlState.clickPoints[mlState.clickPoints.length - 1];
  
  console.log('📍 最后一次点击:');
  console.log('  原始坐标:', lastClick.x, ',', lastClick.y);
  console.log('  显示坐标:', lastClick.displayX.toFixed(1), ',', lastClick.displayY.toFixed(1));
  
  if (lastClick.originalWidth && lastClick.originalHeight) {
    console.log('  原始尺寸:', lastClick.originalWidth, 'x', lastClick.originalHeight);
    
    // 计算点击位置相对于图像的百分比
    const percentX = (lastClick.x / lastClick.originalWidth * 100).toFixed(1);
    const percentY = (lastClick.y / lastClick.originalHeight * 100).toFixed(1);
    
    console.log('  位置百分比:', percentX + '%,', percentY + '%');
    
    // 判断点击位置
    if (percentX > 45 && percentX < 55 && percentY > 45 && percentY < 55) {
      console.log('  ✅ 点击在中心区域');
    } else if (percentX < 25 || percentX > 75) {
      console.log('  ⚠️ 点击在左右边缘');
    } else if (percentY < 25 || percentY > 75) {
      console.log('  ⚠️ 点击在上下边缘');
    }
  }
  
  console.log('\n🎯 后端处理预测:');
  const maxSide = parseInt(document.getElementById('max_side').value) || 1280;
  const maxDim = Math.max(lastClick.originalWidth, lastClick.originalHeight);
  
  if (maxDim > maxSide) {
    const scale = maxSide / maxDim;
    const adjustedX = Math.round(lastClick.x * scale);
    const adjustedY = Math.round(lastClick.y * scale);
    const newWidth = Math.round(lastClick.originalWidth * scale);
    const newHeight = Math.round(lastClick.originalHeight * scale);
    
    console.log('  图像会被缩放');
    console.log('  缩放比例:', scale.toFixed(3));
    console.log('  缩放后尺寸:', newWidth, 'x', newHeight);
    console.log('  调整后坐标:', adjustedX, ',', adjustedY);
    
    // 验证调整后的坐标是否在范围内
    if (adjustedX >= 0 && adjustedX < newWidth && adjustedY >= 0 && adjustedY < newHeight) {
      console.log('  ✅ 调整后坐标在范围内');
    } else {
      console.log('  ❌ 调整后坐标超出范围！');
    }
  } else {
    console.log('  图像不会被缩放');
    console.log('  直接使用原始坐标:', lastClick.x, ',', lastClick.y);
  }
  
} else {
  console.log('❌ 没有找到点击记录');
  console.log('请先在点击模式下点击图像');
}

console.log('\n=== 完成 ===');
