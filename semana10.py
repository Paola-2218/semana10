import os

class Producto:
    def __init__(self, codigo, nombre, cantidad, precio):
        self.codigo = codigo
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def __str__(self):
        return f"{self.codigo},{self.nombre},{self.cantidad},{self.precio}"


class Inventario:
    def __init__(self, archivo="inventario.txt"):
        self.archivo = archivo
        self.productos = {}
        self.cargar_desde_archivo()

    def cargar_desde_archivo(self):
        """Carga los productos desde el archivo si existe"""
        if not os.path.exists(self.archivo):
            # Si no existe, lo crea vacío
            open(self.archivo, "w").close()
            return

        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                for linea in f:
                    datos = linea.strip().split(",")
                    if len(datos) == 4:
                        codigo, nombre, cantidad, precio = datos
                        self.productos[codigo] = Producto(codigo, nombre, int(cantidad), float(precio))
        except (FileNotFoundError, PermissionError) as e:
            print(f" Error al leer el archivo: {e}")

    def guardar_en_archivo(self):
        """Guarda todos los productos en el archivo"""
        try:
            with open(self.archivo, "w", encoding="utf-8") as f:
                for producto in self.productos.values():
                    f.write(str(producto) + "\n")
        except PermissionError:
            print(" No tienes permiso para escribir en el archivo.")
        except Exception as e:
            print(f" Error al guardar: {e}")

    def agregar_producto(self, codigo, nombre, cantidad, precio):
        if codigo in self.productos:
            print(" El producto ya existe en el inventario.")
        else:
            self.productos[codigo] = Producto(codigo, nombre, cantidad, precio)
            self.guardar_en_archivo()
            print(" Producto añadido exitosamente.")

    def actualizar_producto(self, codigo, cantidad=None, precio=None):
        if codigo in self.productos:
            if cantidad is not None:
                self.productos[codigo].cantidad = cantidad
            if precio is not None:
                self.productos[codigo].precio = precio
            self.guardar_en_archivo()
            print(" Producto actualizado correctamente.")
        else:
            print(" Producto no encontrado.")

    def eliminar_producto(self, codigo):
        if codigo in self.productos:
            del self.productos[codigo]
            self.guardar_en_archivo()
            print(" Producto eliminado correctamente.")
        else:
            print(" Producto no encontrado.")

    def mostrar_inventario(self):
        if not self.productos:
            print(" El inventario está vacío.")
        else:
            print("\n Inventario actual:")
            for producto in self.productos.values():
                print(f"🔹 {producto.codigo} | {producto.nombre} | Cantidad: {producto.cantidad} | Precio: ${producto.precio:.2f}")


# ====== Interfaz de usuario en consola ======
def menu():
    inventario = Inventario()

    while True:
        print("\n--- Menú de Gestión de Inventario ---")
        print("1. Mostrar inventario")
        print("2. Agregar producto")
        print("3. Actualizar producto")
        print("4. Eliminar producto")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            inventario.mostrar_inventario()
        elif opcion == "2":
            codigo = input("Ingrese código: ")
            nombre = input("Ingrese nombre: ")
            try:
                cantidad = int(input("Ingrese cantidad: "))
                precio = float(input("Ingrese precio: "))
                inventario.agregar_producto(codigo, nombre, cantidad, precio)
            except ValueError:
                print(" Error: cantidad y precio deben ser números.")
        elif opcion == "3":
            codigo = input("Ingrese código del producto a actualizar: ")
            try:
                cantidad = int(input("Nueva cantidad (deje en blanco si no desea cambiar): ") or -1)
                precio = float(input("Nuevo precio (deje en blanco si no desea cambiar): ") or -1)
                inventario.actualizar_producto(
                    codigo,
                    cantidad if cantidad != -1 else None,
                    precio if precio != -1 else None
                )
            except ValueError:
                print(" Error: cantidad y precio deben ser números.")
        elif opcion == "4":
            codigo = input("Ingrese código del producto a eliminar: ")
            inventario.eliminar_producto(codigo)
        elif opcion == "5":
            print(" Saliendo del sistema...")
            break
        else:
            print(" Opción no válida.")


# Ejecutar programa
if __name__ == "__main__":
    menu()
