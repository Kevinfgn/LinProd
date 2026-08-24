def generate_report(products):
    if not products:
        return {}

    completed = [p for p in products if p.completed and p.exit_time]
    non_completed = [p for p in products if not p.completed]

    reporte = {
        "productos_completados": len(completed),
        "productos_no_completados": len(non_completed),
    }

    if not completed:
        return reporte

    entry_times = [p.entry_time for p in completed]
    exit_times = [p.exit_time for p in completed]
    total_processing_times = [e - s for e, s in zip(exit_times, entry_times)]
    avg_processing_time = sum(total_processing_times) / len(total_processing_times)

    # Collect durations and wait times per task
    task_durations = {}
    task_wait_times = {}
    task_process_map = {}

    for p in completed:
        for record in p.history:
            if record["end_time"] and record["start_time"]:
                task = record["task"]
                process = record.get("process", "Desconocido")
                duration = record["end_time"] - record["start_time"]
                wait_time = record.get("wait_time", 0)

                task_durations.setdefault(task, []).append(duration)
                task_wait_times.setdefault(task, []).append(wait_time)
                task_process_map[task] = process

    avg_wait_times = {k: sum(v)/len(v) for k, v in task_wait_times.items()}
    avg_task_times = {k: sum(v)/len(v) for k, v in task_durations.items()}

    # Bottleneck based on wait time
    bottleneck_task = max(avg_wait_times.items(), key=lambda x: x[1])[0] if avg_wait_times else None
    bottleneck_process = task_process_map.get(bottleneck_task, "Desconocido")
    bottleneck_wait = avg_wait_times.get(bottleneck_task, 0)



    total_wait_time = sum(sum(v) for v in task_wait_times.values())
    total_waits = sum(len(v) for v in task_wait_times.values())
    avg_wait_per_product = total_wait_time / len(completed) if completed else 0

    reporte.update({
        "tiempo_primer_producto": f"{(min(exit_times) - min(entry_times)):.2f} segundos",
        "tiempo_ultimo_producto": f"{(max(exit_times) - min(entry_times)):.2f} segundos",
        "tiempo_promedio_en_terminar": f"{avg_processing_time:.2f} segundos",
        "proceso_y_tarea_cuello_botella": f"{bottleneck_process} [{bottleneck_task}]",
        "espera_promedio_en_cuello_botella": f"{bottleneck_wait:.2f} segundos",
        "tiempo_promedio_de_espera_general": f"{avg_wait_per_product:.2f} segundos",
        "tiempo_total_de_procesamiento": f"{sum(total_processing_times):.2f} segundos",
    })

    return reporte
