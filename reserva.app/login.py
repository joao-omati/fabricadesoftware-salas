import tkinter as tk
from tkinter import messagebox
from banco import conectar
import reservas

def tela_login():
    def autenticar():
        email = entry_email.get()
        senha = entry_senha.get()
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email=? AND senha=?", (email, senha))
        user = cursor.fetchone()
        conn.close()
        if user:
            root.destroy()
            reservas.tela_reservas(user[0], user[1])
        else:
            messagebox.showerror("Erro", "Email ou senha incorretos")

    from cadastro import tela_cadastro

    root = tk.Tk()
    root.title("Login de Usuário")
    root.geometry("300x250")
    root.resizable(False, False)

    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack()

    tk.Label(frame, text="Email").pack()
    entry_email = tk.Entry(frame, width=30)
    entry_email.pack()

    tk.Label(frame, text="Senha").pack()
    entry_senha = tk.Entry(frame, show="*", width=30)
    entry_senha.pack()

    tk.Button(frame, text="Entrar", command=autenticar, bg="#4CAF50", fg="white", width=25).pack(pady=10)
    tk.Button(frame, text="Cadastrar", command=lambda: [root.destroy(), tela_cadastro()], width=25).pack()

    root.mainloop()
