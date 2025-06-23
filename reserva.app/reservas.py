import tkinter as tk
from tkinter import messagebox, ttk
from banco import conectar

SALAS_DISPONIVEIS = ["Sala 101", "Sala 102", "Laboratório 1", "Laboratório 2", "Auditório"]

def tela_reservas(user_id, nome):
    def reservar(nova=True):
        sala = combo_sala.get()
        data = entry_data.get()
        inicio = entry_inicio.get()
        fim = entry_fim.get()

        if not sala or not data or not inicio or not fim:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        conn = conectar()
        cursor = conn.cursor()

        if nova:
            cursor.execute("""
                SELECT * FROM reservas WHERE sala=? AND data=? 
                AND hora_inicio < ? AND hora_fim > ?""",
                (sala, data, fim, inicio))
            conflito = cursor.fetchone()
            if conflito:
                messagebox.showerror("Erro", "Já existe uma reserva nesse horário!")
                conn.close()
                return
            cursor.execute("""
                INSERT INTO reservas (usuario_id, sala, data, hora_inicio, hora_fim)
                VALUES (?, ?, ?, ?, ?)""", (user_id, sala, data, inicio, fim))
        else:
            cursor.execute("""
                UPDATE reservas SET sala=?, data=?, hora_inicio=?, hora_fim=?
                WHERE id=? AND usuario_id=?
            """, (sala, data, inicio, fim, reserva_id_editar, user_id))

        conn.commit()
        conn.close()
        limpar_formulario()
        atualizar_reservas()
        messagebox.showinfo("Sucesso", "Reserva salva com sucesso!")

    def selecionar_reserva(event):
        item = lista_reservas.selection()
        if not item:
            return
        valores = lista_reservas.item(item, "values")
        entry_data.delete(0, tk.END)
        entry_inicio.delete(0, tk.END)
        entry_fim.delete(0, tk.END)
        combo_sala.set(valores[1])
        entry_data.insert(0, valores[2])
        entry_inicio.insert(0, valores[3])
        entry_fim.insert(0, valores[4])
        global reserva_id_editar
        reserva_id_editar = valores[0]
        btn_salvar.config(command=lambda: reservar(False))

    def excluir():
        item = lista_reservas.selection()
        if not item:
            messagebox.showwarning("Selecione", "Selecione uma reserva para excluir.")
            return
        valores = lista_reservas.item(item, "values")
        reserva_id = valores[0]
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reservas WHERE id=? AND usuario_id=?", (reserva_id, user_id))
        conn.commit()
        conn.close()
        atualizar_reservas()
        limpar_formulario()
        messagebox.showinfo("Sucesso", "Reserva excluída.")

    def filtrar():
        filtro = combo_filtro.get()
        valor = entry_filtro.get()
        for i in lista_reservas.get_children():
            lista_reservas.delete(i)
        conn = conectar()
        cursor = conn.cursor()
        if filtro == "Data":
            cursor.execute("SELECT id, sala, data, hora_inicio, hora_fim FROM reservas WHERE usuario_id=? AND data=?", (user_id, valor))
        elif filtro == "Sala":
            cursor.execute("SELECT id, sala, data, hora_inicio, hora_fim FROM reservas WHERE usuario_id=? AND sala=?", (user_id, valor))
        else:
            atualizar_reservas()
            return
        for row in cursor.fetchall():
            lista_reservas.insert('', 'end', values=row)
        conn.close()

    def atualizar_reservas():
        for item in lista_reservas.get_children():
            lista_reservas.delete(item)
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, sala, data, hora_inicio, hora_fim FROM reservas WHERE usuario_id=?", (user_id,))
        for row in cursor.fetchall():
            lista_reservas.insert('', 'end', values=row)
        conn.close()

    def limpar_formulario():
        combo_sala.set("")
        entry_data.delete(0, tk.END)
        entry_inicio.delete(0, tk.END)
        entry_fim.delete(0, tk.END)
        btn_salvar.config(command=lambda: reservar(True))

    root = tk.Tk()
    root.title(f"Painel de Reservas - {nome}")
    root.geometry("750x500")

    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack()

    tk.Label(frame, text="Sala/Laboratório:").grid(row=0, column=0)
    combo_sala = ttk.Combobox(frame, values=SALAS_DISPONIVEIS, width=25, state="readonly")
    combo_sala.grid(row=0, column=1)

    tk.Label(frame, text="Data (YYYY-MM-DD):").grid(row=1, column=0)
    entry_data = tk.Entry(frame, width=28)
    entry_data.grid(row=1, column=1)

    tk.Label(frame, text="Início (HH:MM):").grid(row=2, column=0)
    entry_inicio = tk.Entry(frame, width=28)
    entry_inicio.grid(row=2, column=1)

    tk.Label(frame, text="Fim (HH:MM):").grid(row=3, column=0)
    entry_fim = tk.Entry(frame, width=28)
    entry_fim.grid(row=3, column=1)

    btn_salvar = tk.Button(frame, text="Salvar Reserva", bg="#4CAF50", fg="white", command=lambda: reservar(True))
    btn_salvar.grid(row=4, column=0, columnspan=2, pady=10)

    ttk.Separator(frame, orient="horizontal").grid(row=5, column=0, columnspan=2, sticky="ew", pady=10)

    tk.Label(frame, text="Filtrar por:").grid(row=6, column=0)
    combo_filtro = ttk.Combobox(frame, values=["Data", "Sala"], state="readonly", width=10)
    combo_filtro.grid(row=6, column=1, sticky='w')
    entry_filtro = tk.Entry(frame, width=15)
    entry_filtro.grid(row=6, column=1, padx=(80,0), sticky='w')
    tk.Button(frame, text="Filtrar", command=filtrar).grid(row=6, column=1, padx=(200,0), sticky='w')

    lista_reservas = ttk.Treeview(frame, columns=("ID", "Sala", "Data", "Início", "Fim"), show="headings", height=8)
    for col in ("ID", "Sala", "Data", "Início", "Fim"):
        lista_reservas.heading(col, text=col)
        lista_reservas.column(col, width=100)
    lista_reservas.grid(row=7, column=0, columnspan=2, pady=10)
    lista_reservas.bind("<<TreeviewSelect>>", selecionar_reserva)

    tk.Button(frame, text="Excluir Selecionada", bg="#d9534f", fg="white", command=excluir).grid(row=8, column=0, columnspan=2, pady=5)

    atualizar_reservas()
    root.mainloop()
