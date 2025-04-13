import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QSlider, QLineEdit, QTextEdit, QGroupBox, QFormLayout
)
from PyQt6.QtCore import Qt

# Constants
genes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '*', '/']
gene_bits = 4
encoding = {f"{i:04b}": ch for i, ch in enumerate(genes)}
decoding = {ch: f"{i:04b}" for i, ch in enumerate(genes)}


class GeneticAlgorithm:
    def __init__(self, target, pop_size, mutation_rate, crossover_rate):
        self.target = target
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.chromosome_length = 40  # 10 genes x 4 bits
        self.population = [self.random_chromosome() for _ in range(pop_size)]

    def random_chromosome(self):
        return ''.join(random.choice(list(decoding.values())) for _ in range(10))

    def decode(self, chromosome):
        genes = [chromosome[i:i + gene_bits] for i in range(0, len(chromosome), gene_bits)]
        expr = []
        for g in genes:
            if g in encoding:
                expr.append(encoding[g])
        filtered = []
        expect_number = True
        for ch in expr:
            if expect_number and ch.isdigit():
                filtered.append(ch)
                expect_number = False
            elif not expect_number and ch in '+-*/':
                filtered.append(ch)
                expect_number = True
        return ''.join(filtered[:-1]) if filtered and not expect_number else ''.join(filtered)

    def fitness(self, chromosome):
        expr = self.decode(chromosome)
        try:
            result = eval(expr)
            if result == self.target:
                return float('inf')
            return 1 / abs(self.target - result)
        except:
            return 0.0001

    def roulette_wheel(self, scored_pop):
        total = sum(score for _, score in scored_pop)
        pick = random.uniform(0, total)
        current = 0
        for chrom, score in scored_pop:
            current += score
            if current > pick:
                return chrom

    def crossover(self, parent1, parent2):
        if random.random() < self.crossover_rate:
            point = random.randint(1, len(parent1) - 1)
            return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]
        return parent1, parent2

    def mutate(self, chromosome):
        return ''.join(
            bit if random.random() > self.mutation_rate else str(1 - int(bit))
            for bit in chromosome
        )

    def evolve(self):
        scored = [(chrom, self.fitness(chrom)) for chrom in self.population]
        scored.sort(key=lambda x: x[1], reverse=True)
        new_pop = [scored[0][0]]  # elitism
        while len(new_pop) < self.pop_size:
            p1 = self.roulette_wheel(scored)
            p2 = self.roulette_wheel(scored)
            c1, c2 = self.crossover(p1, p2)
            new_pop.append(self.mutate(c1))
            if len(new_pop) < self.pop_size:
                new_pop.append(self.mutate(c2))
        self.population = new_pop
        return scored[0]  # best


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
        self.mut_slider.setValue(1)
        self.cross_slider.setValue(70)

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
        for generation in range(100):
            best, score = ga.evolve()
            decoded = ga.decode(best)
            history.append(f"Gen {generation+1}: {decoded} -> {score:.4f}")
            if score == float('inf'):
                history.append(f"Solution found: {decoded}")
                break

        self.output.setText('\n'.join(history))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GAApp()
    window.resize(600, 500)
    window.show()
    sys.exit(app.exec())
