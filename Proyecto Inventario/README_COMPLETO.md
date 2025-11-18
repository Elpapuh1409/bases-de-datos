# Guía Completa - Lector QR Win Sports

## 📋 Descripción

Sistema completo de lectura de códigos QR para Win Sports con interfaz web moderna y lógica de Python avanzada. Soporta:

- ✅ Cámara local (índice 0, 1, etc.)
- ✅ Stream remoto (URL HTTP/RTSP desde móvil)
- ✅ Análisis de imágenes
- ✅ Exportación a CSV
- ✅ Interfaz web profesional
- ✅ Decodificación robusto (OpenCV + pyzbar fallback)

---

## 🛠️ Requisitos Previos

**Python 3.8+** con librerías ya instaladas:
```
opencv-python
pyzbar (opcional - para decodificación más rápida)
```

Verifica tu entorno:
```powershell
python -m pip list | findstr opencv
```

---

## 🚀 Instalación Rápida

### 1. Activar el Entorno Virtual

```powershell
# Windows PowerShell
. .\mi_inventario_env\Scripts\Activate.ps1

# Verifica que está activado (deberías ver (mi_inventario_env) al inicio)
```

### 2. (Opcional) Instalar pyzbar en Windows

Si deseas usar `pyzbar` para mejor detección:

```powershell
# Opción A: Via pip (requiere librerías del sistema)
pip install pyzbar

# Opción B: Si falla, usar solo OpenCV (recomendado para Windows)
# El script usa OpenCV automáticamente como fallback
```

---

## 📖 Cómo Usar

### Desde CLI (Línea de Comandos)

#### A. Cámara Local
```powershell
python .\lector_qr.py
```
**Controles:**
- Presiona `q` para salir
- Presiona `s` para guardar una captura (captura_YYYYMMDD_HHMMSS.png)

#### B. Otra Cámara (índice 1, 2, etc.)
```powershell
python .\lector_qr.py --camera 1
```

#### C. Stream Remoto (Móvil o IP Webcam)

**Paso 1:** Instala una app en tu móvil (ej. "IP Webcam" en Android)

**Paso 2:** Conecta PC y móvil a la misma red Wi-Fi

**Paso 3:** Inicia el servidor en la app y copia la URL (ej. http://192.168.1.42:8080)

**Paso 4:** Ejecuta:
```powershell
python .\lector_qr.py --source "http://192.168.1.42:8080/video"
```

#### D. Escanear una Imagen
```powershell
python .\lector_qr.py --image .\ruta\a\imagen.png
```

#### E. Exportar Directamente a CSV
```powershell
python .\lector_qr.py --camera 0 --output mis_escaneos.csv
```

---

### Desde Navegador (Interfaz Web)

1. **Abre** `Pantalla_Inicial.html` en tu navegador
   - Doble clic en el archivo, o
   - Arrastra al navegador, o
   - Haz clic derecho → Abrir con → Navegador

2. **Haz clic** en "Abrir lector (script)" → Se abrirá `lector_qr.html`

3. **En `lector_qr.html`:**
   - Selecciona fuente (cámara local o remota)
   - Presiona "Iniciar lectura"
   - Muestra un código QR frente a la cámara
   - Los resultados aparecen en la tabla
   - Presiona "Descargar CSV" para guardar los datos

---

## 💻 Ejemplos Prácticos

### Ejemplo 1: Escanear inventario y guardar a CSV

```powershell
# Escanea durante 5 minutos y guarda resultados
python .\lector_qr.py --camera 0 --output "inventario_$(Get-Date -f 'yyyyMMdd_HHmmss').csv"
```

### Ejemplo 2: Usar cámara del móvil por 2 horas

```powershell
# En el móvil:
# 1. Abre IP Webcam
# 2. Presiona "Start Server"
# 3. Copia la URL (ej http://192.168.1.42:8080/video)

# En la PC:
python .\lector_qr.py --source "http://192.168.1.42:8080/video" --output "escaneos_mobile.csv"
```

### Ejemplo 3: Verificar un lote de imágenes

```powershell
# Crea una carpeta con QR's
# Luego escanea cada uno:
foreach ($img in Get-ChildItem *.png) {
    python .\lector_qr.py --image $img
}
```

---

## 📊 Salida CSV

El archivo CSV generado tiene este formato:

```csv
código,hora
978-3-16-148410-0,2025-11-12 14:23:45.123
978-0-13-468599-1,2025-11-12 14:23:47.456
```

---

## 🎨 Paleta de Colores Win Sports

- **Blanco:** #ffffff (fondo)
- **Negro:** #000000 (texto/header)
- **Naranja:** #f50 (acento primario)
- **Morado:** #d839ff (acento secundario)

---

## 🔧 Solución de Problemas

### "Cámara no se abre"
- ✅ Permite acceso a cámara en permisos del navegador
- ✅ Verifica que la cámara no esté en uso por otro programa
- ✅ Prueba `--camera 1` o `--camera 2` si tienes múltiples

### "Stream remoto no conecta"
- ✅ Verifica que móvil y PC están en la misma red
- ✅ Prueba la URL en el navegador: http://IP:PUERTO/shot.jpg
- ✅ Usa `/video` o `/mjpegfeed` si `/video` no funciona

### "pyzbar falla en Windows"
- ✅ Normal - el script usa OpenCV automáticamente
- ✅ La detección funciona igual de bien
- ✅ No necesitas instalar nada extra

### "No se detecta ningún QR"
- ✅ Asegúrate de que el código esté en el centro
- ✅ Intenta acercarte más o cambiar ángulo
- ✅ Prueba con una imagen de prueba primero

---

## 📁 Estructura de Archivos

```
Proyecto Inventario/
├── Pantalla_Inicial.html      # Interfaz principal
├── lector_qr.html             # Interfaz web del lector
├── lector_qr.py               # Lógica Python (CLI)
├── qr-scanner.js              # Lógica JavaScript (web)
├── styles.css                 # Estilos compartidos
├── base_de_datos.sql          # BD (opcional)
├── README.md                  # Este archivo
└── mi_inventario_env/         # Entorno virtual Python
```

---

## 🚀 Próximas Mejoras (Futuro)

- [ ] Conectar a base de datos en tiempo real
- [ ] Dashboard de estadísticas
- [ ] Reporte de escaneos por hora/día
- [ ] Multihilo para múltiples cámaras
- [ ] API REST para integración
- [ ] Aplicación de escritorio (PyQt/Tkinter)

---

## 📞 Soporte

Si tienes problemas:
1. Verifica que Python 3.8+ está instalado: `python --version`
2. Activar virtualenv: `. .\mi_inventario_env\Scripts\Activate.ps1`
3. Instalar dependencias: `pip install -r requirements.txt`
4. Ejecutar con verbose: `python lector_qr.py --help`

---

## ✅ Checklist de Configuración

- [ ] Python 3.8+ instalado
- [ ] Virtualenv activado
- [ ] OpenCV instalado (`pip install opencv-python`)
- [ ] `lector_qr.py` prueba correctamente (`python lector_qr.py --help`)
- [ ] `Pantalla_Inicial.html` se abre en navegador
- [ ] `lector_qr.html` carga correctamente
- [ ] Cámara funciona (presionar "Iniciar lectura")

---

**© Win Sports 2025** | Inventario - Sistema de Lectura QR
