import re
import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'es-ES,es;q=0.9',
}

LIDERPROP_ZONES = [
    {
        'name': 'Ramos Mejía',
        'url': 'https://www.liderprop.com/es-ar/propiedades/venta/ph/argentina--gba-zona-oeste--la-matanza--ramos-mejia/apto-credito--si/'
    },
    {
        'name': 'Haedo',
        'url': 'https://www.liderprop.com/es-ar/propiedades/venta/ph/argentina--gba-zona-oeste--moron--haedo/apto-credito--si/'
    },
    {
        'name': 'Villa Sarmiento',
        'url': 'https://www.liderprop.com/es-ar/propiedades/venta/ph/argentina--gba-zona-oeste--moron--villa-sarmiento/apto-credito--si/'
    }
]

BASE_URL = "https://www.liderprop.com"

def fetch_liderprop_properties():
    """
    Rastrea PHs apto crédito en Liderprop para Ramos Mejía, Haedo y Villa Sarmiento.
    """
    properties = []
    seen_ids = set()

    for zone in LIDERPROP_ZONES:
        zone_name = zone['name']
        url = zone['url']
        print(f"[*] Buscando en {zone_name} (Liderprop)...")

        try:
            resp = requests.get(url, headers=HEADERS, timeout=12)
            if resp.status_code != 200:
                continue

            soup = BeautifulSoup(resp.text, 'html.parser')
            # Las fichas suelen estar en contenedores panel-body
            panels = soup.find_all('div', class_=lambda c: c and 'panel-body' in c)

            for panel in panels:
                # Buscar enlace a la propiedad
                prop_link = panel.find('a', href=lambda h: h and '/propiedades/' in h and '/venta--' in h)
                if not prop_link:
                    continue

                href = prop_link['href']
                m_id = re.search(r'/propiedades/(\d+)/', href)
                prop_id = m_id.group(1) if m_id else href

                if prop_id in seen_ids:
                    continue
                seen_ids.add(prop_id)

                full_url = href if href.startswith('http') else BASE_URL + href

                # Precio
                price_div = panel.find('div', class_='price')
                raw_price = price_div.text.strip() if price_div else ''

                # Titulo y descripción
                full_text = panel.get_text(" ", strip=True)
                title = prop_link.text.strip() or f"PH en Venta en {zone_name}"

                # Imagen
                img = panel.find('img', src=lambda s: s and ('liderprop' in s or 'prop' in s or 'jpg' in s or 'png' in s))
                img_url = img['src'] if img else ''
                if img_url and not img_url.startswith('http'):
                    img_url = BASE_URL + img_url

                # Inmobiliaria
                inmo_elem = panel.find(class_=lambda c: c and 'inmobiliaria' in c.lower())
                inmobiliaria = inmo_elem.text.strip() if inmo_elem else 'Inmobiliaria Liderprop'

                properties.append({
                    'id': f"lp_{prop_id}",
                    'source': 'Liderprop',
                    'title': title,
                    'price_raw': raw_price,
                    'zone': zone_name,
                    'address': f"{zone_name}, GBA Oeste",
                    'features_text': "APTO CRÉDITO | " + full_text[:160],
                    'expensas': '',
                    'image_url': img_url,
                    'inmobiliaria': inmobiliaria,
                    'whatsapp': '',
                    'phone': '',
                    'url': full_url,
                })

        except Exception as e:
            print(f"[-] Error en Liderprop {zone_name}: {e}")

    print(f"[+] Total extraídas de Liderprop: {len(properties)}")
    return properties


if __name__ == '__main__':
    items = fetch_liderprop_properties()
    print(f"Ejemplo Liderprop ({len(items)} items):")
    if items:
        import pprint
        pprint.pprint(items[0])
