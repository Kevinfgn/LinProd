import time

class Simulator:
    
    #Controlador de la simulación: administra los ciclos de tiempo,
    #mueve productos y recoge estadísticas.
    

    def __init__(self, products, processes, max_cycles=1000):
        self.products = products
        self.processes = processes
        self.max_cycles = max_cycles
        self.completed_products = []
        self.time = 0

    def run(self):
        
        #Inicia y ejecuta la simulación por ciclos:
        #- En cada ciclo: cada proceso trabaja sus tareas.
        #- Se imprime el estado de cada tarea.
        #- Cuando todos los productos terminan o se alcanza el máximo de ciclos, se detiene.
        
        for p in self.products:
            p.entry_time = time.time()
            self.processes[0].enqueue_product(p)

        while self.time < self.max_cycles and len(self.completed_products) < len(self.products):
            print(f"\n🕒 Ciclo {self.time}")

            for process in self.processes:
                print(f"[{process.name}]")
                result = process.run_cycle()
                if result:
                    self.completed_products.append(result)

                for task in process.tasks:
                    status = task.status()

                    if status["busy"]:
                        print(
                            f"  - {status['task']}: Procesando Producto {status['current_product']} "
                            f"({task.remaining_time} ciclos restantes)"
                        )
                    elif task.queue:
                        print(
                            f"  - {status['task']}: Esperando (en cola {len(task.queue)} producto/s)"
                        )
                    else:
                        print(
                            f"  - {status['task']}: Libre"
                        )

            self.time += 1
            time.sleep(1)
