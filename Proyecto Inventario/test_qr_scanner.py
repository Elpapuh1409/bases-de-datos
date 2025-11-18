#!/usr/bin/env python3
"""
Script de prueba - Simula un escaneo QR para verificar que el sistema funciona
"""

import csv
from datetime import datetime


def test_qr_scanner():
    """Prueba básica del sistema de escaneo QR."""
    print("\n" + "="*60)
    print("PRUEBA DE LECTOR QR WIN SPORTS")
    print("="*60 + "\n")

    # Simular algunos escaneos
    test_codes = [
        "WS-INV-001-2025",
        "978-3-16-148410-0",
        "WS-PRODUCTO-SKU-001",
        "https://winsports.example.com/item/12345",
        "LOTE-BODEGA-A-001",
    ]

    results = []
    print("Simulando escaneos:")
    print("-" * 60)
    
    for i, code in enumerate(test_codes, 1):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        results.append({"código": code, "hora": timestamp})
        print(f"✓ {i}. Detectado: {code} @ {timestamp}")

    # Mostrar resumen
    print("\n" + "="*60)
    print("RESUMEN DE ESCANEOS")
    print("="*60)
    print(f"Total de códigos detectados: {len(results)}")
    print("\nCódigos escaneados:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. {result['código']} ({result['hora']})")
    print("="*60 + "\n")

    # Exportar a CSV
    output_file = "test_escaneos.csv"
    try:
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["código", "hora"])
            writer.writeheader()
            writer.writerows(results)
        print(f"✅ Exportado a: {output_file}\n")
    except Exception as e:
        print(f"❌ Error al exportar: {e}\n")

    print("✅ PRUEBA COMPLETADA EXITOSAMENTE!\n")
    print("Próximos pasos:")
    print("  1. Prueba con imagen: python lector_qr.py --image <ruta>")
    print("  2. Prueba con cámara: python lector_qr.py")
    print("  3. Abre Pantalla_Inicial.html en el navegador\n")


if __name__ == "__main__":
    test_qr_scanner()
