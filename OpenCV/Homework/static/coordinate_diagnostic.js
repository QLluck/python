const $ = id => document.getElementById(id);

const state = {
  image: null,
  clicks: [],
  showGrid: false
};

const log = (message, type = 'info') => {
  const logContent = $('logContent');
  const entry = document.createElement('div');
  entry.className = 'log-entry';
  const time = new Date().toLocaleTimeString();
  const color = type === 'error' ? '#ff0000' : type === 'warning' ? '#ffaa00' : '#00ff00';
  entry.innerHTML = `<span style="color: #666;">[${time}]</span> <span style="color: ${color};">${message}</span>`;
  logContent.appendChild(entry);
  logContent.scrollTop = logContent.scrollHeight;
};

// 文件上传处理
const fileInput = $('fileInput');
const uploadZone = $('uploadZone');
const previewImage = $('previewImage');
const placeholder = $('placeholder');
const overlayCanvas = $('overlayCanvas');
const ctx = overlayCanvas.getContext('2d');

uploadZone.addEventListener('click', () => fileInput.click());

uploadZone.addEventListener('dragover', (e) => {
  e.preventDefault();
  uploadZone.classList.add('drag-over');
});

uploadZone.addEventListener('dragleave', () => {
  uploadZone.classList.remove('drag-over');
});

uploadZone.addEventListener('drop', (e) => {
  e.preventDefault();
  uploadZone.classList.remove('drag-over');
  const files = e.dataTransfer.files;
  if (files.length > 0) {
    loadImage(files[0]);
  }
});

fileInput.addEventListener('change', (e) => {
  if (e.target.files.length > 0) {
    loadImage(e.target.files[0]);
  }
});

function loadImage(file) {
  log(`加载图像: ${file.name} (${(file.size / 1024).toFixed(2)} KB)`);
  
  const reader = new FileReader();
  reader.onload = (e) => {
    previewImage.src = e.target.result;
    previewImage.onload = () => {
      placeholder.style.display = 'none';
      previewImage.style.display = 'block';
      state.image = previewImage;
      state.clicks = [];
      updateInfo();
      setupCanvas();
      log('✅ 图像加载成功', 'info');
      $('clearBtn').disabled = false;
    };
  };
  reader.readAsDataURL(file);
}

function setupCanvas() {
  const container = $('imageContainer');
  const rect = container.getBoundingClientRect();
  overlayCanvas.width = rect.width;
  overlayCanvas.height = rect.height;
  overlayCanvas.style.width = rect.width + 'px';
  overlayCanvas.style.height = rect.height + 'px';
  redrawCanvas();
}

function updateInfo() {
  if (!state.image) return;
  
  const img = state.image;
  const rect = img.getBoundingClientRect();
  const container = $('imageContainer');
  const containerRect = container.getBoundingClientRect();
  
  // 原始尺寸
  const naturalWidth = img.naturalWidth;
  const naturalHeight = img.naturalHeight;
  $('naturalSize').textContent = `${naturalWidth} x ${naturalHeight}`;
  
  // 显示尺寸
  const displayWidth = img.clientWidth;
  const displayHeight = img.clientHeight;
  $('displaySize').textContent = `${displayWidth} x ${displayHeight}`;
  
  // 容器尺寸
  $('containerSize').textContent = `${containerRect.width.toFixed(0)} x ${containerRect.height.toFixed(0)}`;
  
  // 缩放比例
  const scaleX = naturalWidth / displayWidth;
  const scaleY = naturalHeight / displayHeight;
  $('scaleRatio').textContent = `X: ${scaleX.toFixed(3)}, Y: ${scaleY.toFixed(3)}`;
  
  // 居中偏移
  const offsetX = (containerRect.width - displayWidth) / 2;
  const offsetY = (containerRect.height - displayHeight) / 2;
  $('offset').textContent = `X: ${offsetX.toFixed(1)}, Y: ${offsetY.toFixed(1)}`;
  
  // 检查问题
  if (Math.abs(scaleX - scaleY) > 0.01) {
    log('⚠️ 警告: X和Y缩放比例不一致，可能导致坐标偏移', 'warning');
  }
  
  if (offsetX > 10 || offsetY > 10) {
    log(`ℹ️ 图像居中显示，偏移: (${offsetX.toFixed(1)}, ${offsetY.toFixed(1)})`);
  }
}

// 鼠标移动处理
$('imageContainer').addEventListener('mousemove', (e) => {
  if (!state.image) return;
  
  const img = state.image;
  const rect = img.getBoundingClientRect();
  const containerRect = $('imageContainer').getBoundingClientRect();
  
  // 屏幕坐标
  const screenX = e.clientX;
  const screenY = e.clientY;
  $('screenCoord').textContent = `(${screenX}, ${screenY})`;
  
  // 容器坐标
  const containerX = e.clientX - containerRect.left;
  const containerY = e.clientY - containerRect.top;
  $('containerCoord').textContent = `(${containerX.toFixed(1)}, ${containerY.toFixed(1)})`;
  
  // 图像坐标
  const displayWidth = img.clientWidth;
  const displayHeight = img.clientHeight;
  const offsetX = (containerRect.width - displayWidth) / 2;
  const offsetY = (containerRect.height - displayHeight) / 2;
  
  const imageX = containerX - offsetX;
  const imageY = containerY - offsetY;
  $('imageCoord').textContent = `(${imageX.toFixed(1)}, ${imageY.toFixed(1)})`;
  
  // 检查是否在图像内
  const inBounds = imageX >= 0 && imageX < displayWidth && imageY >= 0 && imageY < displayHeight;
  
  if (inBounds) {
    // 原始坐标
    const scaleX = img.naturalWidth / displayWidth;
    const scaleY = img.naturalHeight / displayHeight;
    const actualX = Math.round(imageX * scaleX);
    const actualY = Math.round(imageY * scaleY);
    $('actualCoord').textContent = `(${actualX}, ${actualY})`;
    $('actualCoord').className = 'info-value success';
    
    $('coordStatus').textContent = '✅ 图像内';
    $('coordStatus').className = 'info-value success';
    
    img.style.cursor = 'crosshair';
  } else {
    $('actualCoord').textContent = '超出范围';
    $('actualCoord').className = 'info-value error';
    
    $('coordStatus').textContent = '❌ 图像外';
    $('coordStatus').className = 'info-value error';
    
    img.style.cursor = 'not-allowed';
  }
});

// 点击处理
$('imageContainer').addEventListener('click', (e) => {
  if (!state.image) return;
  
  const img = state.image;
  const rect = img.getBoundingClientRect();
  const containerRect = $('imageContainer').getBoundingClientRect();
  
  const containerX = e.clientX - containerRect.left;
  const containerY = e.clientY - containerRect.top;
  
  const displayWidth = img.clientWidth;
  const displayHeight = img.clientHeight;
  const offsetX = (containerRect.width - displayWidth) / 2;
  const offsetY = (containerRect.height - displayHeight) / 2;
  
  const imageX = containerX - offsetX;
  const imageY = containerY - offsetY;
  
  // 检查边界
  if (imageX < 0 || imageX >= displayWidth || imageY < 0 || imageY >= displayHeight) {
    log('❌ 点击在图像外部，已拒绝', 'error');
    
    // 闪烁红色边框
    img.style.outline = '3px solid red';
    setTimeout(() => {
      img.style.outline = 'none';
    }, 500);
    
    return;
  }
  
  // 转换到原始坐标
  const scaleX = img.naturalWidth / displayWidth;
  const scaleY = img.naturalHeight / displayHeight;
  const actualX = Math.round(imageX * scaleX);
  const actualY = Math.round(imageY * scaleY);
  
  // 记录点击
  state.clicks.push({
    display: {x: imageX, y: imageY},
    actual: {x: actualX, y: actualY},
    container: {x: containerX, y: containerY}
  });
  
  $('clickCount').textContent = state.clicks.length;
  $('lastClick').textContent = `(${actualX}, ${actualY})`;
  
  log(`✅ 点击 #${state.clicks.length}: 显示(${imageX.toFixed(1)}, ${imageY.toFixed(1)}) → 原始(${actualX}, ${actualY})`);
  
  redrawCanvas();
});

function redrawCanvas() {
  if (!state.image) return;
  
  const img = state.image;
  const containerRect = $('imageContainer').getBoundingClientRect();
  
  ctx.clearRect(0, 0, overlayCanvas.width, overlayCanvas.height);
  
  const displayWidth = img.clientWidth;
  const displayHeight = img.clientHeight;
  const offsetX = (containerRect.width - displayWidth) / 2;
  const offsetY = (containerRect.height - displayHeight) / 2;
  
  // 绘制图像边界
  ctx.strokeStyle = 'rgba(0, 255, 0, 0.3)';
  ctx.lineWidth = 2;
  ctx.setLineDash([5, 5]);
  ctx.strokeRect(offsetX, offsetY, displayWidth, displayHeight);
  ctx.setLineDash([]);
  
  // 绘制网格
  if (state.showGrid) {
    ctx.strokeStyle = 'rgba(0, 255, 0, 0.1)';
    ctx.lineWidth = 1;
    
    const gridSize = 50;
    for (let x = offsetX; x < offsetX + displayWidth; x += gridSize) {
      ctx.beginPath();
      ctx.moveTo(x, offsetY);
      ctx.lineTo(x, offsetY + displayHeight);
      ctx.stroke();
    }
    for (let y = offsetY; y < offsetY + displayHeight; y += gridSize) {
      ctx.beginPath();
      ctx.moveTo(offsetX, y);
      ctx.lineTo(offsetX + displayWidth, y);
      ctx.stroke();
    }
  }
  
  // 绘制点击标记
  state.clicks.forEach((click, index) => {
    const canvasX = offsetX + click.display.x;
    const canvasY = offsetY + click.display.y;
    
    // 十字标记
    ctx.strokeStyle = '#00ff00';
    ctx.lineWidth = 2;
    ctx.shadowColor = 'rgba(0, 0, 0, 0.8)';
    ctx.shadowBlur = 4;
    
    const size = 15;
    ctx.beginPath();
    ctx.moveTo(canvasX - size, canvasY);
    ctx.lineTo(canvasX + size, canvasY);
    ctx.moveTo(canvasX, canvasY - size);
    ctx.lineTo(canvasX, canvasY + size);
    ctx.stroke();
    
    // 中心点
    ctx.fillStyle = '#00ff00';
    ctx.beginPath();
    ctx.arc(canvasX, canvasY, 3, 0, 2 * Math.PI);
    ctx.fill();
    
    // 坐标文本
    ctx.shadowBlur = 0;
    ctx.fillStyle = '#00ff00';
    ctx.font = 'bold 11px monospace';
    ctx.fillText(`(${click.actual.x}, ${click.actual.y})`, canvasX + 20, canvasY - 10);
    
    // 编号
    ctx.fillStyle = '#ffffff';
    ctx.strokeStyle = '#00ff00';
    ctx.lineWidth = 3;
    ctx.font = 'bold 14px Arial';
    const num = (index + 1).toString();
    ctx.strokeText(num, canvasX - 5, canvasY + 5);
    ctx.fillText(num, canvasX - 5, canvasY + 5);
  });
}

// 清除按钮
$('clearBtn').addEventListener('click', () => {
  state.clicks = [];
  $('clickCount').textContent = '0';
  $('lastClick').textContent = '-';
  redrawCanvas();
  log('🗑️ 已清除所有标记');
});

// 网格切换
$('toggleGridBtn').addEventListener('click', () => {
  state.showGrid = !state.showGrid;
  $('toggleGridBtn').textContent = state.showGrid ? '隐藏网格' : '显示网格';
  redrawCanvas();
  log(state.showGrid ? '✅ 显示网格' : '❌ 隐藏网格');
});

// 窗口大小改变时重新设置canvas
window.addEventListener('resize', () => {
  if (state.image) {
    setupCanvas();
    updateInfo();
  }
});

log('🚀 诊断工具已就绪');
