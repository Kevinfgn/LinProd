from product import Product
from production_line import Process, Task
from simulator import Simulator
from reports import generate_report


def build_production_line():
    """
    Crea y conecta los procesos y tareas de la línea de producción.
    La estructura final es:
        Inicio:       T1.1 (2 ciclos)
        Intermedio:   T2.1 (3 ciclos) -> T2.2 (2 ciclos)
        Final:        T3.1 (1 ciclo)
    """
    # Crear procesos
    inicio = Process("Inicio", is_start=True)
    intermedio = Process("Intermedio")
    final = Process("Final", is_end=True)

    # Agregar tareas a cada proceso (simulan máquinas)
    inicio.add_task(Task("T1.1", duration=2))
    intermedio.add_task(Task("T2.1", duration=3))
    intermedio.add_task(Task("T2.2", duration=2))
    final.add_task(Task("T3.1", duration=1))

    # Enlazar los procesos para formar la línea de producción
    inicio.set_next_process(intermedio)
    intermedio.set_next_process(final)

    return [inicio, intermedio, final]


def main():
    print("🛠️ Configurando la línea de producción...\n")

    # Crear productos para procesar
    num_productos = 5
    productos = [Product(i) for i in range(num_productos)]

    # Construir la línea de producción
    procesos = build_production_line()

    print("📋 Procesos y Tareas Configurados:")
    for proceso in procesos:
        print(f" - {proceso.name}:")
        for tarea in proceso.tasks:
            print(f"    • Tarea {tarea.name} (duración: {tarea.duration} ciclos)")
    print("\n🔄 Iniciando simulación con", num_productos, "productos...\n")

    # Ejecutar la simulación por ciclos de tiempo
    simulador = Simulator(productos, procesos, max_cycles=50)
    simulador.run()

    # Generar y mostrar la reportería final
    print("\n📊 Reporte Final de Simulación:")
    estadisticas = generate_report(simulador.completed_products)
    for clave, valor in estadisticas.items():
        print(f" - {clave.replace('_', ' ').capitalize()}: {valor:.2f} segundos")

    print("\n✅ Simulación completada.")


if __name__ == "__main__":
    main()
