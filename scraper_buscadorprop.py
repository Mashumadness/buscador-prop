import re
import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'es-ES,es;q=0.9',
}

ZONES = [
    {
        'name': 'Ramos Mejía',
        'slug': 'dptos-tipo-casa-ph-venta-ramos-mejia'
    },
    {
        'name': 'Haedo',
        'slug': 'dptos-tipo-casa-ph-venta-haedo'
    },
    {
        'name': 'Villa Sarmiento',
        'slug': 'dptos-tipo-casa-ph-venta-villa-sarmiento-moron'
    }
]

BASE_URL = "https://www.buscadorprop.com.ar"

def fetch_buscadorprop_properties(max_pages_per_zone=4):
    """
    Rastrea las propiedades tipo PH en BuscadorProp para las zonas indicadas.
    Retorna una lista de diccionarios normalizados.
    """
    properties = []
    seen_ids = set()

    for zone_info in ZONES:
        zone_name = zone_info['name']
        slug = zone_info['slug']
        print(f"[*] Buscando en {zone_name} (BuscadorProp)...")

        for page in range(1, max_pages_per_zone + 1):
            if page == 1:
                url = f"{BASE_URL}/{slug}"
            else:
                url = f"{BASE_URL}/{slug}?pagina={page}"

            try:
                resp = requests.get(url, headers=HEADERS, timeout=12)
                if resp.status_code != 200:
                    break

                soup = BeautifulSoup(resp.text, 'html.parser')
                cards = soup.find_all('div', class_='card-prop')
                if not cards:
                    break

                new_on_page = 0
                for card in cards:
                    link_elem = card.find('a', href=lambda h: h and '/propiedad/' in h)
                    if not link_elem:
                        continue

                    href = link_elem.get('href', '').strip()
                    if not href.startswith('http'):
                        full_link = BASE_URL + href
                    else:
                        full_link = href

                    prop_id = card.get('data-id') or re.search(r'/propiedad/(\d+)', href)
                    prop_id = prop_id.group(1) if hasattr(prop_id, 'group') else str(prop_id or href)

                    if prop_id in seen_ids:
                        continue
                    seen_ids.add(prop_id)
                    new_on_page += 1

                    # Titulo
                    title_elem = card.find('h2') or card.find('h3') or link_elem
                    title = title_elem.text.strip() if title_elem else 'PH en Venta'

                    # Precio
                    price_elem = card.find('div', class_='card-prop__precio__precios__actual')
                    raw_price = price_elem.text.strip() if price_elem else ''

                    # Direccion
                    dir_elem = card.find('div', class_='card-prop__direccion')
                    address = dir_elem.find('span').text.strip() if (dir_elem and dir_elem.find('span')) else (dir_elem.text.strip() if dir_elem else zone_name)

                    # Highlights (Apto crédito, ambientes, dormitorios)
                    high_elem = card.find('div', class_='card-prop__body__arriba__high')
                    high_text = high_elem.text.strip() if high_elem else ''

                    # Expensas
                    exp_elem = card.find('span', class_='card-prop__sin-expensas')
                    expensas = exp_elem.text.strip() if exp_elem else ''

                    # Imagen
                    img_elem = card.find('div', class_='card-prop__image__element')
                    img_url = ''
                    if img_elem and '--background' in img_elem.get('style', ''):
                        bg_style = img_elem.get('style', '')
                        m_img = re.search(r'url\((.*?)\)', bg_style)
                        if m_img:
                            img_url = m_img.group(1).strip('\'"')
                    if not img_url:
                        first_img = card.find('img', src=lambda s: s and 'prop_new' in s)
                        if first_img:
                            img_url = first_img.get('src')

                    # Inmobiliaria
                    inmo_logo = card.find('img', class_='card-prop__logo')
                    inmo_name = inmo_logo.get('alt', '').strip() if inmo_logo else ''
                    if not inmo_name:
                        inmo_btn = card.find('button', attrs={'data-inmobiliaria': True})
                        inmo_name = f"Inmobiliaria #{inmo_btn.get('data-inmobiliaria')}" if inmo_btn else "Inmobiliaria Local"

                    # WhatsApp / Telefono
                    wts_btn = card.find('button', attrs={'data-whatsapp': True})
                    whatsapp_number = wts_btn.get('data-whatsapp', '').strip() if wts_btn else ''
                    tel_btn = card.find('button', attrs={'data-telefono': True})
                    phone_number = tel_btn.get('data-telefono', '').strip() if tel_btn else ''

                    properties.append({
                        'id': f"bp_{prop_id}",
                        'source': 'BuscadorProp',
                        'title': title,
                        'price_raw': raw_price,
                        'zone': zone_name,
                        'address': address,
                        'features_text': high_text,
                        'expensas': expensas,
                        'image_url': img_url,
                        'inmobiliaria': inmo_name,
                        'whatsapp': whatsapp_number,
                        'phone': phone_number,
                        'url': full_link,
                    })

                if new_on_page == 0:
                    break

            except Exception as e:
                print(f"[-] Error en {zone_name} página {page}: {e}")
                break

    print(f"[+] Total extraídas de BuscadorProp: {len(properties)}")
    return properties


if __name__ == '__main__':
    items = fetch_buscadorprop_properties(max_pages_per_zone=2)
    print(f"Ejemplo extraído ({len(items)} items):")
    if items:
        import pprint
        pprint.pprint(items[0])
