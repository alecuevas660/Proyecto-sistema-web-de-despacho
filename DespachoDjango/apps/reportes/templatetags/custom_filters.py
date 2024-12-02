from django import template

register = template.Library()

@register.filter
def punto_miles(value):
    # Asegurarse de que el valor sea un número
    try:
        # Convertir el valor a float (para soportar decimales)
        value = float(value)
        
        # Formatear el número con puntos como separadores de miles
        formatted_value = "{:,.0f}".format(value).replace(",", "X").replace(".", ",").replace("X", ".")
        
        # Retornar el valor formateado
        return formatted_value
    except (ValueError, TypeError):
        return value  # Si no se puede convertir, retorna el valor original