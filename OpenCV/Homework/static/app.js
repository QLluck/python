const $ = (id) => document.getElementById(id);

const state = {
  lastOverlayB64: null,
  lastMaskB64: null,
  lastRoiB64: null,
  lastPreB64: null,
  lastLbpB64: null,
  lastObjectUrl: null,
  toastCount: 0,
  debugLogs: [],
  maxLogs: 100,
};

// Logger system
const Logger = {
  log(level, message, detail = null) {
    const time = new Date().toLocaleTimeString('zh-CN', { hour12: false });
    const entry = { time, level, message, detail };
    
    // Add to logs array with FIFO limit
    state.debugLogs.push(entry);
    if (state.debugLogs.length > state.maxLogs) {
      state.debugLogs.shift();
    }
    
    this.render(entry);
    
    // Console output
    const consoleMethod = level === 'error' ? 'error' : level === 'warning' ? 'warn' : 'log';
    console[consoleMethod](`[${level.toUpperCase()}]`, message, detail || '');
  },
  
  info(message, detail) {
    this.log('info', message, detail);
  },
  
  success(message, detail) {
    this.log('success', message, detail);
  },
  
  warning(message, detail) {
    this.log('warning', message, detail);
  },
  
  error(message, detail) {
    this.log('error', message, detail);
  },
  
  render(entry) {
    const logContainer = $('debugLog');
    if (!logContainer) {
      console.warn('debugLog container not found');
      return;
    }
    
    const entryDiv = document.createElement('div');
    entryDiv.className = 'debug-entry';
    
    entryDiv.innerHTML = `
      <span class="debug-time">${entry.time}</span>
      <span class="debug-level ${entry.level}">[${entry.level.toUpperCase()}]</span>
      <span class="debug-message">${entry.message}${entry.detail ? '<br><span class="debug-detail">└─ ' + entry.detail + '</span>' : ''}</span>
    `;
    
    logContainer.appendChild(entryDiv);
    
    // Auto-scroll to bottom
    logContainer.scrollTop = logContainer.scrollHeight;
  },
  
  clear() {
    state.debugLogs = [];
    const logContainer = $('debugLog');
    if (logContainer) {
      logContainer.innerHTML = '';
    }
    this.info('日志已清空');
  }
};

// Toast 通知系统（优化：最多3个）
function showToast(message, type = 'error') {
  const container = $('toastContainer');
  
  // 限制最多3个Toast
  if (state.toastCount >= 3) {
    const toasts = container.querySelectorAll('.toast');
    if (toasts.length > 0) toasts[0].remove();
  }
  
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  
  const iconMap = {
    success: '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>',
    error: '<circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/>',
    warning: '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>'
  };
  
  toast.innerHTML = `
    <svg class="toast-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      ${iconMap[type] || iconMap.error}
    </svg>
    <div class="toast-content">
      <div class="toast-title">${type === 'success' ? '成功' : type === 'warning' ? '警告' : '错误'}</div>
      <div class="toast-message">${message}</div>
    </div>
    <button class="toast-close" onclick="this.parentElement.remove(); state.toastCount--;">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
      </svg>
    </button>
  `;
  
  container.appendChild(toast);
  state.toastCount++;
  
  // 成功3秒消失，错误5秒消失
  const timeout = type === 'success' ? 3000 : 5000;
  setTimeout(() => {
    if (toast.parentElement) {
      toast.remove();
      state.toastCount--;
    }
  }, timeout);
}

function setLoading(on) {
  $('loading').hidden = !on;
  $('runBtn').disabled = on;
}

function b64ToBlobUrl(b64, mime = 'image/png') {
  const bin = atob(b64);
  const arr = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i);
  const blob = new Blob([arr], { type: mime });
  if (state.lastObjectUrl) URL.revokeObjectURL(state.lastObjectUrl);
  state.lastObjectUrl = URL.createObjectURL(blob);
  return state.lastObjectUrl;
}

function downloadB64(filename, b64) {
  if (!b64) return;
  const a = document.createElement('a');
  a.href = b64ToBlobUrl(b64);
  a.download = filename;
  a.click();
}

// 参数验证函数
function validateParams() {
  const errors = [];
  
  // 验证 median_ksize 必须是奇数
  const medianKsize = parseInt($('median_ksize').value);
  if (isNaN(medianKsize) || medianKsize < 1) {
    errors.push('median_ksize 必须 >= 1');
    $('median_ksize').style.borderColor = '#f43f5e';
  } else if (medianKsize % 2 === 0) {
    errors.push('median_ksize 必须是奇数（如 3, 5, 7）');
    $('median_ksize').style.borderColor = '#f43f5e';
  } else {
    $('median_ksize').style.borderColor = '';
  }
  
  // 验证 max_side
  const maxSide = parseInt($('max_side').value);
  if (isNaN(maxSide) || maxSide <= 0) {
    errors.push('max_side 必须 > 0');
    $('max_side').style.borderColor = '#f43f5e';
  } else {
    $('max_side').style.borderColor = '';
  }
  
  // 验证 tophat_kernel 必须是奇数
  const tophatKernel = parseInt($('tophat_kernel').value);
  if ($('use_tophat').checked && (isNaN(tophatKernel) || tophatKernel < 3 || tophatKernel % 2 === 0)) {
    errors.push('tophat_kernel 必须是 >= 3 的奇数');
    $('tophat_kernel').style.borderColor = '#f43f5e';
  } else {
    $('tophat_kernel').style.borderColor = '';
  }
  
  // 验证 morph_kernel_segment 必须是奇数
  const morphKernel = parseInt($('morph_kernel_segment').value);
  if (isNaN(morphKernel) || morphKernel < 3 || morphKernel % 2 === 0) {
    errors.push('morph_kernel 必须是 >= 3 的奇数');
    $('morph_kernel_segment').style.borderColor = '#f43f5e';
  } else {
    $('morph_kernel_segment').style.borderColor = '';
  }
  
  return errors;
}

function collectFormData() {
  const fd = new FormData();
  
  // 验证文件
  const f = $('fileInput').files[0];
  if (!f) throw new Error('请先选择图像文件');
  
  // 验证文件类型
  const validTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/bmp'];
  if (!validTypes.includes(f.type)) {
    throw new Error(`不支持的文件格式。请选择 PNG、JPG 或 BMP 格式的图像`);
  }
  
  // 验证参数
  const errors = validateParams();
  if (errors.length > 0) {
    throw new Error(errors.join('\n'));
  }
  
  fd.append('file', f);
  const gt = $('gtInput').files[0];
  if (gt) fd.append('gt_mask', gt);

  const bool = (id) => ($(id).checked ? 'true' : 'false');
  fd.append('stage', $('stage').value);
  fd.append('mode', $('mode').value);
  fd.append('max_side', $('max_side').value);
  fd.append('median_ksize', $('median_ksize').value);
  fd.append('use_bilateral', bool('use_bilateral'));
  fd.append('bilateral_d', '7');
  fd.append('bilateral_sigma_color', '75');
  fd.append('bilateral_sigma_space', '50');
  fd.append('clahe_clip', $('clahe_clip').value);
  fd.append('clahe_tile', $('clahe_tile').value);
  fd.append('use_tophat', bool('use_tophat'));
  fd.append('tophat_kernel', $('tophat_kernel').value);
  fd.append('use_blackhat', bool('use_blackhat'));
  fd.append('blackhat_kernel', '15');
  fd.append('detect_threshold', $('detect_threshold').value);
  fd.append('adaptive_block_size', '45');
  fd.append('adaptive_c', '4');
  fd.append('min_component_area', $('min_component_area').value);
  fd.append('max_component_area_ratio', $('max_component_area_ratio').value);
  fd.append('roi_margin_ratio', $('roi_margin_ratio').value);
  fd.append('color_fusion', $('color_fusion').value);
  fd.append('segment_method', $('segment_method').value);
  fd.append('threshold_in_segment', $('threshold_in_segment').value);
  fd.append('morph_kernel_segment', $('morph_kernel_segment').value);
  fd.append('min_post_area', $('min_post_area').value);
  fd.append('grow_T', $('grow_T').value);
  fd.append('grow_G', $('grow_G').value);
  fd.append('use_gradient_gate', bool('use_gradient_gate'));
  fd.append('seed_strategy', $('seed_strategy').value);
  fd.append('watershed_fg_erosion_iters', '2');
  fd.append('watershed_bg_dilation_iters', '3');
  fd.append('return_lbp', bool('return_lbp'));
  return fd;
}

function previewOriginal(file) {
  const url = URL.createObjectURL(file);
  $('previewOrig').src = url;
  $('skeletonOrig').style.display = 'none';
}

// 拖拽上传
const uploadZone = $('uploadZone');
const fileInput = $('fileInput');

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
    fileInput.files = files;
    previewOriginal(files[0]);
    mlState.uploadedImage = files[0];
    mlState.accumulatedMaskB64 = null;
    Logger.info(`文件已选择: ${files[0].name}`, `大小: ${(files[0].size / 1024).toFixed(2)} KB`);
    showToast('文件已选择：' + files[0].name, 'success');
  }
});

fileInput.addEventListener('change', () => {
  const f = fileInput.files[0];
  if (f) {
    previewOriginal(f);
    mlState.uploadedImage = f;
    mlState.accumulatedMaskB64 = null;
    Logger.info(`文件已选择: ${f.name}`, `大小: ${(f.size / 1024).toFixed(2)} KB`);
    showToast('文件已选择：' + f.name, 'success');
  }
});

// 实时参数验证
['median_ksize', 'max_side', 'tophat_kernel', 'morph_kernel_segment'].forEach(id => {
  $(id).addEventListener('input', () => {
    validateParams();
  });
});

// Tab 切换与指示器
const tabs = document.querySelectorAll('.tab');
const tabIndicator = document.querySelector('.tab-indicator');

function updateTabIndicator() {
  const activeTab = document.querySelector('.tab.active');
  if (activeTab) {
    const { offsetLeft, offsetWidth } = activeTab;
    tabIndicator.style.left = offsetLeft + 'px';
    tabIndicator.style.width = offsetWidth + 'px';
  }
}

tabs.forEach((btn) => {
  btn.addEventListener('click', () => {
    const tab = btn.dataset.tab;
    Logger.info(`切换到 ${tab} tab`);
    tabs.forEach((b) => b.classList.remove('active'));
    btn.classList.add('active');
    updateTabIndicator();
    renderActiveTab();
  });
});

setTimeout(updateTabIndicator, 100);
window.addEventListener('resize', updateTabIndicator);

function renderActiveTab() {
  const tab = document.querySelector('.tab.active')?.dataset.tab;
  const cap = $('capMain');
  const img = $('previewMain');
  const skeleton = $('skeletonMain');
  
  // 1. 先清理旧状态
  img.src = '';
  img.onload = null;
  img.onerror = null;
  
  // 2. 显示骨架屏
  skeleton.style.display = 'block';
  
  // 3. 确定要显示的数据
  let b64Data = null;
  
  if (tab === 'overlay') {
    cap.textContent = '叠加 / 轮廓';
    b64Data = state.lastOverlayB64;
  } else if (tab === 'mask') {
    cap.textContent = '二值掩膜';
    b64Data = state.lastMaskB64;
  } else if (tab === 'roi') {
    cap.textContent = 'ROI 框';
    b64Data = state.lastRoiB64;
  } else if (tab === 'pre') {
    cap.textContent = '预处理';
    b64Data = state.lastPreB64;
  } else if (tab === 'lbp') {
    cap.textContent = 'LBP';
    b64Data = state.lastLbpB64;
  }
  
  // 4. 如果有数据，先绑定事件，再设置 src
  if (b64Data) {
    Logger.info(`渲染 ${tab} 图片`, `数据大小: ${(b64Data.length / 1024).toFixed(2)} KB`);
    img.onload = () => {
      skeleton.style.display = 'none';
      Logger.success(`${tab} 图片加载成功`);
    };
    img.onerror = () => {
      skeleton.style.display = 'none';
      Logger.error(`${tab} 图片加载失败`, 'base64 数据可能损坏');
      showToast('图片加载失败', 'error');
    };
    img.src = `data:image/png;base64,${b64Data}`;
  } else {
    // 没有数据，隐藏骨架屏
    skeleton.style.display = 'none';
    Logger.warning(`${tab} 无数据`, '该阶段可能未返回图片');
  }
}

// 复制元数据
$('copyMeta').addEventListener('click', () => {
  const text = $('metaBox').textContent;
  navigator.clipboard.writeText(text).then(() => {
    showToast('元数据已复制到剪贴板', 'success');
  }).catch(() => {
    showToast('复制失败', 'error');
  });
});

// 运行处理
$('runBtn').addEventListener('click', async () => {
  Logger.info('开始处理图像...');
  
  let fd;
  try {
    fd = collectFormData();
    Logger.info('参数验证通过');
  } catch (e) {
    Logger.error('参数验证失败', e.message);
    showToast(e.message || String(e), 'error');
    return;
  }

  setLoading(true);
  $('metaContainer').hidden = true;
  
  Logger.info('发送 API 请求...');
  
  // 3秒后显示耐心等待提示
  const slowTimer = setTimeout(() => {
    showToast('处理较慢，请耐心等待...', 'warning');
  }, 3000);
  
  try {
    const res = await fetch('/api/process', { method: 'POST', body: fd });
    clearTimeout(slowTimer);
    
    let data;
    try {
      data = await res.json();
    } catch {
      throw new Error('服务器返回格式错误');
    }
    
    if (!res.ok) {
      // 详细的错误处理
      let errorMsg = data.error || `请求失败 (HTTP ${res.status})`;
      
      Logger.error(`API 请求失败 (HTTP ${res.status})`, errorMsg);
      
      if (res.status === 400) {
        errorMsg = '参数错误：' + errorMsg;
        if (errorMsg.includes('median_ksize')) {
          $('median_ksize').style.borderColor = '#f43f5e';
        }
      } else if (res.status === 422) {
        errorMsg = '参数验证失败：' + errorMsg;
      } else if (res.status === 500) {
        errorMsg = '服务器内部错误，请稍后重试';
      }
      
      showToast(errorMsg, 'error');
      $('metaBox').textContent = JSON.stringify(data, null, 2);
      $('metaContainer').hidden = false;
      return;
    }
    
    if (!data.ok) {
      Logger.error('处理失败', data.error || '未知错误');
      showToast(data.error || '处理失败', 'error');
      $('metaBox').textContent = JSON.stringify(data, null, 2);
      $('metaContainer').hidden = false;
      return;
    }

    Logger.success('API 响应成功', `耗时: ${data.meta.elapsed_ms}ms`);
    
    // Log data reception
    if (data.overlay_png_b64) {
      Logger.info('overlay 数据已接收', `${(data.overlay_png_b64.length / 1024).toFixed(2)} KB`);
    }
    if (data.mask_png_b64) {
      Logger.info('mask 数据已接收', `${(data.mask_png_b64.length / 1024).toFixed(2)} KB`);
    }
    if (data.roi_preview_png_b64) {
      Logger.info('ROI 数据已接收', `${(data.roi_preview_png_b64.length / 1024).toFixed(2)} KB`);
    }
    if (data.preprocess_png_b64) {
      Logger.info('预处理数据已接收', `${(data.preprocess_png_b64.length / 1024).toFixed(2)} KB`);
    }
    if (data.lbp_png_b64) {
      Logger.info('LBP 数据已接收', `${(data.lbp_png_b64.length / 1024).toFixed(2)} KB`);
    }

    state.lastOverlayB64 = data.overlay_png_b64;
    state.lastMaskB64 = data.mask_png_b64;
    state.lastRoiB64 = data.roi_preview_png_b64;
    state.lastPreB64 = data.preprocess_png_b64;
    state.lastLbpB64 = data.lbp_png_b64;

    $('metaBox').textContent = JSON.stringify(data.meta, null, 2);
    $('metaContainer').hidden = false;
    $('dlOverlay').disabled = !data.overlay_png_b64;
    $('dlMask').disabled = !data.mask_png_b64;
    
    renderActiveTab();
    showToast(`处理完成！耗时 ${data.meta.elapsed_ms}ms`, 'success');
    
  } catch (e) {
    clearTimeout(slowTimer);
    if (e.name === 'TypeError') {
      Logger.error('网络错误', e.message);
      showToast('网络错误或服务不可达。请检查服务是否正常运行，然后重试', 'error');
    } else {
      showToast(String(e), 'error');
    }
  } finally {
    setLoading(false);
  }
});

$('dlOverlay').addEventListener('click', () => downloadB64('overlay.png', state.lastOverlayB64));
$('dlMask').addEventListener('click', () => downloadB64('mask.png', state.lastMaskB64));

// Debug panel controls - 确保在 DOM 加载后初始化
function initDebugPanel() {
  const toggleBtn = $('toggleLog');
  const clearBtn = $('clearLog');
  const panel = $('debugPanel');
  
  if (!toggleBtn || !clearBtn || !panel) {
    console.warn('Debug panel elements not found');
    return;
  }
  
  toggleBtn.addEventListener('click', () => {
    panel.classList.toggle('collapsed');
  });

  clearBtn.addEventListener('click', () => {
    Logger.clear();
  });

  panel.querySelector('.debug-header').addEventListener('click', (e) => {
    if (e.target.closest('.debug-actions')) return;
    panel.classList.toggle('collapsed');
  });
  
  console.log('Debug panel initialized');
}

// 立即初始化（因为脚本在 body 末尾）
initDebugPanel();

// ==================== ML Mode Functionality ====================

// ML state
const mlState = {
  currentMode: 'manual',
  uploadedImage: null,
  clickPoints: [],
  lastPrediction: null,
  accumulatedMaskB64: null,
};

// Mode descriptions
const modeDescriptions = {
  manual: '手动调整所有参数，适合高级用户和精细控制',
  smart: 'AI 自动预测最优参数，您可以在预测后手动微调',
  click: '直接点击病灶位置，系统自动分割，快速便捷'
};

// Initialize ML mode functionality
function initMLMode() {
  console.log('Initializing ML mode...');
  
  const modeTabs = document.querySelectorAll('.mode-tab');
  const modeDescription = $('modeDescription');
  const smartPanel = $('smartModePanel');
  const clickPanel = $('clickModePanel');
  const predictBtn = $('predictBtn');
  const clearClicksBtn = $('clearClicksBtn');
  const paramGrid = document.querySelector('.param-grid');
  const advancedSections = document.querySelectorAll('.accordion');
  
  console.log('ML elements found:', {
    modeTabs: modeTabs.length,
    modeDescription: !!modeDescription,
    smartPanel: !!smartPanel,
    clickPanel: !!clickPanel,
    predictBtn: !!predictBtn,
    clearClicksBtn: !!clearClicksBtn,
    paramGrid: !!paramGrid,
    advancedSections: advancedSections.length
  });
  
  if (modeTabs.length === 0) {
    console.error('No mode tabs found! Check HTML structure.');
    return;
  }
  
  // Mode switching
  modeTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const mode = tab.dataset.mode;
      console.log('Mode tab clicked:', mode);
      switchMode(mode);
    });
  });
  
  function switchMode(mode) {
    console.log('Switching to mode:', mode);
    mlState.currentMode = mode;
    
    // Update active tab
    modeTabs.forEach(tab => {
      tab.classList.toggle('active', tab.dataset.mode === mode);
    });
    
    // Update description
    if (modeDescription) {
      modeDescription.querySelector('.mode-desc-text').textContent = modeDescriptions[mode];
    }
    
    // Show/hide panels
    console.log('Toggling panels:', { smartPanel: !!smartPanel, clickPanel: !!clickPanel });
    if (smartPanel) {
      smartPanel.hidden = mode !== 'smart';
      console.log('Smart panel hidden:', smartPanel.hidden);
    }
    if (clickPanel) {
      clickPanel.hidden = mode !== 'click';
      console.log('Click panel hidden:', clickPanel.hidden);
    }
    
    // Show/hide parameter controls
    const showParams = mode === 'manual' || (mode === 'smart' && mlState.lastPrediction);
    console.log('Show params:', showParams, 'mode:', mode, 'lastPrediction:', !!mlState.lastPrediction);
    if (paramGrid) paramGrid.style.display = showParams ? 'grid' : 'none';
    advancedSections.forEach(section => {
      section.style.display = showParams ? 'block' : 'none';
    });
    
    // Save to localStorage
    localStorage.setItem('mlMode', mode);
    
    Logger.info(`切换到${mode === 'manual' ? '手动' : mode === 'smart' ? '智能' : '点击'}模式`);
    console.log('Mode switch complete');
  }
  
  // Predict parameters (Smart mode)
  if (predictBtn) {
    predictBtn.addEventListener('click', async () => {
      const fileInput = $('fileInput');
      if (!fileInput.files.length) {
        showToast('请先上传图像', 'warning');
        return;
      }
      
      predictBtn.disabled = true;
      predictBtn.querySelector('.btn-text').textContent = '预测中...';
      Logger.info('开始预测最优参数...');
      
      try {
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        formData.append('max_side', $('max_side').value);
        
        const response = await fetch('/api/ml/predict-parameters', {
          method: 'POST',
          body: formData
        });
        
        const result = await response.json();
        
        if (result.ok) {
          mlState.lastPrediction = result;
          displayPrediction(result);
          applyPredictedParameters(result);
          Logger.success('参数预测完成', `方法: ${result.method}, 置信度: ${(result.confidence * 100).toFixed(1)}%`);
        } else {
          throw new Error(result.error || '预测失败');
        }
      } catch (error) {
        Logger.error('参数预测失败', error.message);
        showToast('预测失败: ' + error.message, 'error');
      } finally {
        predictBtn.disabled = false;
        predictBtn.querySelector('.btn-text').textContent = '预测最优参数';
      }
    });
  }
  
  // Display prediction results
  function displayPrediction(result) {
    const predictionResult = $('predictionResult');
    const confidenceBadge = $('confidenceBadge');
    const confidenceValue = $('confidenceValue');
    const predictedMethod = $('predictedMethod');
    const predictedParams = $('predictedParams');
    
    if (!predictionResult) return;
    
    // Show result panel
    predictionResult.hidden = false;
    
    // Update confidence badge
    const confidence = result.confidence;
    const confidencePercent = (confidence * 100).toFixed(1);
    confidenceValue.textContent = confidencePercent + '%';
    
    confidenceBadge.className = 'confidence-badge';
    if (confidence >= 0.8) {
      confidenceBadge.classList.add('high');
    } else if (confidence >= 0.5) {
      confidenceBadge.classList.add('medium');
    } else {
      confidenceBadge.classList.add('low');
    }
    
    // Update method
    const methodNames = {
      'dual': '双路自动选优',
      'otsu_roi': 'Otsu 阈值分割',
      'region_grow': '区域生长',
      'watershed': '分水岭算法'
    };
    predictedMethod.textContent = methodNames[result.method] || result.method;
    
    // Update parameters
    predictedParams.innerHTML = '';
    for (const [key, value] of Object.entries(result.parameters)) {
      const item = document.createElement('div');
      item.className = 'prediction-item';
      item.innerHTML = `
        <span class="prediction-label">${key}:</span>
        <span class="prediction-value">${typeof value === 'number' ? value.toFixed(2) : value}</span>
      `;
      predictedParams.appendChild(item);
    }
    
    // Show parameter controls
    const paramGrid = document.querySelector('.param-grid');
    const advancedSections = document.querySelectorAll('.accordion');
    if (paramGrid) paramGrid.style.display = 'grid';
    advancedSections.forEach(section => {
      section.style.display = 'block';
    });
  }
  
  // Apply predicted parameters to form
  function applyPredictedParameters(result) {
    // Set method
    const methodSelect = $('segment_method');
    if (methodSelect && result.method) {
      methodSelect.value = result.method;
    }
    
    // Set parameters
    const params = result.parameters;
    for (const [key, value] of Object.entries(params)) {
      const input = $(key);
      if (input) {
        if (input.type === 'checkbox') {
          input.checked = !!value;
        } else {
          input.value = value;
        }
      }
    }
  }
  
  // Click mode functionality
  if (clearClicksBtn) {
    clearClicksBtn.addEventListener('click', () => {
      mlState.clickPoints = [];
      mlState.accumulatedMaskB64 = null;
      updateClickCount();
      clearClicksBtn.disabled = true;
      clearClickMarkers();
      
      // 清除结果显示
      state.lastOverlayB64 = null;
      state.lastMaskB64 = null;
      const previewMain = $('previewMain');
      if (previewMain) previewMain.src = '';
      const dlOverlay = $('dlOverlay');
      const dlMask = $('dlMask');
      if (dlOverlay) dlOverlay.disabled = true;
      if (dlMask) dlMask.disabled = true;
      
      Logger.info('已清除所有点击点和分割结果');
    });
  }
  
  function updateClickCount() {
    const clickCount = $('clickCount');
    if (clickCount) {
      clickCount.textContent = mlState.clickPoints.length;
    }
  }
  
  // 绘制点击标记的辅助函数
  function drawClickMarker(imageElement, actualX, actualY, displayX, displayY) {
    let canvas = document.getElementById('clickMarkerCanvas');
    if (!canvas) {
      canvas = document.createElement('canvas');
      canvas.id = 'clickMarkerCanvas';
      canvas.style.position = 'absolute';
      canvas.style.pointerEvents = 'none';
      canvas.style.zIndex = '10';
      canvas.style.left = '0';
      canvas.style.top = '0';
      
      const container = imageElement.parentElement;
      if (container.style.position !== 'relative' && container.style.position !== 'absolute') {
        container.style.position = 'relative';
      }
      container.appendChild(canvas);
    }
    
    const containerRect = imageElement.parentElement.getBoundingClientRect();
    const imgRect = imageElement.getBoundingClientRect();
    canvas.width = containerRect.width;
    canvas.height = containerRect.height;
    canvas.style.width = containerRect.width + 'px';
    canvas.style.height = containerRect.height + 'px';
    
    const ctx = canvas.getContext('2d');
    
    // 用 img 的 boundingRect 与容器的差值计算标记在 canvas 上的位置
    const imgOffsetX = imgRect.left - containerRect.left;
    const imgOffsetY = imgRect.top - containerRect.top;
    const canvasX = imgOffsetX + displayX;
    const canvasY = imgOffsetY + displayY;
    
    // 绘制十字标记
    const markerSize = 15;
    const markerThickness = 2;
    
    ctx.strokeStyle = '#00ff00';
    ctx.lineWidth = markerThickness;
    ctx.shadowColor = 'rgba(0, 0, 0, 0.8)';
    ctx.shadowBlur = 4;
    
    // 绘制十字
    ctx.beginPath();
    ctx.moveTo(canvasX - markerSize, canvasY);
    ctx.lineTo(canvasX + markerSize, canvasY);
    ctx.moveTo(canvasX, canvasY - markerSize);
    ctx.lineTo(canvasX, canvasY + markerSize);
    ctx.stroke();
    
    // 绘制中心圆点
    ctx.shadowBlur = 2;
    ctx.fillStyle = '#00ff00';
    ctx.beginPath();
    ctx.arc(canvasX, canvasY, 3, 0, 2 * Math.PI);
    ctx.fill();
    
    // 绘制坐标文本
    ctx.shadowBlur = 3;
    ctx.fillStyle = '#00ff00';
    ctx.font = 'bold 11px monospace';
    const coordText = `(${actualX}, ${actualY})`;
    const textWidth = ctx.measureText(coordText).width;
    
    // 智能定位文本（避免超出边界）
    let textX = canvasX + 20;
    let textY = canvasY - 10;
    if (textX + textWidth > canvas.width - 10) {
      textX = canvasX - textWidth - 20;
    }
    if (textY < 15) {
      textY = canvasY + 20;
    }
    
    ctx.fillText(coordText, textX, textY);
    
    // 绘制编号
    const clickNumber = mlState.clickPoints.length + 1;
    ctx.shadowBlur = 2;
    ctx.fillStyle = '#ffffff';
    ctx.strokeStyle = '#00ff00';
    ctx.lineWidth = 3;
    ctx.font = 'bold 14px Arial';
    const numberText = clickNumber.toString();
    const numberWidth = ctx.measureText(numberText).width;
    ctx.strokeText(numberText, canvasX - numberWidth/2, canvasY + 4);
    ctx.fillText(numberText, canvasX - numberWidth/2, canvasY + 4);
  }
  
  // 清除所有点击标记
  function clearClickMarkers() {
    const canvas = document.getElementById('clickMarkerCanvas');
    if (canvas) {
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
  }
  
  // 显示图像边界（调试辅助）
  function showImageBoundary(imageElement, show = true) {
    let canvas = document.getElementById('clickMarkerCanvas');
    if (!canvas || !show) return;
    
    const ctx = canvas.getContext('2d');
    const rect = imageElement.getBoundingClientRect();
    const displayWidth = imageElement.clientWidth;
    const displayHeight = imageElement.clientHeight;
    const offsetX = (rect.width - displayWidth) / 2;
    const offsetY = (rect.height - displayHeight) / 2;
    
    // 绘制图像边界（半透明绿色框）
    ctx.strokeStyle = 'rgba(0, 255, 0, 0.3)';
    ctx.lineWidth = 2;
    ctx.setLineDash([5, 5]);
    ctx.strokeRect(
      imageElement.offsetLeft,
      imageElement.offsetTop,
      displayWidth,
      displayHeight
    );
    ctx.setLineDash([]);
  }
  
  // Setup click mode image interaction
  function setupClickModeInteraction() {
    const previewOrig = $('previewOrig');
    const previewMain = $('previewMain');
    
    if (!previewOrig) {
      console.warn('Preview image not found');
      return;
    }
    
    // Add click handler to original image preview
    previewOrig.style.cursor = 'default';
    
    const handleImageClick = async (e) => {
      // Only handle clicks in click mode
      if (mlState.currentMode !== 'click') {
        return;
      }
      
      // Check if image is loaded
      if (!mlState.uploadedImage) {
        showToast('请先上传图像', 'warning');
        return;
      }
      
      // Check if image has loaded (has naturalWidth)
      if (!previewOrig.naturalWidth || !previewOrig.naturalHeight) {
        showToast('图像还在加载中，请稍候', 'warning');
        return;
      }
      
      // Change cursor to crosshair in click mode
      previewOrig.style.cursor = 'crosshair';
      
      // 直接使用 img 元素的 boundingRect，避免容器 border/padding 导致的偏移
      const imgRect = previewOrig.getBoundingClientRect();
      const naturalWidth = previewOrig.naturalWidth;
      const naturalHeight = previewOrig.naturalHeight;
      
      // 点击相对于图像渲染区域的坐标
      const imageX = e.clientX - imgRect.left;
      const imageY = e.clientY - imgRect.top;
      const displayWidth = imgRect.width;
      const displayHeight = imgRect.height;
      
      console.log('Display info:', {
        imgRect: {w: imgRect.width, h: imgRect.height, left: imgRect.left, top: imgRect.top},
        natural: {w: naturalWidth, h: naturalHeight},
        imageCoord: {x: imageX, y: imageY}
      });
      
      // 严格检查：点击必须在图像显示区域内
      if (imageX < 0 || imageX >= displayWidth || imageY < 0 || imageY >= displayHeight) {
        console.log('❌ Click outside image bounds:', {
          imageX, imageY, 
          displayWidth, displayHeight,
          message: '点击在图像外部'
        });
        showToast('请点击图像内的位置（不要点击边缘空白区域）', 'warning');
        
        // 视觉反馈：闪烁边框
        previewOrig.style.outline = '3px solid red';
        setTimeout(() => {
          previewOrig.style.outline = 'none';
        }, 500);
        
        return;
      }
      
      // 转换到原始图像坐标
      const scaleX = naturalWidth / displayWidth;
      const scaleY = naturalHeight / displayHeight;
      const actualX = Math.round(imageX * scaleX);
      const actualY = Math.round(imageY * scaleY);
      
      // 最后验证：确保坐标在原始图像范围内
      const clampedX = Math.max(0, Math.min(actualX, naturalWidth - 1));
      const clampedY = Math.max(0, Math.min(actualY, naturalHeight - 1));
      
      // 检查是否发生了 clamp（说明坐标有问题）
      if (clampedX !== actualX || clampedY !== actualY) {
        console.warn('⚠️ Coordinates were clamped:', {
          actual: {x: actualX, y: actualY},
          clamped: {x: clampedX, y: clampedY}
        });
      }
      
      console.log('✅ Image clicked:', {
        display: {x: imageX, y: imageY, w: displayWidth, h: displayHeight},
        actual: {x: actualX, y: actualY},
        clamped: {x: clampedX, y: clampedY},
        scale: {x: scaleX, y: scaleY},
        imageSize: {w: naturalWidth, h: naturalHeight}
      });
      Logger.info(`点击位置: (${clampedX}, ${clampedY}) [显示: ${imageX.toFixed(1)}, ${imageY.toFixed(1)}]`);
      
      // 绘制点击标记（视觉反馈）
      drawClickMarker(previewOrig, clampedX, clampedY, imageX, imageY);
      
      // Add to click points
      mlState.clickPoints.push({
        x: clampedX, 
        y: clampedY, 
        displayX: imageX, 
        displayY: imageY,
        originalWidth: naturalWidth,
        originalHeight: naturalHeight
      });
      updateClickCount();
      
      if (clearClicksBtn) {
        clearClicksBtn.disabled = false;
      }
      
      // Call API to segment from click (传递原始尺寸)
      await performClickSegmentation(clampedX, clampedY, naturalWidth, naturalHeight);
    };
    
    // 添加鼠标悬停坐标显示
    let coordDisplay = document.getElementById('coordDisplay');
    if (!coordDisplay) {
      coordDisplay = document.createElement('div');
      coordDisplay.id = 'coordDisplay';
      coordDisplay.style.cssText = `
        position: fixed;
        background: rgba(0, 0, 0, 0.85);
        color: #00ff00;
        padding: 6px 12px;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
        font-size: 12px;
        font-weight: bold;
        pointer-events: none;
        z-index: 1000;
        display: none;
        border: 1px solid #00ff00;
        box-shadow: 0 2px 8px rgba(0, 255, 0, 0.3);
      `;
      document.body.appendChild(coordDisplay);
    }
    
    // 关键修复：监听容器而不是图像元素
    const imageWrapper = previewOrig.parentElement;
    
    imageWrapper.addEventListener('click', handleImageClick);
    
    imageWrapper.addEventListener('mousemove', (e) => {
      if (mlState.currentMode !== 'click') {
        coordDisplay.style.display = 'none';
        return;
      }
      
      if (!previewOrig.naturalWidth || !previewOrig.naturalHeight) {
        coordDisplay.style.display = 'none';
        return;
      }
      
      // 直接使用 img 的 boundingRect
      const imgRect = previewOrig.getBoundingClientRect();
      const imageX = e.clientX - imgRect.left;
      const imageY = e.clientY - imgRect.top;
      const displayWidth = imgRect.width;
      const displayHeight = imgRect.height;
      
      if (imageX >= 0 && imageX < displayWidth && imageY >= 0 && imageY < displayHeight) {
        const scaleX = previewOrig.naturalWidth / displayWidth;
        const scaleY = previewOrig.naturalHeight / displayHeight;
        const actualX = Math.round(imageX * scaleX);
        const actualY = Math.round(imageY * scaleY);
        
        coordDisplay.textContent = `坐标: (${actualX}, ${actualY})`;
        coordDisplay.style.display = 'block';
        coordDisplay.style.left = (e.clientX + 15) + 'px';
        coordDisplay.style.top = (e.clientY + 15) + 'px';
        coordDisplay.style.color = '#00ff00';
        coordDisplay.style.borderColor = '#00ff00';
        
        // 改变光标样式表示可点击
        imageWrapper.style.cursor = 'crosshair';
      } else {
        // 在图像外部，显示警告
        coordDisplay.textContent = '⚠️ 图像外部';
        coordDisplay.style.display = 'block';
        coordDisplay.style.left = (e.clientX + 15) + 'px';
        coordDisplay.style.top = (e.clientY + 15) + 'px';
        coordDisplay.style.color = '#ff6b6b';
        coordDisplay.style.borderColor = '#ff6b6b';
        
        // 改变光标样式表示不可点击
        imageWrapper.style.cursor = 'not-allowed';
      }
    });
    
    imageWrapper.addEventListener('mouseleave', () => {
      coordDisplay.style.display = 'none';
      imageWrapper.style.cursor = 'default';
    });
    
    // Update cursor when mode changes
    const originalSwitchMode = switchMode;
    switchMode = function(mode) {
      originalSwitchMode(mode);
      const imageWrapper = previewOrig ? previewOrig.parentElement : null;
      if (imageWrapper) {
        imageWrapper.style.cursor = mode === 'click' ? 'crosshair' : 'default';
      }
    };
  }
  
  // Perform click-based segmentation
  async function performClickSegmentation(x, y, originalWidth, originalHeight) {
    const fileInput = $('fileInput');
    if (!fileInput.files.length) {
      showToast('请先上传图像', 'warning');
      return;
    }
    
    Logger.info('开始点击分割...', `原始坐标: (${x}, ${y}), 原始尺寸: ${originalWidth}x${originalHeight}`);
    
    // 显示加载状态
    const previewMain = $('previewMain');
    const skeletonMain = $('skeletonMain');
    if (skeletonMain) skeletonMain.style.display = 'block';
    
    const startTime = performance.now();
    
    try {
      const formData = new FormData();
      formData.append('file', fileInput.files[0]);
      formData.append('click_x', x);
      formData.append('click_y', y);
      formData.append('original_width', originalWidth);
      formData.append('original_height', originalHeight);
      formData.append('max_side', $('max_side').value);
      
      if (mlState.accumulatedMaskB64) {
        formData.append('accumulated_mask_b64', mlState.accumulatedMaskB64);
      }
      
      Logger.info('发送 API 请求', `max_side: ${$('max_side').value}`);
      
      const response = await fetch('/api/ml/click-segment', {
        method: 'POST',
        body: formData
      });
      
      const result = await response.json();
      const duration = ((performance.now() - startTime) / 1000).toFixed(2);
      
      if (result.ok) {
        // 保存累积 mask（后端已合并）
        mlState.accumulatedMaskB64 = result.mask_b64;
        
        // 保存到全局状态
        state.lastOverlayB64 = result.overlay_b64;
        state.lastMaskB64 = result.mask_b64;
        
        // 更新主显示（叠加图）
        const previewMain = $('previewMain');
        if (previewMain && result.overlay_b64) {
          previewMain.src = 'data:image/png;base64,' + result.overlay_b64;
          previewMain.style.display = 'block';
          
          // 隐藏骨架屏
          const skeletonMain = $('skeletonMain');
          if (skeletonMain) skeletonMain.style.display = 'none';
        }
        
        // 启用下载按钮
        const dlOverlay = $('dlOverlay');
        const dlMask = $('dlMask');
        if (dlOverlay) dlOverlay.disabled = false;
        if (dlMask) dlMask.disabled = false;
        
        const debugInfo = result.debug_info || {};
        
        Logger.success('点击分割完成', 
          `坐标: (${x}, ${y}), ` +
          `图像尺寸: ${originalWidth}x${originalHeight}, ` +
          `grow_T: ${result.parameters_used.grow_T.toFixed(1)}, ` +
          `耗时: ${duration}s, ` +
          `置信度: ${(result.confidence * 100).toFixed(1)}%`);
        showToast(`分割完成 (${duration}s)`, 'success');
      } else {
        throw new Error(result.error || '分割失败');
      }
    } catch (error) {
      Logger.error('点击分割失败', error.message);
      showToast('分割失败: ' + error.message, 'error');
    }
  }
  
  // Initialize click mode interaction after a short delay to ensure DOM is ready
  setTimeout(setupClickModeInteraction, 100);
  
  // 注意：fileInput 的 change 监听器已在前面设置，这里不需要重复
  
  // Restore saved mode
  const savedMode = localStorage.getItem('mlMode');
  if (savedMode && ['manual', 'smart', 'click'].includes(savedMode)) {
    switchMode(savedMode);
  }
  
  Logger.info('ML 模式功能已初始化');
}

// 立即初始化 ML 模式（与 initDebugPanel 保持一致）
initMLMode();
