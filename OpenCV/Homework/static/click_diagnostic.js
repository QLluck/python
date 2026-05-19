// 点击坐标诊断工具
// 在浏览器控制台运行：复制粘贴此脚本全部内容
//
// 功能：
// 1. 在图像上放置一个红色十字标记（显示你点击的位置）
// 2. 在图像四角和中心放置蓝色校准点
// 3. 对比 imgRect 方法 vs containerOffset 方法的坐标差异
// 4. 创建一个 1px 精度的画布覆盖层来可视化偏差

(function() {
  'use strict';

  const img = document.getElementById('previewOrig');
  if (!img || !img.naturalWidth) {
    console.error('请先上传并加载一张图像');
    return;
  }

  const wrapper = img.parentElement;

  // 移除之前的诊断覆盖层
  const oldCanvas = document.getElementById('diagCanvas');
  if (oldCanvas) oldCanvas.remove();
  const oldPanel = document.getElementById('diagPanel');
  if (oldPanel) oldPanel.remove();

  // 创建诊断 canvas
  const canvas = document.createElement('canvas');
  canvas.id = 'diagCanvas';
  canvas.style.cssText = 'position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:50;';
  wrapper.appendChild(canvas);

  // 创建信息面板
  const panel = document.createElement('div');
  panel.id = 'diagPanel';
  panel.style.cssText = `
    position:fixed; bottom:20px; left:20px; z-index:10000;
    background:rgba(0,0,0,0.95); color:#0f0; padding:16px;
    font:12px/1.6 monospace; border-radius:8px; max-width:520px;
    border:1px solid #0f0; max-height:80vh; overflow-y:auto;
  `;
  document.body.appendChild(panel);

  function measure() {
    const imgRect = img.getBoundingClientRect();
    const wrapperRect = wrapper.getBoundingClientRect();
    const cs = getComputedStyle(img);

    return {
      // img 元素
      imgRect,
      imgClientW: img.clientWidth,
      imgClientH: img.clientHeight,
      imgOffsetW: img.offsetWidth,
      imgOffsetH: img.offsetHeight,
      imgNaturalW: img.naturalWidth,
      imgNaturalH: img.naturalHeight,
      imgComputedW: parseFloat(cs.width),
      imgComputedH: parseFloat(cs.height),
      imgObjectFit: cs.objectFit,
      imgObjectPosition: cs.objectPosition,

      // 容器
      wrapperRect,
      wrapperClientW: wrapper.clientWidth,
      wrapperClientH: wrapper.clientHeight,

      // 偏移
      imgOffsetInWrapper: {
        left: imgRect.left - wrapperRect.left,
        top: imgRect.top - wrapperRect.top,
      },

      // 缩放比
      scaleX_rect: img.naturalWidth / imgRect.width,
      scaleY_rect: img.naturalHeight / imgRect.height,
      scaleX_client: img.naturalWidth / img.clientWidth,
      scaleY_client: img.naturalHeight / img.clientHeight,
    };
  }

  function drawCalibration() {
    const m = measure();
    const wrapperRect = m.wrapperRect;

    canvas.width = wrapperRect.width;
    canvas.height = wrapperRect.height;

    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // img 在 wrapper 中的位置
    const ox = m.imgOffsetInWrapper.left;
    const oy = m.imgOffsetInWrapper.top;
    const dw = m.imgRect.width;
    const dh = m.imgRect.height;

    // 绘制 img boundingRect 边界（绿色虚线）
    ctx.strokeStyle = 'rgba(0,255,0,0.6)';
    ctx.lineWidth = 1;
    ctx.setLineDash([4, 4]);
    ctx.strokeRect(ox + 0.5, oy + 0.5, dw - 1, dh - 1);
    ctx.setLineDash([]);

    // 用 clientWidth 方法算的边界（黄色虚线）
    const ox2 = (wrapperRect.width - m.imgClientW) / 2;
    const oy2 = (wrapperRect.height - m.imgClientH) / 2;
    ctx.strokeStyle = 'rgba(255,255,0,0.6)';
    ctx.setLineDash([2, 6]);
    ctx.strokeRect(ox2 + 0.5, oy2 + 0.5, m.imgClientW - 1, m.imgClientH - 1);
    ctx.setLineDash([]);

    // 校准点：四角 + 中心（蓝色）
    const calibPoints = [
      { name: 'TL', dx: 0, dy: 0 },
      { name: 'TR', dx: dw, dy: 0 },
      { name: 'BL', dx: 0, dy: dh },
      { name: 'BR', dx: dw, dy: dh },
      { name: 'C',  dx: dw / 2, dy: dh / 2 },
    ];

    ctx.font = 'bold 10px monospace';
    calibPoints.forEach(p => {
      const cx = ox + p.dx;
      const cy = oy + p.dy;
      ctx.fillStyle = '#00aaff';
      ctx.beginPath();
      ctx.arc(cx, cy, 4, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillText(p.name, cx + 6, cy - 4);
    });

    // 差异箭头（如果两种方法有差异）
    const diffX = Math.abs(ox - ox2);
    const diffY = Math.abs(oy - oy2);
    if (diffX > 0.5 || diffY > 0.5) {
      ctx.strokeStyle = '#ff0000';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(ox2 + dw / 2, oy2);
      ctx.lineTo(ox + dw / 2, oy);
      ctx.stroke();

      ctx.fillStyle = '#ff0000';
      ctx.font = 'bold 11px monospace';
      ctx.fillText(`差异: dx=${(ox - ox2).toFixed(1)} dy=${(oy - oy2).toFixed(1)}`, 10, 15);
    }
  }

  function showInfo(clickInfo) {
    const m = measure();
    let html = '<b style="color:#0ff">== 坐标诊断 ==</b><br><br>';

    html += '<b>图像尺寸:</b><br>';
    html += `  natural: ${m.imgNaturalW} x ${m.imgNaturalH}<br>`;
    html += `  imgRect: ${m.imgRect.width.toFixed(1)} x ${m.imgRect.height.toFixed(1)}<br>`;
    html += `  client:  ${m.imgClientW} x ${m.imgClientH}<br>`;
    html += `  offset:  ${m.imgOffsetW} x ${m.imgOffsetH}<br>`;
    html += `  computed: ${m.imgComputedW.toFixed(1)} x ${m.imgComputedH.toFixed(1)}<br>`;
    html += `  object-fit: ${m.imgObjectFit}<br>`;
    html += `  object-position: ${m.imgObjectPosition}<br><br>`;

    // 检查 object-fit: contain 是否引起内部缩放
    const naturalRatio = m.imgNaturalW / m.imgNaturalH;
    const elementRatio = m.imgRect.width / m.imgRect.height;
    const ratioDiff = Math.abs(naturalRatio - elementRatio);
    if (ratioDiff > 0.01) {
      html += `<b style="color:#f00">!! object-fit 内部缩放 !!</b><br>`;
      html += `  图像宽高比: ${naturalRatio.toFixed(3)}<br>`;
      html += `  元素宽高比: ${elementRatio.toFixed(3)}<br>`;
      html += `  差异: ${ratioDiff.toFixed(3)}<br>`;
      html += `  <span style="color:#ff0">这意味着 imgRect 不等于实际渲染区域！</span><br>`;
      html += `  <span style="color:#ff0">object-fit:contain 在元素内部再次缩放了图像。</span><br>`;

      // 计算实际渲染区域
      let renderW, renderH;
      if (naturalRatio > elementRatio) {
        renderW = m.imgRect.width;
        renderH = m.imgRect.width / naturalRatio;
      } else {
        renderH = m.imgRect.height;
        renderW = m.imgRect.height * naturalRatio;
      }
      const padX = (m.imgRect.width - renderW) / 2;
      const padY = (m.imgRect.height - renderH) / 2;
      html += `  实际渲染: ${renderW.toFixed(1)} x ${renderH.toFixed(1)}<br>`;
      html += `  内部偏移: padX=${padX.toFixed(1)} padY=${padY.toFixed(1)}<br><br>`;
    } else {
      html += '<span style="color:#0f0">object-fit 未引起额外缩放 (宽高比一致)</span><br><br>';
    }

    html += '<b>容器尺寸:</b><br>';
    html += `  wrapperRect: ${m.wrapperRect.width.toFixed(1)} x ${m.wrapperRect.height.toFixed(1)}<br>`;
    html += `  wrapperClient: ${m.wrapperClientW} x ${m.wrapperClientH}<br><br>`;

    html += '<b>偏移:</b><br>';
    html += `  imgRect法:  left=${m.imgOffsetInWrapper.left.toFixed(1)} top=${m.imgOffsetInWrapper.top.toFixed(1)}<br>`;
    const ox2 = (m.wrapperRect.width - m.imgClientW) / 2;
    const oy2 = (m.wrapperRect.height - m.imgClientH) / 2;
    html += `  container法: left=${ox2.toFixed(1)} top=${oy2.toFixed(1)}<br>`;
    const diffX = m.imgOffsetInWrapper.left - ox2;
    const diffY = m.imgOffsetInWrapper.top - oy2;
    if (Math.abs(diffX) > 0.1 || Math.abs(diffY) > 0.1) {
      html += `  <span style="color:#ff0">差异: dx=${diffX.toFixed(1)} dy=${diffY.toFixed(1)}</span><br>`;
    }
    html += '<br>';

    html += '<b>缩放比:</b><br>';
    html += `  imgRect法:  scaleX=${m.scaleX_rect.toFixed(4)} scaleY=${m.scaleY_rect.toFixed(4)}<br>`;
    html += `  client法:   scaleX=${m.scaleX_client.toFixed(4)} scaleY=${m.scaleY_client.toFixed(4)}<br>`;
    if (Math.abs(m.scaleX_rect - m.scaleY_rect) > 0.01) {
      html += `  <span style="color:#f00">!! scaleX != scaleY（图像变形或坐标不准）</span><br>`;
    }
    html += '<br>';

    if (clickInfo) {
      html += '<b style="color:#0ff">最近一次点击:</b><br>';
      html += `  clientX/Y: ${clickInfo.clientX}, ${clickInfo.clientY}<br>`;
      html += `  imgRect法坐标: (${clickInfo.imgRectX.toFixed(1)}, ${clickInfo.imgRectY.toFixed(1)})<br>`;
      html += `  原图坐标(imgRect): (${clickInfo.actualX_rect}, ${clickInfo.actualY_rect})<br>`;

      if (ratioDiff > 0.01) {
        html += `  <span style="color:#ff0">原图坐标(修正后): (${clickInfo.correctedX}, ${clickInfo.correctedY})</span><br>`;
        html += `  <span style="color:#f00">偏差: dx=${clickInfo.correctedX - clickInfo.actualX_rect}, dy=${clickInfo.correctedY - clickInfo.actualY_rect}</span><br>`;
      }
    }

    html += '<br><span style="color:#888">点击图像任意位置查看坐标</span><br>';
    html += '<span style="color:#888">绿框=imgRect  黄框=clientWidth法</span>';

    panel.innerHTML = html;
  }

  // 点击处理
  wrapper.addEventListener('click', function handler(e) {
    const m = measure();
    const imgRect = m.imgRect;

    const imgRectX = e.clientX - imgRect.left;
    const imgRectY = e.clientY - imgRect.top;

    const actualX_rect = Math.round(imgRectX * m.scaleX_rect);
    const actualY_rect = Math.round(imgRectY * m.scaleY_rect);

    // 检查 object-fit 内部缩放并修正
    const naturalRatio = m.imgNaturalW / m.imgNaturalH;
    const elementRatio = imgRect.width / imgRect.height;
    let correctedX = actualX_rect;
    let correctedY = actualY_rect;

    if (Math.abs(naturalRatio - elementRatio) > 0.01) {
      let renderW, renderH, padX, padY;
      if (naturalRatio > elementRatio) {
        renderW = imgRect.width;
        renderH = imgRect.width / naturalRatio;
      } else {
        renderH = imgRect.height;
        renderW = imgRect.height * naturalRatio;
      }
      padX = (imgRect.width - renderW) / 2;
      padY = (imgRect.height - renderH) / 2;

      const correctedDisplayX = imgRectX - padX;
      const correctedDisplayY = imgRectY - padY;
      const correctedScaleX = m.imgNaturalW / renderW;
      const correctedScaleY = m.imgNaturalH / renderH;
      correctedX = Math.round(correctedDisplayX * correctedScaleX);
      correctedY = Math.round(correctedDisplayY * correctedScaleY);
    }

    // 在 canvas 上画红色十字
    drawCalibration();
    const ctx = canvas.getContext('2d');
    const ox = m.imgOffsetInWrapper.left;
    const oy = m.imgOffsetInWrapper.top;
    const cx = ox + imgRectX;
    const cy = oy + imgRectY;

    ctx.strokeStyle = '#ff0000';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(cx - 12, cy); ctx.lineTo(cx + 12, cy);
    ctx.moveTo(cx, cy - 12); ctx.lineTo(cx, cy + 12);
    ctx.stroke();
    ctx.fillStyle = '#ff0000';
    ctx.beginPath();
    ctx.arc(cx, cy, 3, 0, Math.PI * 2);
    ctx.fill();

    ctx.font = 'bold 11px monospace';
    ctx.fillStyle = '#ff0000';
    ctx.fillText(`(${correctedX}, ${correctedY})`, cx + 14, cy - 6);

    showInfo({
      clientX: e.clientX,
      clientY: e.clientY,
      imgRectX,
      imgRectY,
      actualX_rect,
      actualY_rect,
      correctedX,
      correctedY,
    });

    console.log('DIAG click:', {
      imgRectX: imgRectX.toFixed(2),
      imgRectY: imgRectY.toFixed(2),
      actualX_rect,
      actualY_rect,
      correctedX,
      correctedY,
      scaleX: m.scaleX_rect.toFixed(4),
      scaleY: m.scaleY_rect.toFixed(4),
      naturalRatio: naturalRatio.toFixed(4),
      elementRatio: elementRatio.toFixed(4),
    });
  }, true); // capture phase to run before app click handler

  // 初始绘制
  drawCalibration();
  showInfo(null);

  console.log('%c诊断工具已启动', 'color:#0f0;font-weight:bold;font-size:14px');
  console.log('点击图像任意位置查看坐标诊断');
  console.log('移除诊断: document.getElementById("diagCanvas").remove(); document.getElementById("diagPanel").remove();');
})();
