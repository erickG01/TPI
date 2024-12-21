import json
from django.conf import settings

def get_color_scheme():
    try:
        with open(settings.COLOR_FILE, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        # Valores predeterminados si el archivo no existe
        return {
            "primary_color": "bg-dark",
            "secondary_color": "text-white",
            "background_color": "bg-light",
            "text_color": "text-dark"
        }
