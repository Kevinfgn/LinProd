import time

class Simulator:
    def __init__(self, products, processes, max_cycles=1000):
        self.products = products
        self.processes = processes
        self.max_cycles = max_cycles
        self.completed_products = []
        self.time = 0

    def run(self):
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



    def pause_and_report(self):
        print("\n--- Estado de la línea de producción ---")
        for process in self.processes:
            print(process.status())
