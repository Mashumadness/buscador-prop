import os
import json
import urllib.parse
from datetime import datetime

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Buscador de PHs - Zona Oeste (Apto Crédito)</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #0f172a;
            --primary-light: #1e293b;
            --accent: #2563eb;
            --accent-hover: #1d4ed8;
            --success: #10b981;
            --success-bg: #ecfdf5;
            --wa-green: #25d366;
            --wa-hover: #20ba5a;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --border: #e2e8f0;
            --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
            --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
            --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        body {
            background-color: var(--bg);
            color: var(--text-main);
            line-height: 1.5;
            padding-bottom: 60px;
        }

        header {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
            color: white;
            padding: 40px 24px 32px;
            box-shadow: var(--shadow-md);
        }

        .header-container {
            max-width: 1200px;
            margin: 0 auto;
        }

        .header-title-row {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            flex-wrap: wrap;
            gap: 16px;
            margin-bottom: 24px;
        }

        h1 {
            font-size: 1.85rem;
            font-weight: 800;
            letter-spacing: -0.025em;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .header-subtitle {
            color: #94a3b8;
            font-size: 0.95rem;
            margin-top: 6px;
        }

        .badge-verified {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(16, 185, 129, 0.2);
            color: #34d399;
            border: 1px solid rgba(52, 211, 153, 0.3);
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        /* Stats Row */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
        }

        .stat-card {
            background: rgba(255, 255, 255, 0.07);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            padding: 16px;
            border-radius: 12px;
        }

        .stat-label {
            font-size: 0.8rem;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 600;
        }

        .stat-value {
            font-size: 1.5rem;
            font-weight: 800;
            color: #ffffff;
            margin-top: 4px;
        }

        /* Main Container */
        .main-container {
            max-width: 1200px;
            margin: -20px auto 0;
            padding: 0 24px;
        }

        /* Filter Controls */
        .filter-panel {
            background: white;
            border-radius: 16px;
            padding: 20px 24px;
            box-shadow: var(--shadow-md);
            border: 1px solid var(--border);
            display: flex;
            flex-wrap: wrap;
            gap: 16px;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 32px;
        }

        .zone-buttons {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }

        .zone-btn {
            background: #f1f5f9;
            color: var(--text-muted);
            border: 1px solid transparent;
            padding: 8px 16px;
            border-radius: 9999px;
            font-size: 0.875rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .zone-btn:hover {
            background: #e2e8f0;
            color: var(--text-main);
        }

        .zone-btn.active {
            background: var(--accent);
            color: white;
            box-shadow: 0 2px 4px rgba(37, 99, 235, 0.3);
        }

        .search-inputs {
            display: flex;
            gap: 12px;
            flex-grow: 1;
            max-width: 480px;
        }

        .search-box {
            position: relative;
            flex-grow: 1;
        }

        .search-box input {
            width: 100%;
            padding: 10px 16px 10px 38px;
            border-radius: 10px;
            border: 1px solid var(--border);
            font-size: 0.9rem;
            outline: none;
            transition: border 0.2s;
        }

        .search-box input:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
        }

        .search-box svg {
            position: absolute;
            left: 12px;
            top: 50%;
            transform: translateY(-50%);
            width: 18px;
            height: 18px;
            fill: var(--text-muted);
        }

        .sort-select {
            padding: 10px 14px;
            border-radius: 10px;
            border: 1px solid var(--border);
            background: white;
            font-size: 0.9rem;
            color: var(--text-main);
            cursor: pointer;
            outline: none;
        }

        /* Property Cards Grid */
        .cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
            gap: 24px;
        }

        .property-card {
            background: var(--card-bg);
            border-radius: 16px;
            overflow: hidden;
            box-shadow: var(--shadow-sm);
            border: 1px solid var(--border);
            display: flex;
            flex-direction: column;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .property-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-lg);
        }

        .card-image-wrap {
            position: relative;
            width: 100%;
            height: 220px;
            background: #e2e8f0;
            overflow: hidden;
        }

        .card-image {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s ease;
        }

        .property-card:hover .card-image {
            transform: scale(1.03);
        }

        .card-badges {
            position: absolute;
            top: 12px;
            left: 12px;
            right: 12px;
            display: flex;
            justify-content: space-between;
            pointer-events: none;
        }

        .badge-credito {
            background: var(--success);
            color: white;
            font-size: 0.75rem;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 6px;
            letter-spacing: 0.04em;
            box-shadow: var(--shadow-sm);
        }

        .badge-zone {
            background: rgba(15, 23, 42, 0.85);
            backdrop-filter: blur(4px);
            color: white;
            font-size: 0.75rem;
            font-weight: 600;
            padding: 4px 10px;
            border-radius: 6px;
        }

        .card-content {
            padding: 20px;
            display: flex;
            flex-direction: column;
            flex-grow: 1;
        }

        .price-row {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 8px;
        }

        .price-val {
            font-size: 1.65rem;
            font-weight: 800;
            color: var(--primary);
            letter-spacing: -0.02em;
        }

        .expensas-tag {
            font-size: 0.75rem;
            color: #059669;
            background: #d1fae5;
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: 600;
        }

        .property-title {
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--text-main);
            margin-bottom: 8px;
            line-height: 1.35;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            min-height: 2.7em;
        }

        .property-address {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-bottom: 14px;
        }

        .property-address svg {
            width: 15px;
            height: 15px;
            flex-shrink: 0;
            fill: var(--text-muted);
        }

        .features-pill-row {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-bottom: 16px;
        }

        .feature-pill {
            background: #f1f5f9;
            color: #475569;
            font-size: 0.75rem;
            font-weight: 600;
            padding: 4px 10px;
            border-radius: 6px;
        }

        .inmobiliaria-row {
            margin-top: auto;
            padding-top: 14px;
            border-top: 1px solid var(--border);
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-bottom: 16px;
        }

        .inmobiliaria-name {
            font-weight: 600;
            color: var(--text-main);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        /* Card Actions */
        .card-actions {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }

        .btn-wa {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            background: var(--wa-green);
            color: white;
            padding: 10px 14px;
            border-radius: 10px;
            font-size: 0.85rem;
            font-weight: 700;
            text-decoration: none;
            transition: background 0.2s ease;
        }

        .btn-wa:hover {
            background: var(--wa-hover);
        }

        .btn-wa svg {
            width: 18px;
            height: 18px;
            fill: currentColor;
        }

        .btn-view {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            background: #f8fafc;
            color: var(--primary);
            border: 1px solid var(--border);
            padding: 10px 14px;
            border-radius: 10px;
            font-size: 0.85rem;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.2s ease;
        }

        .btn-view:hover {
            background: #f1f5f9;
            border-color: #cbd5e1;
        }

        .no-results {
            grid-column: 1 / -1;
            text-align: center;
            padding: 60px 20px;
            background: white;
            border-radius: 16px;
            border: 1px solid var(--border);
        }

        .no-results h3 {
            font-size: 1.25rem;
            color: var(--text-main);
            margin-bottom: 8px;
        }

        .no-results p {
            color: var(--text-muted);
            font-size: 0.95rem;
        }

        @media (max-width: 768px) {
            .cards-grid {
                grid-template-columns: 1fr;
            }
            .header-title-row {
                flex-direction: column;
            }
            .search-inputs {
                max-width: 100%;
            }
        }
    </style>
</head>
<body>

    <header>
        <div class="header-container">
            <div class="header-title-row">
                <div>
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
                        <span class="badge-verified">✓ Exclusivo Apto Crédito</span>
                        <span style="color: #94a3b8; font-size: 0.8rem;">Actualizado: {FECHA_ACTUALIZACION}</span>
                    </div>
                    <h1>🏠 Buscador de PHs en Zona Oeste</h1>
                    <p class="header-subtitle">Rastreo automático en inmobiliarias independientes de Ramos Mejía, Haedo y Villa Sarmiento (hasta USD 100.000)</p>
                </div>
            </div>

            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-label">Propiedades Encontradas</div>
                    <div class="stat-value">{TOTAL_PROPIEDADES}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Oportunidad Menor Precio</div>
                    <div class="stat-value">{MIN_PRECIO}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Precio Promedio</div>
                    <div class="stat-value">{AVG_PRECIO}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Zonas Rastreadas</div>
                    <div class="stat-value">3 Zonas</div>
                </div>
            </div>
        </div>
    </header>

    <main class="main-container">
        <!-- Filter Panel -->
        <div class="filter-panel">
            <div class="zone-buttons">
                <button class="zone-btn active" onclick="filterByZone('all')">Todas ({TOTAL_PROPIEDADES})</button>
                <button class="zone-btn" onclick="filterByZone('Ramos Mejía')">Ramos Mejía ({COUNT_RAMOS})</button>
                <button class="zone-btn" onclick="filterByZone('Haedo')">Haedo ({COUNT_HAEDO})</button>
                <button class="zone-btn" onclick="filterByZone('Villa Sarmiento')">Villa Sarmiento ({COUNT_SARMIENTO})</button>
            </div>

            <div class="search-inputs">
                <div class="search-box">
                    <svg viewBox="0 0 24 24"><path d="M10 18a7.952 7.952 0 0 0 4.897-1.688l4.396 4.396 1.414-1.414-4.396-4.396A7.952 7.952 0 0 0 18 10c0-4.411-3.589-8-8-8s-8 3.589-8 8 3.589 8 8 8zm0-14c3.309 0 6 2.691 6 6s-2.691 6-6 6-6-2.691-6-6 2.691-6 6-6z"/></svg>
                    <input type="text" id="searchInput" placeholder="Buscar por calle, ambientes..." oninput="handleSearch()">
                </div>
                <select class="sort-select" id="sortSelect" onchange="handleSort()">
                    <option value="price-asc">Menor precio</option>
                    <option value="price-desc">Mayor precio</option>
                </select>
            </div>
        </div>

        <!-- Cards Container -->
        <div class="cards-grid" id="cardsContainer">
            {CARDS_HTML}
        </div>
    </main>

    <script>
        let currentZone = 'all';
        let currentQuery = '';

        function filterByZone(zone) {
            currentZone = zone;
            document.querySelectorAll('.zone-btn').forEach(btn => {
                if (btn.innerText.includes(zone) || (zone === 'all' && btn.innerText.includes('Todas'))) {
                    btn.classList.add('active');
                } else {
                    btn.classList.remove('active');
                }
            });
            applyFilters();
        }

        function handleSearch() {
            currentQuery = document.getElementById('searchInput').value.toLowerCase().trim();
            applyFilters();
        }

        function handleSort() {
            const sortBy = document.getElementById('sortSelect').value;
            const container = document.getElementById('cardsContainer');
            const cards = Array.from(container.getElementsByClassName('property-card'));

            cards.sort((a, b) => {
                const priceA = parseInt(a.getAttribute('data-price')) || 0;
                const priceB = parseInt(b.getAttribute('data-price')) || 0;
                return sortBy === 'price-asc' ? priceA - priceB : priceB - priceA;
            });

            cards.forEach(card => container.appendChild(card));
        }

        function applyFilters() {
            const cards = document.querySelectorAll('.property-card');
            let visibleCount = 0;

            cards.forEach(card => {
                const cardZone = card.getAttribute('data-zone');
                const cardText = card.getAttribute('data-search');

                const matchesZone = (currentZone === 'all' || cardZone === currentZone);
                const matchesSearch = (!currentQuery || cardText.includes(currentQuery));

                if (matchesZone && matchesSearch) {
                    card.style.display = 'flex';
                    visibleCount++;
                } else {
                    card.style.display = 'none';
                }
            });

            let noRes = document.getElementById('noResultsMsg');
            if (visibleCount === 0) {
                if (!noRes) {
                    noRes = document.createElement('div');
                    noRes.id = 'noResultsMsg';
                    noRes.className = 'no-results';
                    noRes.innerHTML = '<h3>No se encontraron propiedades</h3><p>Probá cambiando los filtros o la búsqueda.</p>';
                    document.getElementById('cardsContainer').appendChild(noRes);
                }
                noRes.style.display = 'block';
            } else if (noRes) {
                noRes.style.display = 'none';
            }
        }
    </script>
</body>
</html>
"""

def generate_property_card_html(p):
    """
    Construye el HTML individual para una tarjeta de propiedad.
    """
    price_val = p.get('price_usd', 0)
    price_formatted = f"USD {price_val:,}".replace(',', '.')
    zone = p.get('zone', 'Zona Oeste')
    title = p.get('title', 'PH en Venta')
    address = p.get('address', zone)
    expensas = p.get('expensas', '')
    inmobiliaria = p.get('inmobiliaria', 'Inmobiliaria Local')
    img_url = p.get('image_url') or 'https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?auto=format&fit=crop&w=600&q=80'
    url = p.get('url', '#')
    whatsapp = p.get('whatsapp', '')
    phone = p.get('phone', '')
    features_text = p.get('features_text', '')

    # Extraer tags para píldoras
    pills = []
    if '3 ambiente' in features_text.lower() or '3 amb' in features_text.lower():
        pills.append('3 Ambientes')
    elif '4 ambiente' in features_text.lower() or '4 amb' in features_text.lower():
        pills.append('4 Ambientes')
    elif '5 ambiente' in features_text.lower():
        pills.append('5+ Ambientes')

    if '2 dormitorio' in features_text.lower() or '2 dorm' in features_text.lower():
        pills.append('2 Dormitorios')
    elif '3 dormitorio' in features_text.lower() or '3 dorm' in features_text.lower():
        pills.append('3 Dormitorios')

    if 'cochera' in features_text.lower() or 'auto' in features_text.lower():
        pills.append('Cochera')
    if 'patio' in features_text.lower():
        pills.append('Patio')
    if 'terraza' in features_text.lower():
        pills.append('Terraza')

    if not pills:
        pills.append('3+ Ambientes')

    pills_html = "".join([f'<span class="feature-pill">{pill}</span>' for pill in pills])

    # Enlace WhatsApp
    msg = f"Hola! Te contacto por la propiedad que vi publicada: {title} en {address}. Quería consultar si sigue disponible para visitar."
    msg_encoded = urllib.parse.quote(msg)

    if whatsapp:
        clean_wa = "".join([c for c in whatsapp if c.isdigit()])
        wa_link = f"https://wa.me/{clean_wa}?text={msg_encoded}"
        btn_contact = f'<a href="{wa_link}" target="_blank" class="btn-wa"><svg viewBox="0 0 24 24"><path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.149.929 3.182 0 5.767-2.587 5.768-5.766.001-3.187-2.575-5.771-5.768-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.299.045-.677.063-1.092-.069-.252-.08-.575-.187-.988-.365-1.739-.751-2.874-2.502-2.961-2.617-.087-.116-.708-.94-.708-1.793s.448-1.273.607-1.446c.159-.173.346-.217.462-.217l.332.007c.101.005.241-.038.375.285.144.346.491 1.2.534 1.287s.072.188.014.303c-.058.116-.087.188-.173.289l-.26.302c-.087.087-.179.181-.077.355.101.173.451.745.968 1.206.666.593 1.228.777 1.401.864.173.087.275.072.376-.044.101-.116.433-.506.549-.68.116-.173.231-.145.39-.087s1.011.477 1.184.564.289.13.332.202c.044.073.044.419-.1.824z"/></svg> WhatsApp</a>'
    elif phone:
        clean_phone = "".join([c for c in phone if c.isdigit()])
        btn_contact = f'<a href="tel:{clean_phone}" class="btn-wa" style="background:#0284c7;">📞 Llamar ({phone})</a>'
    else:
        btn_contact = f'<a href="{url}" target="_blank" class="btn-wa" style="background:#475569;">✉️ Contactar</a>'

    exp_badge = f'<span class="expensas-tag">{expensas}</span>' if expensas else ''
    search_blob = f"{title} {address} {zone} {features_text} {inmobiliaria}".lower()

    return f"""
    <div class="property-card" data-zone="{zone}" data-price="{price_val}" data-search="{search_blob}">
        <div class="card-image-wrap">
            <img src="{img_url}" class="card-image" alt="{title}" loading="lazy" onerror="this.src='https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?auto=format&fit=crop&w=600&q=80'">
            <div class="card-badges">
                <span class="badge-credito">APTO CRÉDITO</span>
                <span class="badge-zone">{zone}</span>
            </div>
        </div>
        <div class="card-content">
            <div class="price-row">
                <div class="price-val">{price_formatted}</div>
                {exp_badge}
            </div>
            <h2 class="property-title" title="{title}">{title}</h2>
            <div class="property-address">
                <svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
                <span>{address}</span>
            </div>
            <div class="features-pill-row">
                {pills_html}
            </div>
            <div class="inmobiliaria-row">
                <span>🏢 Inmobiliaria:</span>
                <span class="inmobiliaria-name">{inmobiliaria}</span>
            </div>
            <div class="card-actions">
                {btn_contact}
                <a href="{url}" target="_blank" class="btn-view">Ver Ficha ↗</a>
            </div>
        </div>
    </div>
    """

def generate_report(properties, output_path="reporte_propiedades.html"):
    """
    Genera el archivo HTML interactivo con las propiedades filtradas.
    """
    total = len(properties)
    now_str = datetime.now().strftime("%d/%m/%Y %H:%M")

    count_ramos = sum(1 for p in properties if p.get('zone') == 'Ramos Mejía')
    count_haedo = sum(1 for p in properties if p.get('zone') == 'Haedo')
    count_sarmiento = sum(1 for p in properties if p.get('zone') == 'Villa Sarmiento')

    prices = [p['price_usd'] for p in properties if 'price_usd' in p]
    min_precio_str = f"USD {min(prices):,}".replace(',', '.') if prices else "N/A"
    avg_precio_str = f"USD {int(sum(prices) / len(prices)):,}".replace(',', '.') if prices else "N/A"

    cards_html = "".join([generate_property_card_html(p) for p in properties])

    html_content = HTML_TEMPLATE.replace('{FECHA_ACTUALIZACION}', now_str) \
                                .replace('{TOTAL_PROPIEDADES}', str(total)) \
                                .replace('{MIN_PRECIO}', min_precio_str) \
                                .replace('{AVG_PRECIO}', avg_precio_str) \
                                .replace('{COUNT_RAMOS}', str(count_ramos)) \
                                .replace('{COUNT_HAEDO}', str(count_haedo)) \
                                .replace('{COUNT_SARMIENTO}', str(count_sarmiento)) \
                                .replace('{CARDS_HTML}', cards_html)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"[+] Reporte HTML generado exitosamente en: {output_path}")
    return os.path.abspath(output_path)


if __name__ == '__main__':
    sample = [{
        'id': 'test_1',
        'title': 'Venta Dúplex 3 ambientes con Patio',
        'price_usd': 65900,
        'zone': 'Ramos Mejía',
        'address': 'Constitución al 1100, Ramos Mejía',
        'features_text': 'APTO CRÉDITO | 3 ambientes | 2 dormitorios | patio',
        'expensas': 'Sin expensas',
        'image_url': '',
        'inmobiliaria': 'Nicolás Alvarez Propiedades',
        'whatsapp': '5491178341992',
        'phone': '1178341992',
        'url': 'https://example.com'
    }]
    generate_report(sample, 'test_report.html')
