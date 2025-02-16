import xml.etree.ElementTree as ET
import requests
from io import StringIO

def filter_sitemap(url, output_file, product='platform'):
    try:
        # Descargar el sitemap
        response = requests.get(url)
        response.raise_for_status()
        
        # Crear el elemento raíz con el namespace correcto
        root = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
        
        # Agregar el elemento script
        script = ET.SubElement(root, 'script')
        
        # Parsear el XML descargado para procesar sus URLs
        downloaded_root = ET.fromstring(response.content)
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        # Filter URLs
        filter_prefix = f'https://docs.confluent.io/{product}/'
        for url_elem in downloaded_root.findall('.//ns:url', namespace):
            loc = url_elem.find('ns:loc', namespace)
            if loc is not None and loc.text.startswith(filter_prefix):
                # Crear nuevo elemento url
                url = ET.SubElement(root, 'url')
                # Agregar loc
                loc_new = ET.SubElement(url, 'loc')
                loc_new.text = loc.text
                # Agregar lastmod
                lastmod = url_elem.find('ns:lastmod', namespace)
                if lastmod is not None:
                    lastmod_new = ET.SubElement(url, 'lastmod')
                    lastmod_new.text = lastmod.text
                # Agregar changefreq
                changefreq = url_elem.find('ns:changefreq', namespace)
                if changefreq is not None:
                    changefreq_new = ET.SubElement(url, 'changefreq')
                    changefreq_new.text = changefreq.text
        
        # Convertir el XML a string con la indentación correcta
        def indent(elem, level=0):
            i = "\n" + level*"  "
            if len(elem):
                if not elem.text or not elem.text.strip():
                    elem.text = i + "  "
                if not elem.tail or not elem.tail.strip():
                    elem.tail = i
                for subelem in elem:
                    indent(subelem, level+1)
                if not elem.tail or not elem.tail.strip():
                    elem.tail = i
            else:
                if level and (not elem.tail or not elem.tail.strip()):
                    elem.tail = i

        # Aplicar indentación
        indent(root)
        
        # Escribir el archivo manualmente para evitar la declaración XML
        with open(output_file, 'w', encoding='utf-8') as f:
            xml_str = ET.tostring(root, encoding='unicode')
            f.write(xml_str)
        
        print(f"Sitemap filtrado para '{product}' guardado en {output_file}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar el sitemap: {e}")
    except ET.ParseError as e:
        print(f"Error al parsear el XML: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

# URL del sitemap y archivo de salida
sitemap_url = 'https://docs.confluent.io/home/sitemap.xml'
product = 'platform'  # Aquí puedes cambiar a 'cloud' u otro valor
output_file = f'filtered_{product}_sitemap.xml'

# Ejecutar la función
filter_sitemap(sitemap_url, output_file, product) 