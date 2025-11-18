// resultados.js
// Este script carga y muestra los resultados del inventario desde la base de datos

async function fetchResultados() {
    // Usamos una API local o endpoint Python (por ejemplo, con Flask o FastAPI)
    // Aquí se asume que existe un endpoint /api/resultados que devuelve los datos en JSON
    try {
        const response = await fetch('http://localhost:5000/api/resultados');
        if (!response.ok) throw new Error('No se pudo obtener resultados');
        const data = await response.json();
        renderResultados(data);
    } catch (err) {
        document.getElementById('resultados').innerHTML = '<div style="color:red">Error al cargar resultados</div>';
    }
}

function renderResultados(items) {
    if (!items.length) {
        document.getElementById('resultados').innerHTML = '<em>No hay resultados para mostrar.</em>';
        return;
    }
    let html = `<table border="1" cellpadding="8" style="border-collapse:collapse; width:100%">\n`;
    html += `<tr><th>ID</th><th>Responsable</th><th>Marca</th><th>Equipo</th><th>Serie</th><th>Fecha Ingreso</th><th>Fecha Salida</th><th>Proceso</th><th>Valor</th><th>Observaciones</th><th>Estado</th><th>Progreso</th></tr>`;
    for (const item of items) {
        html += `<tr>`;
        html += `<td>${item.id}</td>`;
        html += `<td>${item.responsable}</td>`;
        html += `<td>${item.marca}</td>`;
        html += `<td>${item.equipo}</td>`;
        html += `<td>${item.serie || ''}</td>`;
        html += `<td>${item.fecha_ingreso || ''}</td>`;
        html += `<td>${item.fecha_salida || ''}</td>`;
        html += `<td>${item.proceso || ''}</td>`;
        html += `<td>${item.valor || ''}</td>`;
        html += `<td>${item.observaciones || ''}</td>`;
        html += `<td>${item.estado || ''}</td>`;
        html += `<td>${item.progreso != null ? item.progreso + '%' : ''}</td>`;
        html += `</tr>`;
    }
    html += `</table>`;
    document.getElementById('resultados').innerHTML = html;
}

fetchResultados();
