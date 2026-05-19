// 点击分割视觉反馈改进
// 在 app.js 中添加或替换以下代码

// 在图像上绘制点击标记
function drawClickMarker(imageElement, x, y, displayX, displayY) {
  // 创建或获取 canvas 覆盖层
  let canvas = document.getElementById('clickMarkerCanvas');
  if (!canvas) {
    canvas = document.createElement('canvas');
    canvas.id = 'clickMarkerCanvas';
    canvas.style.position = 'absolute';
    canvas.style.pointerEvents = 'none'; // 不阻挡鼠标事件
    canvas.style.zIndex = '10';
    imageElement.parentElement.style.position = 'relative';
    imageElement.parentElement.appendChild(canvas);
  }
  
  // 设置 canvas 尺寸匹配图像显示尺寸
  const rect = imageElement.getBoundingClientRect();
  canvas.width = imageElement.width || rect.width;
  canvas.height = imageElement.height || rect.height;
  canvas.style.left = imageElement.offsetLeft + 'px';
  canvas.style.top = imageElement.offsetTop + 'px';
  canvas.style.width = canvas.width + 'px';
  canvas.style.height = canvas.height + 'px';
  
  const ctx = canvas.getContext('2d');
  
  // 绘制十字标记
  const markerSize = 20;
  const markerThickness = 2;
  
  ctx.strokeStyle = '#00ff00'; // 绿色
  ctx.lineWidth = markerThickness;
  ctx.shadowColor = 'rgba(0, 0, 0, 0.5)';
  ctx.shadowBlur = 3;
  
  // 绘制十字
  ctx.beginPath();
  // 水平线
  ctx.moveTo(displayX - markerSize, displayY);
  ctx.lineTo(displayX + markerSize, displayY);
  // 垂直线
  ctx.moveTo(displayX, displayY - markerSize);
  ctx.lineTo(displayX, displayY + markerSize);
  ctx.stroke();
  
  // 绘制中心圆点
  ctx.fillStyle = '#00ff00';
  ctx.beginPath();
  ctx.arc(displayX, displayY, 3, 0, 2 * Math.PI);
  ctx.fill();
  
  // 绘制坐标文本
  ctx.shadowBlur = 0;
  ctx.fillStyle = '#00ff00';
  ctx.font = 'bold 12px monospace';
  ctx.fillText(`(${x}, ${y})`, displayX + 25, displayY - 10);
  
  // 添加编号（如果有多个点击）
  const clickNumber = mlState.clickPoints.length;
  ctx.fillStyle = '#ffffff';
  ctx.strokeStyle = '#00ff00';
  ctx.lineWidth = 3;
  ctx.font = 'bold 16px Arial';
  const numberText = clickNumber.toString();
  ctx.strokeText(numberText, displayX - 5, displayY + 5);
  ctx.fillText(numberText, displayX - 5, displayY + 5);
}

// 清除所有点击标记
function clearClickMarkers() {
  const canvas = document.getElementById('clickMarkerCanvas');
  if (canvas) {
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  }
}

// 重绘所有点击标记
function redrawAllClickMarkers(imageElement) {
  clearClickMarkers();
  
  if (!mlState.clickPoints || mlState.clickPoints.length === 0) {
    return;
  }
  
  const rect = imageElement.getBoundingClientRect();
  const displayWidth = imageElement.width || rect.width;
  const displayHeight = imageElement.height || rect.height;
  const scaleX = displayWidth / imageElement.naturalWidth;
  const scaleY = displayHeight / imageElement.naturalHeight;
  
  mlState.clickPoints.forEach((point, index) => {
    const displayX = point.x * scaleX;
    const displayY = point.y * scaleY;
    drawClickMarker(imageElement, point.x, point.y, displayX, displayY);
  });
}

// 添加鼠标悬停坐标显示
function addCoordinateDisplay(imageElement) {
  // 创建坐标显示元素
  let coordDisplay = document.getElementById('coordDisplay');
  if (!coordDisplay) {
    coordDisplay = document.createElement('div');
    coordDisplay.id = 'coordDisplay';
    coordDisplay.style.cssText = `
      position: absolute;
      background: rgba(0, 0, 0, 0.8);
      color: #00ff00;
      padding: 5px 10px;
      border-radius: 4px;
      font-family: monospace;
      font-size: 12px;
      pointer-events: none;
      z-index: 20;
      display: none;
    `;
    document.body.appendChild(coordDisplay);
  }
  
  imageElement.addEventListener('mousemove', (e) => {
    if (mlState.mode !== 'click') return;
    
    const rect = imageElement.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const clickY = e.clientY - rect.top;
    
    const displayWidth = imageElement.width || rect.width;
    const displayHeight = imageElement.height || rect.height;
    const offsetX = (rect.width - displayWidth) / 2;
    const offsetY = (rect.height - displayHeight) / 2;
    
    const imageX = clickX - offsetX;
    const imageY = clickY - offsetY;
    
    if (imageX >= 0 && imageX < displayWidth && imageY >= 0 && imageY < displayHeight) {
      const scaleX = imageElement.naturalWidth / displayWidth;
      const scaleY = imageElement.naturalHeight / displayHeight;
      const actualX = Math.round(imageX * scaleX);
      const actualY = Math.round(imageY * scaleY);
      
      coordDisplay.textContent = `坐标: (${actualX}, ${actualY})`;
      coordDisplay.style.display = 'block';
      coordDisplay.style.left = (e.clientX + 15) + 'px';
      coordDisplay.style.top = (e.clientY + 15) + 'px';
    } else {
      coordDisplay.style.display = 'none';
    }
  });
  
  imageElement.addEventListener('mouseleave', () => {
    coordDisplay.style.display = 'none';
  });
}

// 修改原有的 handleImageClick 函数
// 在 performClickSegmentation 之前添加：
// drawClickMarker(previewOrig, clampedX, clampedY, imageX, imageY);

// 修改 clearClicksBtn 的事件处理
// 添加：clearClickMarkers();

// 在图像加载完成后调用
// addCoordinateDisplay(previewOrig);
