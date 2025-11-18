# INSTRUCCIONES FINALES - Sistema de Lectura QR Win Sports

## Estado del Proyecto: COMPLETO

Tu sistema de lectura QR con interfaz web profesional está listo para usar.

---

## Diseño Implementado

**Paleta de Colores Win Sports:**
- **Blanco** (#ffffff) - Fondo y tarjetas
- **Negro** (#000000) - Texto y headers
- **Naranja** (#f50) - Acento primario
- **Morado** (#d839ff) - Acento secundario

**Elementos Visuales:**
- Headers sticky con navegación
- Buttons con hover effects
- Cards con sombras y transiciones
- Grid layouts responsive
- Tipografía premium (Segoe UI, Roboto)
- Animaciones suaves

---

## Archivos Principales

```
Tu Carpeta/
├── Pantalla_Inicial.html      ← ABRE AQUÍ (página principal)
├── usos.html                   ← Guía completa
├── lector_qr.html              ← Interfaz web del lector
├── lector_qr.py                ← Script Python (CLI)
├── qr-scanner.js               ← Lógica JavaScript
├── styles.css                  ← Estilos compartidos
├── test_qr_scanner.py          ← Script de prueba
└── README_COMPLETO.md          ← Documentación completa
```

---

## Cómo Empezar

### Opción 1: Interfaz Web (Recomendado para principiantes)

**Paso 1:** Abre `Pantalla_Inicial.html` en tu navegador
```
Doble clic en el archivo → Se abre automáticamente
o
Arrastra al navegador
```

**Paso 2:** Haz clic en "Abrir Lector QR"

**Paso 3:** En `lector_qr.html`:
- Selecciona fuente (cámara local o remota)
- Presiona "Iniciar lectura"
- Muestra un código QR frente a la cámara
- Los resultados aparecen en la tabla
- Presiona "Descargar CSV" para guardar

---

### Opción 2: Línea de Comandos (Más control)

**Paso 1:** Activa el entorno virtual
```powershell
. .\mi_inventario_env\Scripts\Activate.ps1
```

**Paso 2:** Ejecuta comandos

```powershell
# Cámara local
python .\lector_qr.py

# Cámara remota
python .\lector_qr.py --source "http://192.168.1.42:8080/video"

# Imagen
python .\lector_qr.py --image ./qr.png

# Exportar a CSV
python .\lector_qr.py --camera 0 --output resultados.csv

# Ver ayuda
python .\lector_qr.py --help
```

---

### Opción 3: Usar Móvil como Cámara

**En el Móvil:**
1. Descarga "IP Webcam" (Google Play / App Store)
2. Abre la app
3. Conecta a tu red Wi-Fi
4. Presiona "Start Server"
5. Copia la URL que aparece (ej: http://192.168.1.42:8080)

**En la PC:**

```powershell
python .\lector_qr.py --source "http://192.168.1.42:8080/video"
```

O en la web: `lector_qr.html` → Selecciona "Fuente remota" → Pega la URL → "Iniciar lectura"

---

## Páginas Web

### `Pantalla_Inicial.html` - Página Principal
- Tabla de inventario
- Botón para abrir lector
- Enlace a guía de uso
- Información sobre el sistema
- **Colores:** Blanco (fondo), Negro (texto), Naranja (botones primarios), Morado (hover)

### `usos.html` - Guía Completa
- 6 pasos visuales interactivos
- Comando PowerShell
- Opciones disponibles
- Funcionalidades principales
- Solución de problemas
- **Elementos:** Step cards, Code boxes, Feature grid

### `lector_qr.html` - Escáner Web
- Selector de fuente (local/remota)
- Vista previa de video
- Tabla de resultados
- Controles (espejo, mostrar caja)
- Botones (Descargar CSV, Limpiar)
- Instrucciones

---

## Scripts Python

### `lector_qr.py` - Motor Principal
```bash
# Ver ayuda
python lector_qr.py --help

# Usar cámara local
python lector_qr.py

# Stream remoto
python lector_qr.py --source "URL"

# Imagen
python lector_qr.py --image archivo.png

# Exportar directamente
python lector_qr.py --camera 0 --output datos.csv
```

### `test_qr_scanner.py` - Prueba Funcional
```bash
# Ejecutar prueba (simula 5 escaneos)
python test_qr_scanner.py

# Genera: test_escaneos.csv
```

---

## Controles en Cámara

Cuando ejecutas `lector_qr.py` desde CLI:

| Tecla | Acción |
|---|---|
| `q` | Salir |
| `s` | Guardar captura (captura_TIMESTAMP.png) |

---

## Exportación CSV

Los archivos CSV incluyen:
```csv
código,hora
WS-INV-001-2025,2025-11-12 14:02:22.250
978-3-16-148410-0,2025-11-12 14:02:22.251
```

**Compatible con:** Excel, Google Sheets, Python pandas, etc.

---

## 🔧 Solución Rápida de Problemas

### "No se abre la página"
Haz doble clic en `Pantalla_Inicial.html`

### "Cámara no funciona"
Permite acceso a cámara en permisos del navegador
Verifica que no esté en uso otra aplicación
Prueba `--camera 1` o `--camera 2`

### "Stream remoto no conecta"
Verifica que móvil y PC estén en la misma red Wi-Fi
Prueba la URL en el navegador primero
Usa `/video` o `/mjpegfeed` si `/video` no funciona

### "Python no encontrado"
Activa el virtualenv: `. .\mi_inventario_env\Scripts\Activate.ps1`
Verifica con: `python --version`

---

## Documentación Adicional

- **README_COMPLETO.md** - Guía técnica completa
- **RESUMEN_DISEÑO.md** - Detalles visuales y componentes
- **lector_qr.py** - Código comentado con docstrings

---

## Características del Sistema

**Lectura QR**
- OpenCV + pyzbar (fallback automático)
- Detección de múltiples códigos por frame
- Deduplicación automática

**Fuentes Soportadas**
- Cámara local (índice 0, 1, 2, ...)
- Stream HTTP (IP Webcam, URLs RTSP)
- Análisis de imágenes estáticas

**Exportación**
- CSV con timestamp
- Compatible con bases de datos
- Historial completo

**Interfaz**
- Web moderna y responsive
- CLI para scripts
- Controles intuitivos

**Diseño**
- Paleta Win Sports (blanco, negro, naranja, morado)
- Responsive (mobile, tablet, desktop)
- Animaciones suaves
- Tipografía premium

---

## Ejemplos Reales

### Ejemplo 1: Inventario Diario
```powershell
python .\lector_qr.py --camera 0 --output "inventario_$(Get-Date -f 'yyyyMMdd').csv"
```

### Ejemplo 2: Usar Móvil por 2 Horas
```powershell
python .\lector_qr.py --source "http://192.168.1.42:8080/video" --output "escaneos_movil.csv"
```

### Ejemplo 3: Verificar Imágenes
```powershell
Get-ChildItem *.png | ForEach-Object { python .\lector_qr.py --image $_.Name }
```

---

## Notas Importantes

1. **Primera vez:** Permite acceso a cámara en tu navegador
2. **IP Webcam:** Verifica que ambos dispositivos estén en la misma red
3. **Exportación:** Los datos se guardan en UTF-8 (compatible con Excel)
4. **Seguridad:** No almacena datos personales, solo códigos QR
5. **Offline:** Funciona sin conexión a internet.

---

## ¡Listo!

Tu sistema está completo y listo para usar. 

**Próximos pasos:**
1. Abre `Pantalla_Inicial.html`
2. Haz clic en "Abrir Lector QR"
3. ¡Comienza a escanear!

Para ayuda adicional, consulta `README_COMPLETO.md` o presiona "¿Cómo usar con móvil?" en la página.

---

**© Win Sports 2025** | Sistema de Lectura QR - ¡Listo para Producción!
