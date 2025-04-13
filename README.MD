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

1. **Inicialización**
   - Se crea una **población inicial** de cromosomas aleatorios.
   - Cada cromosoma representa una cadena binaria compuesta por varios **genes** de 4 bits cada uno (suficiente para codificar números y operadores).

2. **Decodificación**
   - Cada cromosoma se traduce en una cadena legible de números y operadores.
   - Se eliminan secuencias inválidas (por ejemplo, operadores consecutivos).

3. **Evaluación (Fitness)**
   - Se evalúa la expresión usando `eval()`.
   - El fitness se calcula como `1 / |objetivo - resultado|`, con un valor especial de `infinito` si el resultado es exacto.

4. **Selección**
   - Se usa **ruleta** (roulette wheel selection) para elegir cromosomas, favoreciendo los más aptos.

5. **Crossover**
   - Con cierta probabilidad (`crossover_rate`), se cruzan dos padres para producir dos hijos mezclando sus genes.

6. **Mutación**
   - Con baja probabilidad (`mutation_rate`), se invierte aleatoriamente cada bit de un cromosoma.

7. **Repetición**
   - Se genera una nueva población y se repite el proceso por varias generaciones o hasta hallar una solución perfecta.

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
