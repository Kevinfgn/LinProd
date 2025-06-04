def generate_report(products):
    if not products:
        return {}

    entry_times = [p.entry_time for p in products]
    exit_times = [p.exit_time for p in products]

    return {
        "total_products": len(products),
        "first_completion": min(exit_times) - min(entry_times),
        "last_completion": max(exit_times) - min(entry_times),
        "average_completion_time": sum(e - s for e, s in zip(exit_times, entry_times)) / len(products),
    }
