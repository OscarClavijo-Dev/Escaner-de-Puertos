import socket
import tkinter as tk
from tkinter import ttk
from concurrent.futures import ThreadPoolExecutor

# -------------------------
# FUNCIÓN: escanear un puerto
# -------------------------
def escanear_puerto(ip, puerto):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)  # timeout pequeño = rápido
        resultado = sock.connect_ex((ip, puerto))
        sock.close()

        if resultado == 0:
            return puerto
    except:
        pass

    return None


# -------------------------
# FUNCIÓN: iniciar escaneo
# -------------------------
def iniciar_escaneo():
    ip = entrada_ip.get()
    salida.delete(1.0, tk.END)

    puertos = range(1, 1025)  # puertos básicos (principiante)
    total = len(puertos)
    progreso["maximum"] = total
    progreso["value"] = 0

    salida.insert(tk.END, f"Escaneando {ip}...\n\n")

    abiertos = []

    with ThreadPoolExecutor(max_workers=100) as executor:
        for puerto in puertos:
            resultado = executor.submit(escanear_puerto, ip, puerto)

            # actualizar progreso
            progreso["value"] += 1
            ventana.update_idletasks()

            if resultado.result():
                abiertos.append(resultado.result())

    if abiertos:
        for p in abiertos:
            salida.insert(tk.END, f"[+] Puerto abierto: {p}\n")
    else:
        salida.insert(tk.END, "No se encontraron puertos abiertos\n")


# -------------------------
# INTERFAZ GRÁFICA
# -------------------------
ventana = tk.Tk()
ventana.title("Port Scanner - Principiante")
ventana.geometry("400x350")

tk.Label(ventana, text="Dirección IP:").pack(pady=5)

entrada_ip = tk.Entry(ventana)
entrada_ip.pack()

tk.Button(ventana, text="Escanear", command=iniciar_escaneo).pack(pady=10)

progreso = ttk.Progressbar(ventana)
progreso.pack(fill="x", padx=20, pady=5)

salida = tk.Text(ventana, height=10)
salida.pack(fill="both", padx=10, pady=10)

ventana.mainloop()
