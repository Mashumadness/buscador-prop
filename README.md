# 🏠 Buscador de Propiedades (Zona Oeste)

Buscador automático local para encontrar **PHs y departamentos tipo casa** en **Ramos Mejía**, **Haedo** y **Villa Sarmiento** directo desde inmobiliarias independientes (agregadores directos de CRMs locales como Xintel y Tokko, sin depender exclusivamente de portales tradicionales como Zonaprop o Argenprop).

---

## 🎯 Criterios de Búsqueda y Filtrado

* **Tipología:** PH / Departamento tipo casa / Dúplex.
* **Ubicaciones:** Ramos Mejía, Haedo, Villa Sarmiento (GBA Oeste).
* **Ambientes:** $\ge 3$ ambientes o $\ge 2$ dormitorios.
* **Financiamiento:** **Exclusivo Apto Crédito Hipotecario** (con validación estricta para descartar avisos con *"NO apto crédito"*).
* **Presupuesto:** Hasta **USD 100.000** (ordenados por oportunidad de menor a mayor).

---

## 🚀 Características

* **Rastreo Multi-Portal:** Conecta con plataformas de inmobiliarias locales (BuscadorProp, Liderprop, etc.).
* **Filtro Inteligente:** Normaliza precios en USD, valida dormitorios/ambientes y descarta falsos positivos de crédito bancario.
* **Reporte HTML Interactivo:** Genera un dashboard visual (`reporte_propiedades.html`) con fotos, detalles, filtros por zona al vuelo y buscador en tiempo real.
* **Contacto Directo por WhatsApp:** Cada tarjeta cuenta con un botón verde que abre una conversación de WhatsApp con el corredor inmobiliario con un mensaje pre-armado consultando por la propiedad.
* **Lanzador de 1 Clic (Windows):** Archivo `.bat` y acceso directo para correrlo con doble clic.

---

## 🛠️ Instalación y Uso

### 1. Requisitos Previos
* Python 3.10 o superior instalado.
* Git.

### 2. Instalación de Dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecución
#### Desde la terminal:
```bash
python main.py
```
*(Opcional: podés pasar un monto máximo en dólares como parámetro, e.g. `python main.py 90000`).*

#### Desde Windows con doble clic:
* Ejecutar el archivo `ejecutar_buscador.bat`.
* El script rastreará los avisos, aplicará los filtros y abrirá automáticamente el reporte en tu navegador predeterminado.

---

## 📂 Estructura del Proyecto

```text
buscador_propiedades/
├── scraper_buscadorprop.py  # Extractor para BuscadorProp (Ramos Mejía, Haedo, Villa Sarmiento)
├── scraper_liderprop.py     # Extractor para Liderprop (Avisos apto crédito)
├── filter_engine.py         # Motor de validación (precios, apto crédito, ambientes)
├── report_generator.py      # Generador del dashboard visual en HTML
├── main.py                  # Orquestador del flujo completo
├── ejecutar_buscador.bat    # Script ejecutable de Windows de 1 clic
├── requirements.txt         # Dependencias Python
└── README.md                # Documentación del proyecto
```
