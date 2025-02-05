"""
compute_sales.py

Este script calcula el costo total de las ventas basado en un catálogo de
precios y un registro de ventas.

Uso:
    python computeSales.py priceCatalogue.json salesRecord.csv

Parámetros:
    - priceCatalogue.json: Archivo JSON con los precios de los productos.
    - salesRecord.csv: Archivo CSV con los registros de ventas.

Salida:
    - Imprime el total de ventas y el tiempo de ejecución en la consola.
    - Guarda los resultados en un archivo SalesResults.txt.

Manejo de errores:
    - Maneja archivos no encontrados y formatos incorrectos.
    - Continúa la ejecución a pesar de errores en los datos de entrada.
"""
import json
import sys
import time
import csv


def load_json_file(file_path):
    """Carga un archivo JSON y maneja errores"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            print(f"Error: El archivo {file_path} no es un JSON válida.")
    except FileNotFoundError:
        print(f"Error: El archivo {file_path} no se encontró.")
    except json.JSONDecodeError:
        print(f"Error: El archivo {file_path} tiene un formato JSON inválido.")
    except (OSError, IOError) as file_error:
        print(f"Error inesperado al leer {file_path}: {file_error}")
    return None


def load_csv_file(file_path):
    """Carga un archivo CSV y maneja errores"""
    sales_record = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if len(row) != 2:
                    print(f"Error: Fila inválida en {file_path}: {row}")
                    continue
                product, quantity = row
                try:
                    quantity = int(quantity)
                    sales_record.append(
                        {
                            "product": product,
                            "quantity": quantity
                        }
                    )
                except ValueError:
                    print(f"Error: {quantity} inválido para {product}")
    except FileNotFoundError:
        print(f"Error: El archivo {file_path} no se encontró.")
    except (OSError, IOError) as file_error:
        print(f"Error inesperado al leer {file_path}: {file_error}")
    return sales_record


def compute_total_sales(price_catalogue, sales_record):
    """Calcula el costo total de todas las ventas registradas"""
    total_cost = 0.0
    errors = []
    price_dict = {item["title"]: item["price"] for item in price_catalogue}
    for sale in sales_record:
        product = sale.get("Product")
        quantity = sale.get("Quantity")
        if product is None or quantity is None:
            errors.append(f"Registro inválido en ventas: {sale}")
            continue
        if product not in price_dict:
            errors.append(f"{product} no encontrado en el catálogo")
            continue
        if not isinstance(quantity, (int, float)) or quantity < 0:
            errors.append(f"Cantidad {quantity} inválido para {product}")
            continue
        price = price_dict[product]
        total_cost += price * quantity
    return total_cost, errors


def main():
    """Función principal que ejecuta el programa"""
    if len(sys.argv) != 3:
        print("Usa: python compute_sales.py precios.json ventas.csv")
        sys.exit(1)
    price_catalogue_file = sys.argv[1]
    sales_record_file = sys.argv[2]
    start_time = time.time()
    price_catalogue = load_json_file(price_catalogue_file)
    sales_record = load_json_file(sales_record_file)
    if price_catalogue is None or not sales_record:
        print("Error: No se pudieron cargar los archivos correctamente.")
        sys.exit(1)
    total_cost, errors = compute_total_sales(price_catalogue, sales_record)
    execution_time = time.time() - start_time
    result_message = (
        f"Total de ventas: ${total_cost:.2f}\n"
        f"Tiempo de ejecución: {execution_time:.4f} segundos\n"
    )
    print(result_message)
    if errors:
        print("Errores encontrados:")
        for error in errors:
            print(f" - {error}")
    with open("SalesTC1Results.txt", "w", encoding="utf-8") as result_file:
        result_file.write(result_message)
        if errors:
            result_file.write("Errores encontrados:\n")
            for error in errors:
                result_file.write(f" - {error}\n")


if __name__ == "__main__":
    main()
