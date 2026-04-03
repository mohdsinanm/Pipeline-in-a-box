from src.celery_app import celery

@celery.task(bind=True)
def count_dna(self, filepath):
    counts = {"A": 0, "C": 0, "T": 0, "G": 0}

    try:
        with open(filepath, "r") as f:
            for line in f:
                for char in line.strip().upper():
                    if char in counts:
                        counts[char] += 1

        return {
            "status": "success",
            "counts": counts
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }