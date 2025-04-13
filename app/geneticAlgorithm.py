import random

# Configuracion gentica
from .genes_conf import gene_bits, encoding, decoding 

class GeneticAlgorithm:
    
    def __init__(self, target, pop_size, mutation_rate, crossover_rate):
        self.target = target
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.chromosome_length = 40  # 10 genes x 4 bits
        self.population = [self.random_chromosome() for _ in range(pop_size)]

    def random_chromosome(self):
        # Retorna una cadena de 40 bits (10 genes * 4 bits)
        return ''.join(random.choice(list(decoding.values())) for _ in range(10))

    def decode(self, chromosome):
        # Divide cada 4 bits (genes)
        bits_list = [chromosome[i:i + gene_bits] for i in range(0, len(chromosome), 4)]
        # Convierte a dígito / operador
        expr_raw = []
        for g in bits_list:
            if g in encoding:
                expr_raw.append(encoding[g])

        # Validar secuencia: numero -> operador -> numero -> operador -> ...
        filtered = []
        expect_number = True
        for ch in expr_raw:
            if expect_number and ch.isdigit():
                filtered.append(ch)
                expect_number = False
            elif not expect_number and ch in '+-*/':
                filtered.append(ch)
                expect_number = True

        # Si termina en operador, quítalo
        if filtered and filtered[-1] in '+-*/':
            filtered.pop()

        return ''.join(filtered)

    def fitness(self, chromosome):
        expr = self.decode(chromosome)
        if not expr:
            # Si la expresión está vacía, devuelva fitness muy bajo
            return 0.0001
        try:
            result = eval(expr)
            # Si el resultado es exacto, fitness infinito
            if result == self.target:
                return float('inf')
            return 1 / abs(self.target - result)
        except:
            # Cualquier excepción => fitness muy bajo (por ej. division zero)
            return 0.0001

    def roulette_wheel(self, scored_pop):
        # scored_pop es lista de (chrom, score)
        total = sum(score for _, score in scored_pop)
        # Evita divisiones por cero si total ~ 0
        if total <= 0:
            return random.choice(scored_pop)[0]
        pick = random.uniform(0, total)
        current = 0
        for chrom, score in scored_pop:
            current += score
            if current > pick:
                return chrom
        return scored_pop[-1][0]  # fallback

    def crossover(self, parent1, parent2):
        # Con probabilidad crossover_rate, mezcla en un punto random
        if random.random() < self.crossover_rate:
            point = random.randint(1, len(parent1) - 1)
            c1 = parent1[:point] + parent2[point:]
            c2 = parent2[:point] + parent1[point:]
            return c1, c2
        return parent1, parent2

    def mutate(self, chromosome):
        # Invierte bits con probabilidad mutation_rate
        mutated = []
        for bit in chromosome:
            if random.random() < self.mutation_rate:
                mutated.append(str(1 - int(bit)))
            else:
                mutated.append(bit)
        return ''.join(mutated)

    def evolve(self):
        scored = [(chrom, self.fitness(chrom)) for chrom in self.population]
        # Ordenar por fitness descendente
        scored.sort(key=lambda x: x[1], reverse=True)
        # Elitismo: tomar el mejor cromosoma directamente
        new_population = [scored[0][0]]

        # Para mayor diversidad, opcionalmente se puede omitir el elitismo
        # new_population = []

        while len(new_population) < self.pop_size:
            p1 = self.roulette_wheel(scored)
            p2 = self.roulette_wheel(scored)
            c1, c2 = self.crossover(p1, p2)
            c1 = self.mutate(c1)
            c2 = self.mutate(c2)
            new_population.append(c1)
            if len(new_population) < self.pop_size:
                new_population.append(c2)

        self.population = new_population
        # Retorna el mejor (cromosoma, fitness)
        return scored[0]