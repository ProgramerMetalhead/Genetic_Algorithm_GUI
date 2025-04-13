from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QSlider, QLineEdit, QTextEdit, QGroupBox, QFormLayout,
    QDialog, QVBoxLayout as QVLayout
)
from PyQt6.QtCore import Qt

# Para graficar con PyQt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

# importar algoritmo genetico
from .geneticAlgorithm import GeneticAlgorithm

class GAApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Genetic Algorithm GUI")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Input controls
        input_box = QGroupBox("GA Parameters")
        form_layout = QFormLayout()

        self.target_input = QLineEdit("42")
        self.pop_input = QLineEdit("100")

        self.mut_slider = QSlider(Qt.Orientation.Horizontal)
        self.cross_slider = QSlider(Qt.Orientation.Horizontal)
        self.mut_slider.setRange(0, 100)
        self.cross_slider.setRange(0, 100)
        self.mut_slider.setValue(1)   # 1%
        self.cross_slider.setValue(70)  # 70%

        form_layout.addRow("Target Number:", self.target_input)
        form_layout.addRow("Population Size:", self.pop_input)
        form_layout.addRow("Mutation Rate (%):", self.mut_slider)
        form_layout.addRow("Crossover Rate (%):", self.cross_slider)
        input_box.setLayout(form_layout)

        self.run_button = QPushButton("Run Evolution")
        self.run_button.clicked.connect(self.run_ga)

        self.output = QTextEdit()
        self.output.setReadOnly(True)

        layout.addWidget(input_box)
        layout.addWidget(self.run_button)
        layout.addWidget(QLabel("Output:"))
        layout.addWidget(self.output)

        self.setLayout(layout)

    def run_ga(self):
        try:
            target = int(self.target_input.text())
            pop_size = int(self.pop_input.text())
            mutation_rate = self.mut_slider.value() / 100
            crossover_rate = self.cross_slider.value() / 100
        except ValueError:
            self.output.setText("Invalid input! Make sure to enter valid numbers.")
            return

        ga = GeneticAlgorithm(target, pop_size, mutation_rate, crossover_rate)
        history = []
        self.best_scores = []  # Para graficar la evolución de la mejor aptitud

        for generation in range(100):
            best_chrom, best_score = ga.evolve()
            decoded = ga.decode(best_chrom)
            self.best_scores.append(best_score)
            history.append(f"Gen {generation+1}: {decoded} -> fitness={best_score:.4f}")

            if best_score == float('inf'):
                history.append(f"Solution found: {decoded}")
                break

        self.output.setText('\n'.join(history))

        # Llamamos a la función para mostrar la gráfica
        self.show_chart()

    def show_chart(self):
        # Crear un QDialog para alojar el gráfico
        dialog = QDialog(self)
        dialog.setWindowTitle("Evolución de la aptitud (Fitness)")

        # Crear la figura de matplotlib
        figure = plt.Figure()
        canvas = FigureCanvas(figure)

        ax = figure.add_subplot(111)
        ax.plot(range(1, len(self.best_scores) + 1), self.best_scores)
        ax.set_xlabel("Generación")
        ax.set_ylabel("Mejor Fitness")

        layout = QVLayout()
        layout.addWidget(canvas)
        dialog.setLayout(layout)

        # Renderizamos la gráfica
        canvas.draw()

        # Mostramos el diálogo
        dialog.exec()