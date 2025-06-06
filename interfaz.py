#Interfaz gráfica

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import time
from product import Product
from simulator import Simulator
from reports import generate_report

class ProcessCreationDialog(tk.Toplevel):
    def __init__(self, parent, existing_starts, existing_ends):
        super().__init__(parent)
        self.title("Nuevo Proceso")
        self.resizable(False, False)
        self.result = None

        ttk.Label(self, text="Nombre del Proceso:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.name_entry = ttk.Entry(self, width=30)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        self.is_start_var = tk.BooleanVar()
        self.is_end_var = tk.BooleanVar()

        self.chk_start = ttk.Checkbutton(self, text="Proceso Inicial", variable=self.is_start_var, command=self.on_check_start)
        self.chk_start.grid(row=1, column=0, columnspan=2, padx=10, sticky="w")

        self.chk_end = ttk.Checkbutton(self, text="Proceso Final", variable=self.is_end_var, command=self.on_check_end)
        self.chk_end.grid(row=2, column=0, columnspan=2, padx=10, sticky="w")

        self.chk_start.grid(row=1, column=0, columnspan=2, padx=10, sticky="w")
        self.chk_end.grid(row=2, column=0, columnspan=2, padx=10, sticky="w")

        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Crear", command=self.on_submit).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=self.destroy).pack(side="left", padx=5)

        self.existing_starts = existing_starts
        self.existing_ends = existing_ends

        self.name_entry.focus()
        self.grab_set()  # Bloquear interacción con la ventana principal

    def on_submit(self):
        name = self.name_entry.get().strip()
        if not name:
            tk.messagebox.showerror("Error", "Debe ingresar un nombre.")
            return
        if self.is_start_var.get() and self.existing_starts:
            tk.messagebox.showerror("Error", "Ya existe un proceso inicial.")
            return
        if self.is_end_var.get() and self.existing_ends:
            tk.messagebox.showerror("Error", "Ya existe un proceso final.")
            return
        self.result = {
            "name": name,
            "is_start": self.is_start_var.get(),
            "is_end": self.is_end_var.get()
        }
        self.destroy()

    def on_check_start(self):
        if self.is_start_var.get():
            self.is_end_var.set(False)

    def on_check_end(self):
        if self.is_end_var.get():
            self.is_start_var.set(False)



class ProcessUI:
    """Clase para representar visualmente un proceso en la GUI."""
    def __init__(self, parent, process_name, is_start=False, is_end=False):
        self.process_name = process_name
        self.is_start = is_start
        self.is_end = is_end
        self.tasks = []

        self.frame = ttk.LabelFrame(parent, text=f"Proceso: {process_name}")

        ttk.Label(self.frame, text=f"Nombre del proceso: {process_name}").pack(anchor="w", padx=10)

        tipo = []
        if is_start:
            tipo.append("Inicial")
        if is_end:
            tipo.append("Final")
        if tipo:
            ttk.Label(self.frame, text=f"Tipo: {', '.join(tipo)}").pack(anchor="w", padx=10)

        # Frame donde se listan las tareas agregadas
        self.task_list_frame = ttk.Frame(self.frame)
        self.task_list_frame.pack(anchor="w", padx=20)

        # Selector para enlazar al siguiente proceso
        ttk.Label(self.frame, text="Siguiente proceso:").pack(anchor="w", padx=10, pady=(10, 0))
        self.next_process_var = tk.StringVar()
        self.next_process_dropdown = ttk.Combobox(self.frame, textvariable=self.next_process_var, state="readonly")
        self.next_process_dropdown.pack(anchor="w", padx=10, pady=(0, 10))


        def set_available_next_processes(self, process_names):
            """Actualiza las opciones del dropdown con los nombres disponibles."""
            opciones = [name for name in process_names if name != self.process_name]
            self.next_process_dropdown['values'] = opciones


    def add_task(self):
        task_name = simpledialog.askstring("Nombre de la Tarea", "Ingrese el nombre de la tarea:")
        if not task_name:
            return

        try:
            duration = int(simpledialog.askstring("Duración", "Ingrese la duración (en ciclos):"))
        except (TypeError, ValueError):
            tk.messagebox.showerror("Error", "La duración debe ser un número entero.")
            return

        # Guardar la tarea
        # Mostrar visualmente
        label_text = f"{task_name} - {duration} ciclos"
        label = tk.Label(self.task_list_frame, text=label_text, anchor="w", bg="lightgray")
        label.pack(fill="x", pady=1)
        self.tasks.append({
            "name": task_name,
            "duration": duration,
            "label": label
        })

    def set_available_next_processes(self, process_names):
        """Actualiza las opciones del dropdown con los nombres disponibles."""
        opciones = [name for name in process_names if name != self.process_name]
        self.next_process_dropdown['values'] = opciones


class AppGUI:
    """Ventana principal del sistema."""
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Línea de Producción")

        self.process_uis = []
        self.simulador = None
        self.productos = []

        # 🔹 Contenedor horizontal para botones principales
        controls_frame = ttk.Frame(root)
        controls_frame.pack(pady=10)

        self.btn_add_process = ttk.Button(controls_frame, text="➕ Agregar Proceso", command=self.add_process)
        self.btn_add_process.pack(side="left", padx=5)

        self.btn_add_task = ttk.Button(controls_frame, text="➕ Agregar Tarea", command=self.add_task_globally)
        self.btn_add_task.pack(side="left", padx=5)

        self.btn_run_simulation = ttk.Button(controls_frame, text="▶️ Iniciar Simulación", command=self.build_simulation)
        self.btn_run_simulation.pack(side="left", padx=5)

        self.pause_requested = False
        self.btn_pause = ttk.Button(controls_frame, text="⏸️ Pausar", command=self.request_pause)
        self.btn_pause.pack(side="left", padx=5)

        self.btn_continue = ttk.Button(controls_frame, text="▶️ Reanudar", command=self.continue_simulation, state="disabled")
        self.btn_continue.pack(side="left", padx=5)

        # Campo de cantidad de productos
        cantidad_frame = ttk.Frame(root)
        cantidad_frame.pack(pady=5)
        ttk.Label(cantidad_frame, text="Cantidad de productos:").pack(side="left", padx=(0, 5))
        self.num_products_var = tk.StringVar(value="5")
        ttk.Entry(cantidad_frame, textvariable=self.num_products_var, width=5).pack(side="left")

        # Contenedor de procesos en cuadrícula
        self.process_container = ttk.Frame(root)
        self.process_container.pack(fill="both", expand=True, padx=10, pady=5)

        # Panel de estado de simulación
        self.log_frame = ttk.LabelFrame(root, text="Estado de la Simulación")
        self.log_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.log_text = tk.Text(self.log_frame, height=15, wrap="none", state="disabled", bg="#f4f4f4")
        self.log_text.pack(fill="both", expand=True)

        self.current_cycle = 0


    def add_process(self):
        existing_start = any(p.is_start for p in self.process_uis)
        existing_end = any(p.is_end for p in self.process_uis)

        dialog = ProcessCreationDialog(self.root, existing_start, existing_end)
        self.root.wait_window(dialog)

        if dialog.result:
            data = dialog.result
            ui = ProcessUI(self.process_container, data["name"], is_start=data["is_start"], is_end=data["is_end"])
            self.process_uis.append(ui)
            col = len(self.process_uis) - 1
            ui.frame.grid(row=0, column=col, padx=10, pady=5, sticky="n")
            self.update_next_process_options()
            self.update_next_process_options()

    def update_next_process_options(self):
        names = [p.process_name for p in self.process_uis]
        for p in self.process_uis:
            p.set_available_next_processes(names)

    def build_simulation(self):
        from production_line import Process, Task  # Importación aquí para evitar dependencia circular

        procesos = {}
        relaciones = {}

        # Crear procesos
        for ui in self.process_uis:
            p = Process(ui.process_name, is_start=ui.is_start, is_end=ui.is_end)
            for task_data in ui.tasks:
                task = Task(task_data["name"], task_data["duration"])
                task._ui_label = task_data["label"]  # referencia visual
                p.add_task(task)

            procesos[ui.process_name] = p

            if ui.next_process_var.get():
                relaciones[ui.process_name] = ui.next_process_var.get()

        # Validaciones básicas
        iniciales = [p for p in procesos.values() if p.is_start]
        finales = [p for p in procesos.values() if p.is_end]
        if len(iniciales) != 1 or len(finales) != 1:
            tk.messagebox.showerror("Error", "Debe haber exactamente un proceso inicial y uno final.")
            return

        # Enlazar procesos
        for nombre, siguiente in relaciones.items():
            procesos[nombre].set_next_process(procesos[siguiente])

        # Mostrar resumen en consola
        print("\n✅ Configuración de la línea de producción construida correctamente:")
        for p in procesos.values():
            tipo = " (Inicial)" if p.is_start else " (Final)" if p.is_end else ""
            print(f"Proceso: {p.name}{tipo}")
            for t in p.tasks:
                print(f"   - Tarea: {t.name} ({t.duration} ciclos)")
            if p.next_process:
                print(f"   ↳ Siguiente: {p.next_process.name}")
        
        # Crear productos
        try:
            num = int(self.num_products_var.get())
            if num <= 0:
                raise ValueError
        except ValueError:
            tk.messagebox.showerror("Error", "Ingrese una cantidad válida de productos.")
            return


        productos = [Product(i) for i in range(num)]

        # Lanzar simulación
        self.log("Iniciando simulación...")

        sim = Simulator(productos, list(procesos.values()), max_cycles=100)
        self.simulador = sim
        self.productos = productos
        self.current_cycle = 0

        self.root.update_idletasks()

        for p in productos:
            p.entry_time = time.time()
            procesos[iniciales[0].name].enqueue_product(p)

        ciclo = self.current_cycle
        while ciclo < 100 and len(sim.completed_products) < len(productos):
            if self.pause_requested:
                self.log("\n⏸️ Simulación pausada por el usuario.")
                self.pause_requested = False
                self.current_cycle = ciclo
                self.btn_continue["state"] = "normal"
                break

            self.log(f"\n Ciclo {ciclo}")
            self.root.update()

            for process in sim.processes:
                self.log(f"[{process.name}]")
                result = process.run_cycle()
                if result:
                    sim.completed_products.append(result)

                for task in process.tasks:
                    status = task.status()
                    label = getattr(task, "_ui_label", None)
                    if status["busy"]:
                        mensaje = f"Procesando Producto {status['current_product']} ({task.remaining_time} ciclos restantes)"
                        if label:
                            label.config(bg="red", fg="white", text=f"🔴 {task.name} - {mensaje}")
                    elif task.queue:
                        mensaje = f"Esperando {len(task.queue)} producto/s"
                        if label:
                            label.config(bg="gold", fg="black", text=f"🟡 {task.name} - {mensaje}")
                    else:
                        mensaje = "Libre"
                        if label:
                            label.config(bg="lightgreen", fg="black", text=f"🟢 {task.name} - {mensaje}")


            ciclo += 1
            time.sleep(1)

        if len(sim.completed_products) == len(productos):
            self.log("\n✅ Todos los productos procesados.")
            self.log("\n Reporte Final:")
            reporte = generate_report(sim.completed_products)
            for k, v in reporte.items():
                if isinstance(v, (int, float)):
                    self.log(f" - {k.replace('_', ' ').capitalize()}: {v:.2f} segundos")
                else:
                    self.log(f" - {k.replace('_', ' ').capitalize()}: {v}")
            ReportWindow(self.root, reporte)



        # Mostrar reporte
        print("\n Reporte Final:")
        reporte = generate_report(sim.completed_products)
        for k, v in reporte.items():
            if isinstance(v, (int, float)):
                print(f" - {k.replace('_', ' ').capitalize()}: {v:.2f} segundos")
            else:
                print(f" - {k.replace('_', ' ').capitalize()}: {v}")


        ventana_reporte = ReportWindow(self.root, reporte)


    #Para escribir en el panel
    def log(self, mensaje):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", mensaje + "\n")
        self.log_text.see("end")  
        self.log_text.configure(state="disabled")
    
    #pausar simulación
    def request_pause(self):
        self.pause_requested = True
    
    #reanudar simulación
    def continue_simulation(self):
        sim = self.simulador
        productos = self.productos
        ciclo = self.current_cycle

        self.btn_continue["state"] = "disabled"
        self.log("\n Reanudando simulación...\n")

        while ciclo < 100 and len(sim.completed_products) < len(productos):
            if self.pause_requested:
                self.log("\n⏸️ Simulación pausada por el usuario.")
                self.pause_requested = False
                self.current_cycle = ciclo
                self.btn_continue["state"] = "normal"
                break

            self.log(f"\n Ciclo {ciclo}")
            self.root.update()

            for process in sim.processes:
                self.log(f"[{process.name}]")
                result = process.run_cycle()
                if result:
                    sim.completed_products.append(result)

                for task in process.tasks:
                    status = task.status()
                    label = getattr(task, "_ui_label", None)
                    if status["busy"]:
                        mensaje = f"Procesando Producto {status['current_product']} ({task.remaining_time} ciclos restantes)"
                        if label:
                            label.config(bg="red", fg="white", text=f"🔴 {task.name} - {mensaje}")
                    elif task.queue:
                        mensaje = f"Esperando {len(task.queue)} producto/s"
                        if label:
                            label.config(bg="gold", fg="black", text=f"🟡 {task.name} - {mensaje}")
                    else:
                        mensaje = "Libre"
                        if label:
                            label.config(bg="lightgreen", fg="black", text=f"🟢 {task.name} - {mensaje}")

            ciclo += 1
            time.sleep(1)

        # Finalización
        if len(sim.completed_products) == len(productos):
            from reports import generate_report
            self.log("\n✅ Todos los productos procesados.")
            self.log("\n Reporte Final:")
            reporte = generate_report(sim.completed_products)
            for k, v in reporte.items():
                self.log(f" - {k.replace('_', ' ').capitalize()}: {v:.2f} segundos")

            ventana_reporte = ReportWindow(self.root, reporte)
            self.simulador = None
            self.productos = []
            self.current_cycle = 0

    def add_task_globally(self):
        if not self.process_uis:
            messagebox.showinfo("Info", "Primero agregue al menos un proceso.")
            return

        process_names = [p.process_name for p in self.process_uis]
        dialog = TaskCreationDialog(self.root, process_names)
        self.root.wait_window(dialog)

        if dialog.result:
            data = dialog.result
            target = next(p for p in self.process_uis if p.process_name == data["process"])

            label_text = f"{data['name']} - {data['duration']} ciclos"
            label = tk.Label(target.task_list_frame, text=label_text, anchor="w", bg="lightgray")
            label.pack(fill="x", pady=1)

            target.tasks.append({
                "name": data["name"],
                "duration": data["duration"],
                "label": label
            })


class ReportWindow(tk.Toplevel):
    def __init__(self, parent, reporte):
        super().__init__(parent)
        self.title("📊 Reporte de Simulación")
        self.resizable(False, False)

        frame = ttk.Frame(self, padding=10)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Reporte", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 10))

        for key, value in reporte.items():
            label_text = f"{key.replace('_', ' ').capitalize()}: {value:.2f} segundos" if isinstance(value, float) else f"{key.replace('_', ' ').capitalize()}: {value}"
            ttk.Label(frame, text=label_text).pack(anchor="w")
        
        ttk.Button(frame, text="Cerrar", command=self.destroy).pack(pady=10)

class TaskCreationDialog(tk.Toplevel):
    def __init__(self, parent, process_names):
        super().__init__(parent)
        self.title("Nueva Tarea")
        self.resizable(False, False)
        self.result = None

        ttk.Label(self, text="Nombre de la tarea:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.task_entry = ttk.Entry(self)
        self.task_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self, text="Duración (ciclos):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.duration_entry = ttk.Entry(self)
        self.duration_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self, text="Proceso destino:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.process_var = tk.StringVar()
        self.process_dropdown = ttk.Combobox(self, textvariable=self.process_var, values=process_names, state="readonly")
        self.process_dropdown.grid(row=2, column=1, padx=10, pady=5)

        ttk.Button(self, text="Agregar", command=self.on_submit).grid(row=3, column=0, columnspan=2, pady=10)

        self.grab_set()

    def on_submit(self):
        try:
            duration = int(self.duration_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Duración inválida")
            return

        name = self.task_entry.get().strip()
        process = self.process_var.get()

        if not name or not process:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        self.result = {"name": name, "duration": duration, "process": process}
        self.destroy()



if __name__ == "__main__":
    root = tk.Tk()
    app = AppGUI(root)
    root.mainloop()
