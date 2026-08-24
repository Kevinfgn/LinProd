class Product:
    
    ##Representa un producto que fluye a través de la línea de producción.
    ##Guarda su historial de pasos y tiempo de entrada/salida.
    def __init__(self, product_id: int):
        self.id = product_id
        self.history = []        # Lista para registrar eventos de procesamiento
        self.completed = False   # Indica si terminó toda la línea
        self.entry_time = None   # Tiempo en que entró al sistema
        self.exit_time = None    # Tiempo en que salió (si completó)
