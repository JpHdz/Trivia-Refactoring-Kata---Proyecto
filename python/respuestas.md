# Visión General del Taller

**Pregunta guía:** ¿Puedes dejar el código en un estado del que te sientas orgulloso, sin que el GameTest se ponga en rojo ni una sola vez?

> 70% seguro de que sí

---

## Bloque 0: Preparación del entorno

### Paso 0.3 — Jugar una partida manualmente

**¿Qué tipos de mensajes aparecen en consola?**

Aparecen mensajes de bienvenida, petición de número de jugadores, de turno del jugador actual, resultado del dado, nueva posición, categoría de la pregunta, la pregunta en sí, y el resultado.

**¿Qué secuencia tiene un turno de juego?**

1. Tirar el dado.
2. Se mueve al jugador o se intenta sacarlo de la penalización.
3. Se anuncia la categoría y se lee una pregunta.
4. Se pide indicar si la respuesta fue correcta o no.
5. Se evalúa: si es correcta se da una moneda (y se verifica si ganó); si es incorrecta se manda a la penalización.
6. Pasa el turno al siguiente jugador.

**¿Cuándo termina la partida?**

Cuando un jugador responde correctamente y, al sumar su moneda, alcanza las 6 monedas. En ese momento `did_player_win` retorna `False`, lo que rompe el ciclo.

---

## Bloque 1: Exploración y análisis — leer antes de cambiar

### Paso 1.1 — Lectura activa de `Game.java` (Ficha de análisis)

**Olores de código detectados:**

- **Método demasiado largo:** `roll()` tiene alrededor de 27 líneas y `handle_correct_answer()` tiene alrededor de 29 líneas.

- **Nombres engañosos o que no revelan la intención:** `did_player_win()` retorna `False` si el jugador gana. `places` y `purses` no son tan claros como `positions` o `coins`.

- **Duplicación de código:** El bloque para mover al jugador en el tablero y reiniciar su posición si pasa de 12. También el bloque para pasar al siguiente jugador y reiniciar el índice a 0.

- **Números mágicos sin nombre:** `6` (monedas para ganar y tamaño máximo de jugadores), `12` (casillas del tablero), `50` (número de preguntas iniciales por categoría).

- **Mezcla de responsabilidades:** La clase `Game` maneja el estado de los jugadores, la creación y gestión del mazo de preguntas, la lógica del flujo del turno y las impresiones en consola.

**El typo y el bug:**

- **Error ortográfico encontrado:** No.
- **Lógica incorrecta encontrada:** Sí. `did_player_win()` evalúa si el jugador _no_ ganó para seguir jugando, contradiciendo el nombre.

---

## Bloque 2: Refactorización iterativa — el ciclo de vida del kata

### Micro-paso J2 — Extraer números mágicos como constantes

**Al analizar `if (purses[currentPlayer] == 6)`, ¿qué significa `6`?**

El número `6` representa la cantidad de monedas necesarias para ganar la partida.

---

## Bloque 3: Bugs, typo y limpieza final

### Paso 3.2 — La caza del bug

**¿Las posiciones 0–11 cubren las 4 categorías correctamente?**

No completamente. El método de asignación de categorías usa condiciones específicas para posiciones de forma muy literal. Aunque cubre las 4 categorías, la lógica es poco flexible y propensa a errores si se agregan más categorías o cambia el tamaño del tablero.

### Paso 3.3 — Relectura final: la prueba del orgullo

- **¿Algún método tiene más de 10 líneas y podría partirse?** Sí. Métodos como `handle_correct_answer` y `roll` originalmente tenían más de 10 líneas. En los commits de refactorización, estos métodos fueron divididos y simplificados.
- **¿Alguna variable se llama `i`, `j`, `x` o algo igualmente poco descriptivo?** No. Después de la refactorización, los nombres de variables son descriptivos.
- **¿Hay algún comentario que explica lo que el código ya debería decir por sí solo?** No. Tras la refactorización, los métodos y variables tienen nombres claros y no requieren comentarios explicativos.
- **¿Hay alguna condición booleana compleja que podría extraerse como método con nombre de intención?** Sí. La condición de victoria y la lógica de salida de la penalización fueron extraídas como métodos `did_player_win` y `_handle_penalty_box_turn`, mejorando la legibilidad.

---

## Bloque 4: Retrospectiva y opcional

### Paso 4.1 — Retrospectiva

**Sobre la técnica del Golden Master:**

- **¿En qué momento te sentiste seguro de que el Golden Master cubría lo suficiente?** Cuando, pasando los pasos, el test seguía en verde.
- **¿Hubo algún cambio que el Golden Master no pudo detectar como peligroso?** Sí. El bug relacionado con la condición de victoria o la lógica de penalización. Si el bug está presente en ambas versiones, no lo detecta porque compara dos comportamientos igualmente incorrectos.
- **¿Por qué crees que el README dice que no debemos escribir tests unitarios durante la refactorización? ¿Estás de acuerdo?** Porque el Golden Master ya actúa como red de seguridad, asegurando que el comportamiento externo no cambie. Sí, estoy de acuerdo con esta práctica.

**Sobre la refactorización:**

- **¿Qué olor de código fue el más difícil de eliminar? ¿Por qué?** El separar responsabilidades pues tuve varios bugsillos.
- **¿Cuántas veces se puso en rojo el test? ¿Qué lo causó?** No las conté, pero fueron varias veces. Fueron más errores que no me leí bien y me despistaba.
- **¿Qué refactorización manual (no automática del IDE) fue la más arriesgada?** La migración de la lógica de preguntas a la clase `QuestionDeck`, porque requería muchas líneas de código.
- **¿Cómo podría mejorarse el diseño para que el próximo cambio de requisito sea más fácil?** Manteniendo las responsabilidades bien separadas, usando constantes para valores mágicos y evitando duplicación.
