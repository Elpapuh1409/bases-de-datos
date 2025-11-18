/**
 * qr-scanner.js - Lógica para captura de video y decodificación QR
 * Usa jsQR (detección por JavaScript) para decodificar códigos QR desde video
 */

// Cargar jsQR dinámicamente
const script = document.createElement('script');
script.src = 'https://cdn.jsdelivr.net/npm/jsqr@1.10.0/dist/jsQR.js';
document.head.appendChild(script);

const video = document.getElementById('qr-video');
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');
let stream = null;
let animationId = null;
let scannedCodes = [];

async function startLocalCamera() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ 
            video: { facingMode: 'environment' } 
        });
        video.srcObject = stream;
        video.play();
        scanQR();
    } catch (err) {
        alert('Error al acceder a la cámara: ' + err.message);
        console.error(err);
    }
}

function startRemoteStream(url) {
    video.src = url;
    video.crossOrigin = 'anonymous';
    video.play().catch(err => {
        alert('Error al reproducir stream: ' + err.message);
    });
    scanQR();
}

function stopStream() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
    if (video.src) video.src = '';
    if (video.srcObject) video.srcObject = null;
    if (animationId) cancelAnimationFrame(animationId);
}

function scanQR() {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    if (canvas.width === 0) {
        // Video aún no cargado, reintentar
        animationId = requestAnimationFrame(scanQR);
        return;
    }
    
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Aplicar espejo si está habilitado
    if (document.getElementById('mirror').checked) {
        ctx.save();
        ctx.translate(canvas.width, 0);
        ctx.scale(-1, 1);
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        ctx.restore();
    }
    
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    
    // jsQR devuelve null si no detecta código
    if (typeof jsQR !== 'undefined') {
        const code = jsQR(imageData.data, imageData.width, imageData.height);
        
        if (code) {
            const data = code.data;
            addScannedCode(data);
            
            // Dibujar caja alrededor del QR si está habilitado
            if (document.getElementById('draw-bbox').checked && code.location) {
                drawBoundingBox(code.location);
            }
        }
    }
    
    animationId = requestAnimationFrame(scanQR);
}

function drawBoundingBox(location) {
    const { topLeftCorner, topRightCorner, bottomLeftCorner, bottomRightCorner } = location;
    ctx.strokeStyle = '#f50';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(topLeftCorner.x, topLeftCorner.y);
    ctx.lineTo(topRightCorner.x, topRightCorner.y);
    ctx.lineTo(bottomRightCorner.x, bottomRightCorner.y);
    ctx.lineTo(bottomLeftCorner.x, bottomLeftCorner.y);
    ctx.closePath();
    ctx.stroke();
}

function addScannedCode(code) {
    // Evitar duplicados en corto tiempo (2 segundos)
    const lastCode = scannedCodes[scannedCodes.length - 1];
    if (lastCode && lastCode.code === code && (Date.now() - lastCode.timestamp) < 2000) {
        return;
    }
    
    const now = new Date().toLocaleTimeString();
    const item = { code, time: now, timestamp: Date.now() };
    scannedCodes.push(item);
    
    const tbody = document.getElementById('results-tbody');
    const row = tbody.insertRow(0);
    row.innerHTML = `
        <td style="word-break: break-all;">${code}</td>
        <td>${now}</td>
        <td><span class="badge">✓ Detectado</span></td>
    `;
    
    // Mantener solo últimas 30 filas
    while (tbody.rows.length > 30) {
        tbody.deleteRow(tbody.rows.length - 1);
    }
    
    console.log('QR detectado:', code);
}

// Eventos de interfaz
document.getElementById('start-btn').addEventListener('click', function() {
    const source = document.querySelector('input[name="source"]:checked').value;
    const url = source === 'remote' ? document.getElementById('remote-url').value : null;
    
    if (source === 'remote' && !url) {
        alert('Ingresa una URL válida.');
        return;
    }
    
    stopStream();
    
    if (source === 'local') {
        startLocalCamera();
    } else {
        startRemoteStream(url);
    }
    
    this.disabled = true;
    document.getElementById('stop-btn').disabled = false;
});

document.getElementById('stop-btn').addEventListener('click', function() {
    stopStream();
    this.disabled = true;
    document.getElementById('start-btn').disabled = false;
});

document.getElementById('export-btn').addEventListener('click', function() {
    if (scannedCodes.length === 0) {
        alert('No hay códigos escaneados aún.');
        return;
    }
    
    let csv = 'Código,Hora\n';
    scannedCodes.forEach(item => {
        csv += `"${item.code}","${item.time}"\n`;
    });
    
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.href = url;
    link.download = `escaneos-${new Date().toISOString().split('T')[0]}.csv`;
    link.click();
});

document.getElementById('clear-btn').addEventListener('click', function() {
    if (confirm('¿Limpiar todos los escaneos?')) {
        scannedCodes = [];
        document.getElementById('results-tbody').innerHTML = '';
    }
});

// Selección de fuente
document.querySelectorAll('input[name="source"]').forEach(radio => {
    radio.addEventListener('change', function() {
        document.getElementById('remote-input').hidden = this.value !== 'remote';
    });
});

console.log('qr-scanner.js cargado correctamente.');
