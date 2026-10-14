import os
import sys
import webbrowser
from datetime import datetime

from scraper_buscadorprop import fetch_buscadorprop_properties
from scraper_liderprop import fetch_liderprop_properties
from filter_engine import apply_filters
from report_generator import generate_report

# Asegurar codificación utf-8 en consola de Windows
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

def run_search(max_price=100000, open_browser=True):
    print("=" * 65)
    print("  BUSCADOR DE PHs - ZONA OESTE (APTO CRÉDITO)")
    print(f"  Ramos Mejía | Haedo | Villa Sarmiento | Máximo USD {max_price:,}".replace(',', '.'))
    print(f"  Fecha de ejecución: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 65)

    all_raw_properties = []

    # 1. Scraping BuscadorProp
    try:
        bp_props = fetch_buscadorprop_properties(max_pages_per_zone=4)
        all_raw_properties.extend(bp_props)
    except Exception as e:
        print(f"[!] Error al rastrear BuscadorProp: {e}")

    # 2. Scraping Liderprop
    try:
        lp_props = fetch_liderprop_properties()
        all_raw_properties.extend(lp_props)
    except Exception as e:
        print(f"[!] Error al rastrear Liderprop: {e}")

    print(f"\n[i] Total avisos brutos recolectados: {len(all_raw_properties)}")

    # 3. Aplicar Filtros (Apto Crédito, 3+ amb, <= 100k USD)
    print("[*] Aplicando filtros estrictos de Apto Crédito, 3+ Ambientes y Precio...")
    filtered = apply_filters(all_raw_properties, max_price=max_price)
    print(f"[+] Propiedades finales que cumplen TODOS los requisitos: {len(filtered)}")

    if not filtered:
        print("\n[!] No se encontraron propiedades que cumplan con todos los filtros exactos hoy.")
        print("    Probá correrlo nuevamente más tarde para detectar nuevos avisos.")
        return

    # 4. Generar Reporte HTML interactivo
    report_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reporte_propiedades.html")
    full_path = generate_report(filtered, output_path=report_file)

    print("\n" + "=" * 65)
    print("  RESUMEN DE OPORTUNIDADES ENCONTRADAS:")
    print("=" * 65)
    for idx, p in enumerate(filtered[:5], 1):
        price_fmt = f"USD {p['price_usd']:,}".replace(',', '.')
        print(f"  {idx}. [{p['zone']}] {price_fmt} - {p['title']}")
        print(f"     Dirección: {p['address']}")
        print(f"     Inmobiliaria: {p['inmobiliaria']}")
        if p.get('whatsapp'):
            print(f"     WhatsApp: +{p['whatsapp']}")
        print(f"     Ficha: {p['url']}")
        print("-" * 65)

    print(f"\n[OK] Reporte completo generado en: {full_path}")

    # 5. Abrir automáticamente en el navegador
    if open_browser:
        print("[*] Abriendo reporte en tu navegador...")
        webbrowser.open(f"file:///{full_path}")


if __name__ == '__main__':
    max_usd = 100000
    if len(sys.argv) > 1:
        try:
            max_usd = int(sys.argv[1])
        except ValueError:
            pass

    run_search(max_price=max_usd)
