import re

def parse_price(price_raw):
    """
    Parsea una cadena como 'USD 65.900' o 'U$S 88.000' a un entero (65900).
    Retorna None si no es un precio válido en dólares.
    """
    if not price_raw:
        return None
    
    raw = price_raw.strip().upper()
    if 'CONSULTAR' in raw or 'RESERVADO' in raw:
        return None
    
    # Extraer dígitos
    clean = re.sub(r'[^\d]', '', raw)
    if not clean:
        return None
    
    try:
        val = int(clean)
        # En Argentina a veces ponen 6590000 si hay decimales o pesos, pero USD suele ser entre 15.000 y 500.000
        if 15000 <= val <= 1000000:
            return val
        return None
    except ValueError:
        return None


def is_apto_credito(text, source=''):
    """
    Verifica que la propiedad sea apta para crédito hipotecario,
    descartando falsos positivos que digan 'NO apto crédito'.
    """
    if not text:
        return False
    
    t = text.lower()
    
    # Si explícitamente dice 'no apto' o 'no es apto', descartar
    if re.search(r'\bno\s+(es\s+)?apto\s+cr[eé]dito\b', t) or 'sin credito' in t or 'no credito' in t:
        return False
    
    # Si la fuente ya venía pre-filtrada por apto-crédito
    if 'apto-credito--si' in t or 'apto crédito' in t or 'apto credito' in t:
        return True
    
    if re.search(r'\bapto\s+cr[eé]dito\b', t):
        return True
        
    return False


def has_3_or_more_rooms(text):
    """
    Verifica que tenga 3 o más ambientes, o 2 o más dormitorios.
    """
    if not text:
        return False
    
    t = text.lower()
    
    # Chequeo de dormitorios (>= 2 dormitorios equivale a 3 o más ambientes)
    dorm_match = re.search(r'(\d+)\s*(?:dormitorio|dorm)\b', t)
    if dorm_match:
        try:
            dorms = int(dorm_match.group(1))
            if dorms >= 2:
                return True
        except ValueError:
            pass
            
    if any(k in t for k in ['2 dormitorios', '3 dormitorios', '4 dormitorios', 'dos dormitorios', 'tres dormitorios']):
        return True

    # Chequeo de ambientes (>= 3 ambientes)
    amb_match = re.search(r'(\d+)\s*(?:ambiente|amb)\b', t)
    if amb_match:
        try:
            ambs = int(amb_match.group(1))
            if ambs >= 3:
                return True
            elif ambs < 3 and not dorm_match:
                # Si explícitamente dice 1 o 2 ambientes y no especifica dormitorios >= 2, descartar
                return False
        except ValueError:
            pass

    if any(k in t for k in ['3 ambientes', '4 ambientes', '5 ambientes', '3 amb', '4 amb', 'tres ambientes', 'cuatro ambientes']):
        return True

    return False


def apply_filters(properties, max_price=100000):
    """
    Aplica todos los filtros requeridos por el usuario:
    - Precio <= max_price USD
    - Apto crédito == True (sin negaciones)
    - Ambientes >= 3 o dormitorios >= 2
    - Desduplica avisos
    """
    filtered = []
    seen_keys = set()

    for p in properties:
        full_text = f"{p.get('title', '')} {p.get('features_text', '')} {p.get('address', '')}"
        
        # 1. Parsear precio
        price_val = parse_price(p.get('price_raw', ''))
        if price_val is None or price_val > max_price:
            continue
        p['price_usd'] = price_val

        # 2. Apto crédito
        if not is_apto_credito(full_text):
            continue

        # 3. Ambientes (3+ ambientes o 2+ dormitorios)
        if not has_3_or_more_rooms(full_text):
            continue

        # 4. Desduplicación por link o dirección
        dedup_key = p.get('url') or p.get('id')
        if dedup_key in seen_keys:
            continue
        seen_keys.add(dedup_key)

        filtered.append(p)

    # Ordenar por precio ascendente (las mejores oportunidades primero)
    filtered.sort(key=lambda x: x['price_usd'])
    return filtered


if __name__ == '__main__':
    sample = [
        {
            'title': 'PH 3 ambientes',
            'features_text': 'APTO CRÉDITO | 3 ambientes | 2 dormitorios',
            'price_raw': 'USD 65.900',
            'url': 'http://test1'
        },
        {
            'title': 'PH 2 ambientes',
            'features_text': 'APTO CRÉDITO | 2 ambientes | 1 dormitorio',
            'price_raw': 'USD 38.000',
            'url': 'http://test2'
        },
        {
            'title': 'PH 3 ambientes',
            'features_text': 'NO APTO CRÉDITO | 3 ambientes',
            'price_raw': 'USD 50.000',
            'url': 'http://test3'
        },
        {
            'title': 'PH 4 ambientes',
            'features_text': 'APTO CRÉDITO | 4 ambientes',
            'price_raw': 'USD 120.000',
            'url': 'http://test4'
        }
    ]
    res = apply_filters(sample)
    print(f"Filtrados: {len(res)} (esperado: 1)")
    assert len(res) == 1
    assert res[0]['price_usd'] == 65900
    print("[+] Test de filtros exitoso!")
