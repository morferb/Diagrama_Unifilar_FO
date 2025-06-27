# Diagrama_Unifilar_FO

### 🧵 ¿Qué es un Diagrama Unifilar de FO?

En fibra óptica, un **diagrama unifilar** muestra conexiones **punto a punto** o **punto a multipunto** (ej. OLT → splitter → ONT), incluyendo puertos, fibras, y elementos de distribución, pero representado de forma **simplificada en una sola línea de conexión por fibra o trayecto**.

### Instalá Graphviz en tu sistema (Linux, Windows, Mac):

```bash
sudo apt install graphviz
```


# 🕸️ Generador de Topología OLT-Splitter-ONT

Este script en Python genera un archivo `.dot` con la topología de una red óptica pasiva (PON) incluyendo OLTs, interfaces WAN, splitters de nivel 1 y 2, ONTs, y sus distancias. También exporta un archivo `.csv` con los tramos de fibra óptica y permite generar una imagen de la topología usando Graphviz.

---

## ⚙️ Lógica del Programa

1. Solicita datos de entrada: cantidad de OLTs, interfaces WAN, splitters, ONTs y distancias de fibra óptica.
2. Genera un archivo `.dot` para representar gráficamente la topología.
3. Exporta un archivo `.csv` con las distancias entre cada elemento.
4. Usa Graphviz para convertir el `.dot` en una imagen (`.png`, `.svg` o `.pdf`).

---

## 📥 Input Esperado

Durante la ejecución interactiva, se solicitan los siguientes datos:

- Nombre del archivo de salida (`.dot`)
- Cantidad de OLTs
- Cantidad de interfaces WAN por OLT
- Cantidad de niveles de splitter (1 o 2)
- Splitters conectados a cada OLT y su tipo (ej: 1:4)
- Si hay nivel 2: splitters conectados a otros splitters y su tipo
- ONTs conectadas al último nivel de splitter
- Distancia entre cada tramo de la red en metros

---

## 📤 Output

- Archivo `.dot` con la topología de red.
- Archivo `.csv` con los tramos: origen, destino, distancia.
- Imagen en formato `.png`, `.svg` o `.pdf`.

---

## 🧪 Ejemplo de Uso

```bash
$ python3 generar_topologia.py
Nombre de archivo destino (ej. red.dot): red.dot
Cantidad de OLT: 1
Cantidad de interfaces WAN para OLT1: 2
Cantidad de niveles de splitter (1 o 2): 2
Splitter nivel 1 conectados a OLT1 (separados por coma): S1, S2
Tipo de splitter S1 (ej: 1:2, 1:4, etc): 1:4
Tipo de splitter S2 (ej: 1:2, 1:4, etc): 1:2
Splitter nivel 2 conectados a S1 (separados por coma): S1A, S1B
Tipo de splitter S1A (ej: 1:2, 1:4, etc): 1:4
Tipo de splitter S1B (ej: 1:2, 1:4, etc): 1:4
ONTs conectadas a S1A (separados por coma): ONT1, ONT2
ONTs conectadas a S1B (separados por coma): ONT3
ONTs conectadas a S2 (separados por coma): ONT4
Distancia OLT OLT1 → Splitter S1 (en metros): 120
Distancia OLT OLT1 → Splitter S2 (en metros): 80
Distancia Splitter S1 → Splitter S1A (en metros): 40
Distancia Splitter S1 → Splitter S1B (en metros): 30
Distancia S1A → ONT ONT1 (en metros): 5
Distancia S1A → ONT ONT2 (en metros): 5
Distancia S1B → ONT ONT3 (en metros): 10
Distancia S2 → ONT ONT4 (en metros): 15

Seleccioná el formato de imagen:
1. PNG
2. SVG
3. PDF
Opción (1/2/3): 1
✅ Archivo 'red.dot' generado correctamente.
📄 Archivo CSV 'red_tramos.csv' generado correctamente.
🖼️ Imagen 'red.png' generada con éxito.
```
Morferb
