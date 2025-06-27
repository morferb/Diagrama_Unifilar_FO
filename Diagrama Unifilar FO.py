import subprocess
import csv

def get_input_list(prompt):
    data = input(prompt + " (separados por coma): ").strip()
    return [item.strip() for item in data.split(",") if item.strip()]

def main():
    nombre_archivo = input("Nombre de archivo destino (ej. red.dot): ")
    nombre_csv = nombre_archivo.replace(".dot", "_tramos.csv")

    dot = []
    dot.append('digraph OLT_SPLITTER_ONT {')
    dot.append('\tfontname="Helvetica,Arial,sans-serif"')
    dot.append('\tnode [fontname="Helvetica,Arial,sans-serif"]')
    dot.append('\tedge [fontname="Helvetica,Arial,sans-serif"]')
    dot.append('\tgraph [center=1 rankdir=LR]')
    dot.append('\tedge [dir=none]')
    dot.append('\tnode [width=0.3 height=0.3 label=""]')

    # 1. Ingresar cantidad de OLT
    cantidad_olt = int(input("Cantidad de OLT: "))
    olts = [f"OLT{i+1}" for i in range(cantidad_olt)]

    # Interfaces WAN por OLT
    wan_por_olt = {}
    for i, olt in enumerate(olts, start=1):
        cant_wan = int(input(f"Cantidad de interfaces WAN para {olt}: "))
        wan_por_olt[olt] = [f"WAN_{olt}_{j+1}" for j in range(cant_wan)]

    # 2. Nivel de splitter
    nivel_splitter = int(input("Cantidad de niveles de splitter (1 o 2): "))
    
    # 3. Splitters de nivel 1 por OLT + tipo
    s1_por_olt = {}
    splitter_tipo = {}
    for olt in olts:
        splitters = get_input_list(f"Splitter nivel 1 conectados a {olt}")
        s1_por_olt[olt] = splitters
        for s in splitters:
            tipo = input(f"Tipo de splitter {s} (ej: 1:2, 1:4, etc): ")
            splitter_tipo[s] = tipo

    # 4. Splitters de nivel 2 (solo si hay nivel 2) + tipo
    s2_por_s1 = {}
    if nivel_splitter == 2:
        for olt in olts:
            for s1 in s1_por_olt[olt]:
                s2s = get_input_list(f"Splitter nivel 2 conectados a {s1}")
                s2_por_s1[s1] = s2s
                for s in s2s:
                    tipo = input(f"Tipo de splitter {s} (ej: 1:2, 1:4, etc): ")
                    splitter_tipo[s] = tipo

    # 5. ONTs por último nivel de splitter
    onts_por_splitter = {}
    if nivel_splitter == 2:
        for s1, s2s in s2_por_s1.items():
            for s2 in s2s:
                onts = get_input_list(f"ONTs conectadas a {s2}")
                onts_por_splitter[s2] = onts
    else:
        for olt in olts:
            for s1 in s1_por_olt[olt]:
                onts = get_input_list(f"ONTs conectadas a {s1}")
                onts_por_splitter[s1] = onts

    # === Entrada de distancias de fibra óptica ===
    distancias = []

    # OLT → SPLITTER NIVEL 1
    for olt in olts:
        for s1 in s1_por_olt[olt]:
            dist = input(f"Distancia OLT {olt} → Splitter {s1} (en metros): ")
            distancias.append((olt, s1, dist))

    # SPLITTER NIVEL 1 → SPLITTER NIVEL 2
    if nivel_splitter == 2:
        for s1, s2s in s2_por_s1.items():
            for s2 in s2s:
                dist = input(f"Distancia Splitter {s1} → Splitter {s2} (en metros): ")
                distancias.append((s1, s2, dist))

    # SPLITTER → ONT
    for splitter, onts in onts_por_splitter.items():
        for ont in onts:
            dist = input(f"Distancia {splitter} → ONT {ont} (en metros): ")
            distancias.append((splitter, ont, dist))

    # === Generación del DOT ===
    colors = [
        "#e6194b", "#3cb44b", "#ffe119", "#4363d8",
        "#f58231", "#911eb4", "#46f0f0", "#f032e6",
        "#bcf60c", "#fabebe", "#008080", "#e6beff"
    ]
    color_index = 0

    # OLTs + interfaces WAN
    for i, olt in enumerate(olts):
        dot.append(f'\t{olt} [shape=box label="{olt}"]')
        for j, wan in enumerate(wan_por_olt[olt]):
            ip_example = f"85.217.{i+1}.{j+1}"
            dot.append(f'\t{wan} [shape=box style=filled fillcolor="#99ccff" label="{wan}\\n{ip_example}"]')
            dot.append(f'\t{wan} -> {olt} [color="{colors[color_index % len(colors)]}"]')
            color_index += 1

    # SPLITTERS Y CONEXIONES
    for (src, dst, dist) in distancias:
        # Crear nodos si no existen aún
        if src.startswith("OLT"):
            pass  # OLT ya creado
        elif src.startswith("S") and src in splitter_tipo:
            color = "#ffff99" if nivel_splitter == 1 or src in s1_por_olt.get("OLT1", []) else "#ffd700"
            label = f"{src}\\n({splitter_tipo[src]})"
            dot.append(f'\t{src} [shape=diamond style=filled fillcolor="{color}" label="{label}"]')
        if dst.startswith("S") and dst in splitter_tipo:
            color = "#ffd700"
            label = f"{dst}\\n({splitter_tipo[dst]})"
            dot.append(f'\t{dst} [shape=diamond style=filled fillcolor="{color}" label="{label}"]')
        elif dst.startswith("ONT"):
            dot.append(f'\t{dst} [shape=circle label="{dst}"]')

        color = colors[color_index % len(colors)]
        dot.append(f'\t{src} -> {dst} [color="{color}" label="{dist} m"]')
        color_index += 1

    dot.append("}")

    # Guardar .dot
    with open(nombre_archivo, "w") as f:
        f.write("\n".join(dot))
    print(f"\n✅ Archivo '{nombre_archivo}' generado correctamente.")

    # Guardar .csv
    with open(nombre_csv, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Origen", "Destino", "Distancia (m)"])
        writer.writerows(distancias)
    print(f"📄 Archivo CSV '{nombre_csv}' generado correctamente.")

    # Elegir formato de salida
    print("\nSeleccioná el formato de imagen:")
    print("1. PNG")
    print("2. SVG")
    print("3. PDF")
    opcion = input("Opción (1/2/3): ").strip()

    formato = "png"
    if opcion == "2":
        formato = "svg"
    elif opcion == "3":
        formato = "pdf"

    salida = nombre_archivo.replace(".dot", f".{formato}")

    try:
        subprocess.run(["dot", f"-T{formato}", nombre_archivo, "-o", salida], check=True)
        print(f"🖼️ Imagen '{salida}' generada con éxito.")
    except FileNotFoundError:
        print("⚠️ Error: El comando 'dot' no está disponible. Instalá Graphviz.")
    except subprocess.CalledProcessError:
        print("❌ Error al generar el archivo con Graphviz.")

if __name__ == "__main__":
    main()

