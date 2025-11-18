#!/usr/bin/env python3
"""
Lector QR Avanzado para Win Sports
Detecta y decodifica códigos QR desde:
- Cámara local
- Stream remoto (URL HTTP/RTSP)
- Archivo de imagen

Características:
- Decodificación con pyzbar (recomendado) o OpenCV fallback
- Exportación a CSV
- Validación de datos
- Interfaz CLI completa
"""

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Tuple
import threading
import queue
import time

import cv2
import numpy as np

# Intentar importar pyzbar
try:
    from pyzbar import pyzbar
    PYZBAR_AVAILABLE = True
    print("[INFO] pyzbar disponible - usando para decodificación.")
except ImportError:
    PYZBAR_AVAILABLE = False
    print("[INFO] pyzbar no disponible - usando OpenCV QRCodeDetector (fallback).")
except Exception as e:
    PYZBAR_AVAILABLE = False
    print(f"[WARN] Error cargando pyzbar: {e} - Usando OpenCV como alternativa.")


class QRScanner:
    """Escáner de códigos QR con soporte local y remoto."""

    def __init__(self, output_csv: Optional[str] = None):
        self.output_csv = output_csv
        self.results: List[Dict[str, str]] = []
        self.detector = cv2.QRCodeDetector()
        self.running = False
        self.results_lock = threading.Lock()

    def decode_with_pyzbar(self, frame: np.ndarray) -> List[str]:
        """Decodifica QR usando pyzbar."""
        try:
            barcodes = pyzbar.decode(frame)
            return [b.data.decode("utf-8") for b in barcodes if b and b.data]
        except Exception as e:
            print(f"[ERROR] pyzbar: {e}")
            return []

    def decode_with_cv(self, frame: np.ndarray) -> List[str]:
        """Decodifica QR usando OpenCV."""
        try:
            # Intentar detectAndDecodeMulti (disponible en OpenCV 4.0+)
            try:
                ok, decoded_infos, points, straight_qr = self.detector.detectAndDecodeMulti(frame)
                if ok and decoded_infos:
                    return [s for s in decoded_infos if s]
            except AttributeError:
                # Fallback a detectAndDecode (compatible con versiones antiguas)
                pass

            # Single decode
            data, points, straight_qr = self.detector.detectAndDecode(frame)
            return [data] if data else []
        except Exception as e:
            print(f"[ERROR] OpenCV: {e}")
            return []

    def decode_frame(self, frame: np.ndarray) -> List[str]:
        """Decodifica frame usando pyzbar o OpenCV."""
        if PYZBAR_AVAILABLE:
            return self.decode_with_pyzbar(frame)
        else:
            return self.decode_with_cv(frame)

    def add_result(self, code: str) -> None:
        """Agrega un resultado de escaneo."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        with self.results_lock:
            self.results.append({"código": code, "hora": timestamp})
            print(f"✓ Detectado: {code} @ {timestamp}")

    def scan_video(self, source: int | str, max_frames: Optional[int] = None) -> None:
        """Escanea video desde cámara o URL."""
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            print(f"[ERROR] No se pudo abrir la fuente: {source}")
            return

        print(f"[INFO] Capturando desde: {source}")
        print("[CONTROLES] Presiona 'q' para salir, 's' para guardar captura")

        frame_count = 0
        deduplication_cache: Dict[str, float] = {}
        last_seen: Dict[str, float] = {}

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("[WARN] No se pudo leer frame. Reintentando...")
                    time.sleep(0.5)
                    continue

                frame_count += 1
                if max_frames and frame_count > max_frames:
                    print(f"[INFO] Alcanzado límite de {max_frames} frames.")
                    break

                # Decodificar
                codes = self.decode_frame(frame)
                current_time = time.time()

                for code in codes:
                    # Deduplicación (2 segundos)
                    if code in last_seen:
                        if current_time - last_seen[code] < 2.0:
                            continue
                    
                    last_seen[code] = current_time
                    self.add_result(code)

                # Mostrar frame
                cv2.imshow("Lector QR Win Sports", frame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break
                elif key == ord("s"):
                    filename = f"captura_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    cv2.imwrite(filename, frame)
                    print(f"[OK] Captura guardada: {filename}")

        except KeyboardInterrupt:
            print("\n[INFO] Escaneo interrumpido por usuario.")
        finally:
            cap.release()
            cv2.destroyAllWindows()

    def scan_image(self, image_path: str) -> None:
        """Escanea una imagen."""
        if not Path(image_path).exists():
            print(f"[ERROR] Archivo no encontrado: {image_path}")
            return

        img = cv2.imread(image_path)
        if img is None:
            print(f"[ERROR] No se pudo abrir: {image_path}")
            return

        print(f"[INFO] Escaneando imagen: {image_path}")
        codes = self.decode_frame(img)

        if codes:
            print(f"\n[RESULTADOS] Se encontraron {len(codes)} código(s):")
            for code in codes:
                self.add_result(code)
        else:
            print("[WARN] No se detectaron códigos QR.")

    def export_csv(self, filename: Optional[str] = None) -> None:
        """Exporta resultados a CSV."""
        if not self.results:
            print("[WARN] No hay resultados para exportar.")
            return

        output_file = filename or self.output_csv or f"escaneos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        try:
            with open(output_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["código", "hora"])
                writer.writeheader()
                writer.writerows(self.results)
            print(f"[OK] Exportado a: {output_file}")
        except Exception as e:
            print(f"[ERROR] No se pudo exportar: {e}")

    def print_summary(self) -> None:
        """Imprime resumen de resultados."""
        print("\n" + "="*60)
        print("RESUMEN DE ESCANEOS")
        print("="*60)
        print(f"Total de códigos detectados: {len(self.results)}")
        if self.results:
            print("\nÚltimos 10 escaneos:")
            for i, result in enumerate(self.results[-10:], 1):
                print(f"  {i}. {result['código']} ({result['hora']})")
        print("="*60 + "\n")


def build_parser() -> argparse.ArgumentParser:
    """Construye el parser de argumentos."""
    parser = argparse.ArgumentParser(
        description="Lector QR para Win Sports - Detecta códigos QR desde cámara, URL o imagen",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  # Cámara local (por defecto)
  %(prog)s

  # Otra cámara
  %(prog)s --camera 1

  # Stream remoto (IP Webcam)
  %(prog)s --source "http://192.168.1.42:8080/video"

  # Imagen
  %(prog)s --image ./qr.png

  # Exportar a CSV específico
  %(prog)s --camera 0 --output resultados.csv
        """
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--image", "-i",
        help="Ruta a una imagen para decodificar"
    )
    group.add_argument(
        "--camera", "-c",
        type=int,
        default=0,
        help="Índice de la cámara (default: 0)"
    )
    group.add_argument(
        "--source", "-s",
        type=str,
        help="Fuente de video remota (URL HTTP/RTSP)"
    )

    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Archivo CSV para exportar resultados"
    )

    parser.add_argument(
        "--max-frames",
        type=int,
        help="Máximo número de frames a procesar (para testing)"
    )

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Función principal."""
    parser = build_parser()
    args = parser.parse_args(argv)

    print("\n" + "="*60)
    print("WIN SPORTS - LECTOR QR AVANZADO")
    print("="*60)
    print(f"Librería: {'pyzbar' if PYZBAR_AVAILABLE else 'OpenCV QRCodeDetector'}")
    print(f"OpenCV versión: {cv2.__version__}")
    print("="*60 + "\n")

    scanner = QRScanner(output_csv=args.output)

    # Determinar fuente
    if args.image:
        scanner.scan_image(args.image)
    else:
        # Usar --source si se proporciona, sino usar --camera
        source = args.source if args.source else args.camera
        
        # Si source es string y es un número, convertir a int
        if isinstance(source, str) and source.isdigit():
            source = int(source)
        
        scanner.scan_video(source, max_frames=args.max_frames)

    # Mostrar resumen y exportar
    scanner.print_summary()

    if scanner.results:
        if args.output:
            scanner.export_csv(args.output)
        else:
            should_export = input("¿Deseas exportar los resultados a CSV? (s/n): ").lower()
            if should_export == "s":
                scanner.export_csv()

    return 0


if __name__ == "__main__":
    sys.exit(main())
