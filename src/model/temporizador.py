import time

class Temporizador:
    def __enter__(self):
        self.inicio = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.fin = time.perf_counter()
        self.total = self.fin - self.inicio
        print(f"Tiempo de ejecucion: {self.total:.4f} seg.")