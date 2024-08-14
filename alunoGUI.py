import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from Aluno import Aluno

class AlunoGUI(tk.Tk):
    def __init__(self):
        # Inicialização da janela
        tk.Tk.__init__(self)
        self.title('Cadastro de Alunos')
        self.geometry('400x400')
        self.aluno = Aluno()
        self.create_widgets()

    # Método para criar os widgets
    def create_widgets(self):
        # Criação dos widgets
        self.lb_id = tk.Label(self, text='ID: ')
        self.lb_id.pack()
        self.et_id = tk.Entry(self)
        self.et_id.pack()

        self.lb_nome = tk.Label(self, text='Nome:')
        self.lb_nome.pack()
        self.et_nome = tk.Entry(self)
        self.et_nome.pack()

        self.lb_nota1 = tk.Label(self, text='Nota 1:')
        self.lb_nota1.pack()
        self.et_nota1 = tk.Entry(self)
        self.et_nota1.pack()

        self.lb_nota2 = tk.Label(self, text='Nota 2:')
        self.lb_nota2.pack()
        self.et_nota2 = tk.Entry(self)
        self.et_nota2.pack()

        frame = tk.Frame(self, borderwidth=2, pady=5)
        frame.pack()

        # Criação dos botões
        self.bt_cadastrar = tk.Button(frame, text='Cadastrar', command=self.cadastrar, borderwidth=2, padx=10)
        self.bt_cadastrar.pack(side='left')

        self.bt_deletar = tk.Button(frame, text='Deletar', command=self.deletar, borderwidth=2, padx=10)
        self.bt_deletar.pack(side='left')

        self.bt_alterar = tk.Button(frame, text='Alterar', command=self.alterar, borderwidth=2, padx=10)
        self.bt_alterar.pack(side='left')

        self.bt_limpar = tk.Button(frame, text='Limpar', command=self.limpar, borderwidth=2, padx=10)
        self.bt_limpar.pack(side='left')

        # Criação da Treeview
        self.view = ttk.Treeview(columns=('#0', 'Nome', 'Nota 1', 'Nota 2', 'Média', 'Aprovado'))

        # Criação da barra de rolagem
        self.viewscrollbar = ttk.Scrollbar(self, orient='vertical', command=self.view.yview)
        self.viewscrollbar.pack(side='right', fill='y', anchor='e')

        # Configuração da Treeview
        self.view.configure(yscrollcommand=self.viewscrollbar.set)
        self.view.heading('#0', text='ID')
        self.view.column('#0', width=50)
        self.view.heading('#1', text='Nome')
        self.view.column('#1', width=110)
        self.view.heading('#2', text='Nota 1')
        self.view.column('#2', width=50)
        self.view.heading('#3', text='Nota 2')
        self.view.column('#3', width=50)
        self.view.heading('#4', text='Média')
        self.view.column('#4', width=50)
        self.view.heading('#5', text='Aprovado')
        self.view.column('#5', width=60)
        self.view.pack()

        # Evento de seleção
        self.view.bind("<<TreeviewSelect>>", self.on_select)

        self.consultar()

    # Método para limpar os campos
    def limpar(self):
        try:
            self.et_id.delete(0, 'end')
            self.et_nome.delete(0, 'end')
            self.et_nota1.delete(0, 'end')
            self.et_nota2.delete(0, 'end')
        except:
            pass

    # Método para selecionar um item da Treeview
    def on_select(self, event):
        try:
            item = self.view.selection()[0]
            self.et_id.delete(0, 'end')
            self.et_id.insert(0, self.view.item(item, 'text'))
            self.et_nome.delete(0, 'end')
            self.et_nome.insert(0, self.view.item(item, 'values')[0])
            self.et_nota1.delete(0, 'end')
            self.et_nota1.insert(0, self.view.item(item, 'values')[1])
            self.et_nota2.delete(0, 'end')
            self.et_nota2.insert(0, self.view.item(item, 'values')[2])
        except:
            pass

    # Método para cadastrar um aluno
    def cadastrar(self):
        try:
            nome = self.et_nome.get()
            nota1 = float(self.et_nota1.get())
            nota2 = float(self.et_nota2.get())
            self.aluno.cadastrar(nome, nota1, nota2)
            messagebox.showinfo('Cadastro', 'Aluno cadastrado com sucesso!')
            self.consultar()
        except:
            messagebox.showerror('Erro', 'Preencha os campos')

    # Método para deletar um aluno
    def deletar(self):
        id = int(self.et_id.get())
        try:
            result = messagebox.askquestion('Atenção', 'Deseja realmente excluir o aluno?', type='yesno')
            if result == 'yes':
                self.aluno.excluir(id)
                messagebox.showinfo('Exclusão', 'Aluno excluído com sucesso!')
                self.consultar()
            else:
                messagebox.showinfo('Exclusão', 'Exclusão cancelada!')
                self.consultar()
                
        except:
            messagebox.showerror('Erro', 'Selecione um aluno')

    # Método para alterar os dados de um aluno
    def alterar(self):
        try:
            id = int(self.et_id.get())
            nome = self.et_nome.get()
            nota1 = float(self.et_nota1.get())
            nota2 = float(self.et_nota2.get())
            self.aluno.alterar(id, nome, nota1, nota2)
            messagebox.showinfo('Alteração', 'Aluno alterado com sucesso!')
            self.consultar()
        except:
            messagebox.showerror('Erro', 'Selecione um aluno')
    
    # Método para consultar os alunos cadastrados
    def consultar(self):
        try:
            self.view.delete(*self.view.get_children())
            consulta = Aluno().consultar()
            for i in consulta:
                self.view.insert('', 'end', text=i[0], values=(i[1], i[2], i[3], i[4], 'Sim' if i[5] else 'Não'))
        except:
            pass

# Execução da aplicação
if __name__ == '__main__':
    AlunoGUI().mainloop()
