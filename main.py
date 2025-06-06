from product import Product
from production_line import Process, Task
from simulator import Simulator
from reports import generate_report


def build_production_line():
    
    #Crea y conecta los procesos y tareas de la línea de producción.
    #La estructura final es:
    #    Inicio:       T1.1 (2 ciclos) /Ensamblaje: Soldar Piezas(2 ciclos) -> Ajustar tornillos (1 ciclo)
    #    Intermedio:   T2.1 (3 ciclos) -> T2.2 (2 ciclos) /Pintura: Aplicar base(3 ciclos) -> Aplicar pintura(2 ciclos)
    #    Final:        T3.1 (1 ciclo) /Empaque: Insertar manual(1 ciclo) -> Cerrar caja(1 ciclo)
    
    # Crear procesos
    inicio = Process("Ensamblaje", is_start=True)
    intermedio = Process("Pintura")
    final = Process("Empaque", is_end=True)

    # Agregar tareas a cada proceso
    inicio.add_task(Task("Soldar Piezas", duration=2))
    inicio.add_task(Task("Ajustar tornillos", duration=1))
    intermedio.add_task(Task("Aplicar base", duration=3))
    intermedio.add_task(Task("Aplicar pintura", duration=2))
    final.add_task(Task("Insertar manual", duration=1))
    final.add_task(Task("Cerrar caja", duration=1))

    # Enlazar procesos en orden secuencial
    inicio.set_next_process(intermedio)
    intermedio.set_next_process(final)

    return [inicio, intermedio, final]


def main():
    print("🛠️ Configurando la línea de producción...\n")

    # Crear productos para simular
    num_productos = 5
    productos = [Product(i) for i in range(num_productos)]

    # Construir estructura de procesos y tareas
    procesos = build_production_line()

    # Mostrar la configuración antes de iniciar
    print("📋 Procesos y Tareas Configurados:")
    for proceso in procesos:
        print(f" - {proceso.name}:")
        for tarea in proceso.tasks:
            print(f"    • Tarea {tarea.name} (duración: {tarea.duration} ciclos)")
    print("\n🔄 Iniciando simulación con", num_productos, "productos...\n")

    # Ejecutar la simulación
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
