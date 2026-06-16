let cameraActive = false;
let frameUpdateInterval = null;
let statusUpdateInterval = null;
const FPS_CALCULATE_INTERVAL = 1000;
let lastFrameTime = Date.now();
let frameCount = 0;
let fps = 0;

const elements = {
    canvas: document.getElementById('canvas-frame'),
    loading: document.getElementById('loading'),
    startBtn: document.getElementById('start-btn'),
    stopBtn: document.getElementById('stop-btn'),
    clearBtn: document.getElementById('clear-btn'),
    saveBtn: document.getElementById('save-btn'),
    colorSelect: document.getElementById('color-select'),
    brushSize: document.getElementById('brush-size'),
    sizeValue: document.getElementById('size-value'),
    statusMode: document.getElementById('status-mode'),
    statusColor: document.getElementById('status-color'),
    statusSize: document.getElementById('status-size'),
    statusFps: document.getElementById('status-fps')
};

elements.startBtn.addEventListener('click', startCamera);
elements.stopBtn.addEventListener('click', stopCamera);
elements.clearBtn.addEventListener('click', clearCanvas);
elements.saveBtn.addEventListener('click', saveDrawing);
elements.colorSelect.addEventListener('change', changeColor);
elements.brushSize.addEventListener('input', changeBrushSize);

async function startCamera() {
    try {
        showLoading(true);
        const response = await fetch('/api/start-camera', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        const data = await response.json();
        if (data.status === 'success') {
            cameraActive = true;
            updateUIState();
            frameUpdateInterval = setInterval(updateFrame, 100);
            statusUpdateInterval = setInterval(updateStatus, 500);
            showLoading(false);
        } else {
            alert('Error: ' + data.message);
            showLoading(false);
        }
    } catch (error) {
        console.error('Error starting camera:', error);
        alert('Failed to start camera');
        showLoading(false);
    }
}

async function stopCamera() {
    try {
        const response = await fetch('/api/stop-camera', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        if (response.ok) {
            cameraActive = false;
            clearInterval(frameUpdateInterval);
            clearInterval(statusUpdateInterval);
            updateUIState();
            elements.canvas.src = '';
        }
    } catch (error) {
        console.error('Error stopping camera:', error);
    }
}

async function updateFrame() {
    try {
        const response = await fetch('/api/get-frame');
        const data = await response.json();
        if (data.frame) {
            elements.canvas.src = 'data:image/jpeg;base64,' + data.frame;
            frameCount++;
            const currentTime = Date.now();
            if (currentTime - lastFrameTime >= FPS_CALCULATE_INTERVAL) {
                fps = (frameCount * 1000) / (currentTime - lastFrameTime);
                frameCount = 0;
                lastFrameTime = currentTime;
                elements.statusFps.textContent = fps.toFixed(1);
            }
        }
    } catch (error) {
        console.error('Error updating frame:', error);
    }
}

async function updateStatus() {
    try {
        const response = await fetch('/api/get-status');
        const data = await response.json();
        elements.statusMode.textContent = data.mode;
        elements.statusColor.textContent = data.color;
        elements.statusSize.textContent = data.brush_size;
    } catch (error) {
        console.error('Error updating status:', error);
    }
}

async function changeColor(event) {
    const color = event.target.value;
    try {
        const response = await fetch('/api/set-color', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ color: color })
        });
        const data = await response.json();
        if (data.status === 'success') {
            elements.statusColor.textContent = color;
        }
    } catch (error) {
        console.error('Error changing color:', error);
    }
}

async function changeBrushSize(event) {
    const size = parseInt(event.target.value);
    elements.sizeValue.textContent = size;
    try {
        const response = await fetch('/api/set-brush-size', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ size: size })
        });
        const data = await response.json();
        if (data.status === 'success') {
            elements.statusSize.textContent = size;
        }
    } catch (error) {
        console.error('Error changing brush size:', error);
    }
}

async function clearCanvas() {
    if (confirm('Are you sure you want to clear the canvas?')) {
        try {
            const response = await fetch('/api/clear-canvas', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            if (response.ok) {
                console.log('Canvas cleared');
            }
        } catch (error) {
            console.error('Error clearing canvas:', error);
        }
    }
}

async function saveDrawing() {
    try {
        showLoading(true);
        const response = await fetch('/api/save-drawing', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        const data = await response.json();
        if (data.status === 'success') {
            const imageResponse = await fetch('/api/get-drawing-image');
            const blob = await imageResponse.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = data.filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            alert('Drawing saved successfully!');
        } else {
            alert('Error: ' + data.message);
        }
        showLoading(false);
    } catch (error) {
        console.error('Error saving drawing:', error);
        alert('Failed to save drawing');
        showLoading(false);
    }
}

function updateUIState() {
    const disabled = !cameraActive;
    elements.startBtn.disabled = !disabled;
    elements.stopBtn.disabled = disabled;
    elements.clearBtn.disabled = disabled;
    elements.saveBtn.disabled = disabled;
    elements.colorSelect.disabled = disabled;
    elements.brushSize.disabled = disabled;
}

function showLoading(show) {
    if (show) {
        elements.loading.classList.add('active');
    } else {
        elements.loading.classList.remove('active');
    }
}

updateUIState();