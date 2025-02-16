import xml.etree.ElementTree as ET
import requests
from io import StringIO

def filter_sitemap(url, output_file, product='platform'):
    try:
        # Descargar el sitemap
        response = requests.get(url)
        response.raise_for_status()  # Verificar si hubo errores en la descarga
        
        # Parsear el XML desde el contenido descargado
        root = ET.fromstring(response.content)
        
        # Define the namespace
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        # Find all URL elements
        urls = root.findall('ns:url', namespace)
        
        # Keep track of URLs to remove
        urls_to_remove = []
        
        # Filter URLs
        filter_prefix = f'https://docs.confluent.io/{product}/'
        for url in urls:
            loc = url.find('ns:loc', namespace)
            if loc is not None:
                if not loc.text.startswith(filter_prefix):
                    urls_to_remove.append(url)
        
        # Remove unwanted URLs
        for url in urls_to_remove:
            root.remove(url)
        
        # Write the filtered XML to a new file
        tree = ET.ElementTree(root)
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        
        print(f"Sitemap filtrado para '{product}' guardado en {output_file}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar el sitemap: {e}")
    except ET.ParseError as e:
        print(f"Error al parsear el XML: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

# URL del sitemap y archivo de salida
sitemap_url = 'https://docs.confluent.io/home/sitemap.xml'
product = 'cloud'  # Aquí puedes cambiar a 'cloud' u otro valor
output_file = f'filtered_{product}_sitemap.xml'

# Ejecutar la función
filter_sitemap(sitemap_url, output_file, product) 