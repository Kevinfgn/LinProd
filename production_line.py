import time
from collections import deque


class Task:
    
    #Simula una tarea o máquina que puede procesar productos uno a la vez.
    #Mantiene una cola FIFO y controla su tiempo de ejecución.
    

    def __init__(self, name, duration):
        self.name = name
        self.duration = duration          # Cuántos ciclos tarda en completarse
        self.queue = deque()              # Cola de productos esperando su turno
        self.current_product = None       # Producto actualmente en proceso
        self.remaining_time = 0           # Tiempo restante del producto actual
        self.busy = False                 # Estado ocupado/libre

    def enqueue_product(self, product):
        self.queue.append(product)

    def process(self):
        
        #Avanza un ciclo de procesamiento.
        #-Si está ocupado: reduce tiempo restante.
        #-Si termina: libera el producto.
        #-Si está libre: toma uno de la cola si existe.
        
        if self.busy:
            self.remaining_time -= 1
            if self.remaining_time <= 0:
                completed = self.current_product
                completed.history[-1]["end_time"] = time.time()
                self.current_product = None
                self.busy = False
                return completed
        elif self.queue:
            self.current_product = self.queue.popleft()
            wait_time = time.time() - self.current_product.entry_time if not self.current_product.history else time.time() - self.current_product.history[-1]["end_time"]

            self.busy = True
            self.remaining_time = self.duration
            self.current_product.history.append({
                "task": self.name,
                "process": getattr(self, "process_name", "Desconocido"),
                "start_time": time.time(),
                "end_time": None,
                "wait_time": wait_time
            })
        return None

    def status(self):
        
        ##Devuelve un diccionario con información de estado para visualización.
        
        return {
            "task": self.name,
            "busy": self.busy,
            "queue_length": len(self.queue),
            "current_product": self.current_product.id if self.current_product else None
        }


class Process:
    
    ##Representa un proceso (grupo de tareas) en la línea de producción.
    ##Tiene conexión hacia otro proceso, permitiendo una cadena.
    

    def __init__(self, name, is_start=False, is_end=False):
        self.name = name
        self.tasks = []
        self.next_process = None
        self.is_start = is_start
        self.is_end = is_end

    def add_task(self, task: Task):
        task.process_name = self.name  # Inject process name
        self.tasks.append(task)

    def set_next_process(self, process):
        self.next_process = process

    def enqueue_product(self, product):
        
        ##Encola un producto en la primera tarea del proceso.
        
        if self.tasks:
            self.tasks[0].enqueue_product(product)

    def run_cycle(self):
        
        ##Ejecuta un ciclo de todas las tareas del proceso en orden.
        ##Mueve productos a tareas siguientes o al siguiente proceso.
        
        for i, task in enumerate(self.tasks):
            result = task.process()
            if result:
                if i < len(self.tasks) - 1:
                    self.tasks[i + 1].enqueue_product(result)
                elif self.next_process:
                    self.next_process.enqueue_product(result)
                elif self.is_end:
                    result.completed = True
                    result.exit_time = time.time()
                    return result
        return None
