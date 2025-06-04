class Product:
    def __init__(self, product_id: int):
        self.id = product_id
        self.history = []  # historial de pasos recorridos con tiempo
        self.completed = False
        self.entry_time = None
        self.exit_time = None
