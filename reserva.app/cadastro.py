import tkinter as tk
from tkinter import messagebox
from banco import conectar
import login

def tela_cadastro():
    def cadastrar():
        nome = entry_nome.get()
        email = entry_email.get()
        senha = entry_senha.get()

        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
            conn.commit()
            messagebox.showinfo("Sucesso", "Cadastro realizado!")
            root.destroy()
            login.tela_login()
        except:
            messagebox.showerror("Erro", "Email já cadastrado!")
        conn.close()

    root = tk.Tk()
    root.title("Cadastro")

    tk.Label(root, text="Nome").pack()
    entry_nome = tk.Entry(root)
    entry_nome.pack()

    tk.Label(root, text="Email").pack()
    entry_email = tk.Entry(root)
    entry_email.pack()

    tk.Label(root, text="Senha").pack()
    entry_senha = tk.Entry(root, show="*")
    entry_senha.pack()

    tk.Button(root, text="Cadastrar", command=cadastrar).pack()

    root.mainloop()
