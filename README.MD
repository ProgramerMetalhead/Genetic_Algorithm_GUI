# 🧬 Genetic Algorithm GUI - Documentación

## 📌 Propósito del Proyecto

Esta aplicación es una implemetaciion del contendio explicado en le blog http://www.ai-junkie.com/ga/intro/gat2.html **encontrar una expresión matemática** (usando dígitos del 0 al 9 y operadores `+ - * /`) que se **aproxime o iguale a un número objetivo** dado por el usuario. Para lograrlo, se utiliza un **algoritmo genético**, una técnica inspirada en la evolución biológica, para explorar posibles soluciones.

---

## ⚙️ Funcionamiento General

- El usuario ingresa un número objetivo (por ejemplo, `42`).
- El algoritmo intenta encontrar una secuencia como `6+7*4+2` que se acerque a ese número.
- Cada posible expresión está codificada como un **cromosoma**, representado por una cadena de bits.
- A través de generaciones, se aplica **selección, recombinación (crossover)** y **mutación** para evolucionar mejores soluciones.

---

## 🔁 Flujo del Algoritmo Genético

### 1. Inicialización

   Se crea una **población inicial** de `pop_size` cromosomas, donde cada cromosoma es una cadena de bits que representa **10 genes**, y cada **gen** son 4 bits (en total, 40 bits), por utlimo cada gen corresponde a un dígito (`0–9`) o a un operador (`+`, `-`, `*`, `/`).

   ```python
   def __init__(self, target, pop_size, mutation_rate, crossover_rate):
      self.target = target
      self.pop_size = pop_size
      self.mutation_rate = mutation_rate
      self.crossover_rate = crossover_rate
      self.chromosome_length = 40  # 10 genes x 4 bits
      self.population = [self.random_chromosome() for _ in range(pop_size)]
   ```

   random_chromosome() genera una cadena de 40 bits dividida en 10 genes.

### 2. Decodificacion

   Se separa el cromosoma en trozos de 4 bits.

   Cada trozo (gen) se compara en un diccionario de mapeo encoding para ver si se traduce a un dígito o operador.

   Se construye la secuencia usando la regla:

   - Alternar número y operador.

   - Si se esperan dígitos pero aparece un operador, se ignora.

   Si se esperan operadores pero aparece un dígito, se ignora.

   Se evita que la expresión termine en operador, suprimiendo el último operador si es el caso.

```python 
   def decode(self, chromosome):
    genes = [chromosome[i:i + 4] for i in range(0, len(chromosome), 4)]
    expr = []
    for g in genes:
        if g in encoding:  # encoding = { '0000': '0', '0001': '1', ... }
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

    # Evitar que termine en operador
    return ''.join(filtered[:-1]) if filtered and not expect_number else ''.join(filtered)
```

### 3 Evaluacion (Fitness)

   Se evalúa la expresión decodificada con `eval()`.

   El fitness se define como:

   $$ 
      \text{fitness} = 
      \begin{cases}
         \infty, & \text{si }(resultado = objetivo) \\
         \frac{1}{|objetivo - resultado|}, & \text{de lo contrario}
      \end{cases}
   $$

   Si la evaluación falla (por ejemplo, división entre cero), se asigna un fitness pequeño (ej. 0.0001).

   ```python
      def fitness(self, chromosome):
         expr = self.decode(chromosome)
         try:
            result = eval(expr)
            if result == self.target:
                  return float('inf')
            return 1 / abs(self.target - result)
         except:
            return 0.0001
 
   ```

### 4. Selección
   Se usa **roulet_wheel()** para elegir cromosomas, favoreciendo los más aptos. este calcula la suma de todos los fitness, para escoge un número aleatorio pick en el rango [0, total].

   Se recorre la población acumulando fitness hasta sobrepasar pick.

   El cromosoma correspondiente es elegido para reproducción.

   ```python
      def roulette_wheel(self, scored_pop):
         total = sum(score for _, score in scored_pop)
         pick = random.uniform(0, total)
         current = 0
         for chrom, score in scored_pop:
            current += score
            if current > pick:
                  return chrom
   ```
   

### 5. Crossover
   Con cierta probabilidad (`crossover_rate`), se cruzan dos padres para producir dos hijos mezclando sus genes.

   - Con probabilidad crossover_rate, se elige un punto de corte entre [1, len(parent1)-1].

   - Se intercambia todo lo que hay a la derecha de ese punto entre parent1 y parent2.

   ```python
      def crossover(self, parent1, parent2):
         if random.random() < self.crossover_rate:
            point = random.randint(1, len(parent1) - 1)
            return (
                  parent1[:point] + parent2[point:], 
                  parent2[:point] + parent1[point:]
            )
         return parent1, parent2

   ```

6. **Mutación**
   Con baja probabilidad (`mutation_rate`), se invierte aleatoriamente cada bit de un cromosoma.

   - Con probabilidad mutation_rate, se invierte cada bit.

   - Si el bit es 0, pasa a 1; si es 1, pasa a 0.

   ```python
      def mutate(self, chromosome):
         return ''.join(
            bit if random.random() > self.mutation_rate else str(1 - int(bit))
            for bit in chromosome
         )
   ```

### 7. Repetición

   Se genera una nueva población y se repite el proceso por varias generaciones o hasta hallar una solución perfecta.
   
   Se calcula fitness de cada cromosoma (paso 3).

   Se ordena la población por fitness (descendente).

   Elitismo: se lleva directo el mejor cromosoma a la siguiente generación.

   Hasta completar la nueva población:

   - Se eligen 2 padres con roulette_wheel (paso 4).

   - Se realiza crossover (paso 5).

   - Se mutan los hijos (paso 6).

   Se repite un número fijo de generaciones o hasta encontrar solución exacta ```(fitness == inf)```

   ```python
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
 
   ```

---

## 📊 Interfaz de Usuario

- Entrada del número objetivo y tamaño de población.
- Sliders para tasas de mutación y crossover.
- Botón para iniciar la evolución.
- Área de texto que muestra la mejor solución en cada generación.
"""

output_path = Path("/mnt/data/GeneticAlgorithm_GUI_Manual.md")
output_path.write_text(markdown_content.strip(), encoding="utf-8")

output_path.name
