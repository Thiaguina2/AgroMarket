
import tkinter as tk
from tkinter import messagebox
import json
import os

# ARQUIVO DE DADOS
ARQUIVO = "produtos.json"

produtos = []
produtos_exibidos = []
indice_edicao = None


# CARREGAR PRODUTOS
def carregar_produtos():
    global produtos

    if os.path.exists(ARQUIVO):
        try:
            with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
                produtos = json.load(arquivo)
        except (json.JSONDecodeError, OSError):
            produtos = []


# SALVAR PRODUTOS
def salvar_produtos():
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(produtos, arquivo, ensure_ascii=False, indent=4)


# JANELA PRINCIPAL
janela = tk.Tk()
janela.title("AgroMarket")
janela.geometry("850x680")
janela.configure(bg="#f4f7f2")

# CORES
VERDE = "#2e7d32"
VERDE_CLARO = "#e8f5e9"
FUNDO = "#f4f7f2"
BRANCO = "#ffffff"
CINZA = "#555555"


# CABEÇALHO
cabecalho = tk.Frame(janela, bg=VERDE, height=90)
cabecalho.pack(fill="x")

tk.Label(
    cabecalho,
    text="AgroMarket",
    font=("Arial", 25, "bold"),
    bg=VERDE,
    fg=BRANCO
).pack(pady=(15, 0))

tk.Label(
    cabecalho,
    text="Sistema de gerenciamento agropecuário",
    font=("Arial", 10),
    bg=VERDE,
    fg=BRANCO
).pack()


# CARTÕES DE INFORMAÇÕES
painel = tk.Frame(janela, bg=FUNDO)
painel.pack(fill="x", padx=25, pady=15)

cartao1 = tk.Frame(painel, bg=BRANCO, padx=20, pady=12)
cartao1.pack(side="left", fill="both", expand=True, padx=5)

tk.Label(
    cartao1,
    text="Produtos cadastrados",
    bg=BRANCO,
    fg=CINZA
).pack()

total_produtos = tk.Label(
    cartao1,
    text="0",
    font=("Arial", 22, "bold"),
    bg=BRANCO,
    fg=VERDE
)
total_produtos.pack()

cartao2 = tk.Frame(painel, bg=BRANCO, padx=20, pady=12)
cartao2.pack(side="left", fill="both", expand=True, padx=5)

tk.Label(
    cartao2,
    text="Categorias",
    bg=BRANCO,
    fg=CINZA
).pack()

total_categorias = tk.Label(
    cartao2,
    text="0",
    font=("Arial", 22, "bold"),
    bg=BRANCO,
    fg=VERDE
)
total_categorias.pack()


# FORMULÁRIO
formulario = tk.Frame(janela, bg=BRANCO, padx=20, pady=15)
formulario.pack(fill="x", padx=30, pady=5)

tk.Label(
    formulario,
    text="Cadastro de produtos",
    font=("Arial", 15, "bold"),
    bg=BRANCO,
    fg=VERDE
).grid(row=0, column=0, columnspan=2, sticky="w", pady=10)

tk.Label(
    formulario,
    text="Nome do produto:",
    bg=BRANCO
).grid(row=1, column=0, sticky="w", pady=5)

nome = tk.Entry(formulario, width=35)
nome.grid(row=1, column=1, pady=5)

tk.Label(
    formulario,
    text="Categoria:",
    bg=BRANCO
).grid(row=2, column=0, sticky="w", pady=5)

categoria = tk.Entry(formulario, width=35)
categoria.grid(row=2, column=1, pady=5)

tk.Label(
    formulario,
    text="Preço:",
    bg=BRANCO
).grid(row=3, column=0, sticky="w", pady=5)

preco = tk.Entry(formulario, width=35)
preco.grid(row=3, column=1, pady=5)


# LIMPAR CAMPOS
def limpar_campos():
    global indice_edicao

    nome.delete(0, tk.END)
    categoria.delete(0, tk.END)
    preco.delete(0, tk.END)

    indice_edicao = None


# ATUALIZAR INFORMAÇÕES
def atualizar_painel():
    total_produtos.config(text=str(len(produtos)))

    categorias_unicas = set(
        produto["categoria"].lower()
        for produto in produtos
    )

    total_categorias.config(text=str(len(categorias_unicas)))


# ATUALIZAR LISTA
def atualizar_lista():
    global produtos_exibidos

    lista.delete(0, tk.END)
    produtos_exibidos = []

    pesquisa = campo_busca.get().lower()

    for i, produto in enumerate(produtos):
        if (
            pesquisa in produto["nome"].lower()
            or pesquisa in produto["categoria"].lower()
        ):
            texto = (
                f"{produto['nome']} | "
                f"{produto['categoria']} | "
                f"R$ {produto['preco']:.2f}"
            )

            lista.insert(tk.END, texto)
            produtos_exibidos.append(i)

    atualizar_painel()


# CADASTRAR
def cadastrar():
    n = nome.get().strip()
    c = categoria.get().strip()
    p = preco.get().strip()

    if not n or not c or not p:
        messagebox.showwarning("Aviso", "Preencha todos os campos!")
        return

    try:
        valor = float(p.replace(",", "."))

        if valor <= 0:
            raise ValueError

    except ValueError:
        messagebox.showerror("Erro", "Digite um preço válido!")
        return

    produtos.append({
        "nome": n,
        "categoria": c,
        "preco": valor
    })

    salvar_produtos()
    limpar_campos()
    atualizar_lista()

    messagebox.showinfo("Sucesso", "Produto cadastrado!")


# PESQUISAR
def pesquisar():
    atualizar_lista()


def mostrar_todos():
    campo_busca.delete(0, tk.END)
    atualizar_lista()


# SELECIONAR PRODUTO
def obter_selecionado():
    selecionado = lista.curselection()

    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um produto!")
        return None

    return produtos_exibidos[selecionado[0]]


# EDITAR
def editar():
    global indice_edicao

    indice = obter_selecionado()

    if indice is None:
        return

    indice_edicao = indice
    produto = produtos[indice]

    limpar_campos()
    indice_edicao = indice

    nome.insert(0, produto["nome"])
    categoria.insert(0, produto["categoria"])
    preco.insert(0, str(produto["preco"]))


# SALVAR EDIÇÃO
def salvar_edicao():
    global indice_edicao

    if indice_edicao is None:
        messagebox.showwarning("Aviso", "Selecione um produto para editar!")
        return

    n = nome.get().strip()
    c = categoria.get().strip()
    p = preco.get().strip()

    if not n or not c or not p:
        messagebox.showwarning("Aviso", "Preencha todos os campos!")
        return

    try:
        valor = float(p.replace(",", "."))

        if valor <= 0:
            raise ValueError

    except ValueError:
        messagebox.showerror("Erro", "Digite um preço válido!")
        return

    produtos[indice_edicao] = {
        "nome": n,
        "categoria": c,
        "preco": valor
    }

    salvar_produtos()
    limpar_campos()
    atualizar_lista()

    messagebox.showinfo("Sucesso", "Produto atualizado!")


# EXCLUIR
def excluir():
    indice = obter_selecionado()

    if indice is None:
        return

    resposta = messagebox.askyesno(
        "Confirmar",
        "Deseja excluir este produto?"
    )

    if resposta:
        produtos.pop(indice)
        salvar_produtos()
        limpar_campos()
        atualizar_lista()


# DETALHES
def detalhes():
    indice = obter_selecionado()

    if indice is None:
        return

    produto = produtos[indice]

    mensagem = (
        f"Nome: {produto['nome']}\n\n"
        f"Categoria: {produto['categoria']}\n\n"
        f"Preço: R$ {produto['preco']:.2f}"
    )

    messagebox.showinfo("Detalhes", mensagem)


# ÁREA DE PESQUISA
area_busca = tk.Frame(janela, bg=FUNDO)
area_busca.pack(fill="x", padx=30, pady=15)

tk.Label(
    area_busca,
    text="Pesquisar:",
    bg=FUNDO
).pack(side="left", padx=5)

campo_busca = tk.Entry(area_busca, width=35)
campo_busca.pack(side="left", padx=5)

tk.Button(
    area_busca,
    text="Buscar",
    command=pesquisar,
    bg=VERDE,
    fg=BRANCO
).pack(side="left", padx=5)

tk.Button(
    area_busca,
    text="Mostrar todos",
    command=mostrar_todos
).pack(side="left", padx=5)


# LISTA DE PRODUTOS
tk.Label(
    janela,
    text="Lista de produtos",
    font=("Arial", 15, "bold"),
    bg=FUNDO,
    fg=VERDE
).pack(anchor="w", padx=35)

lista = tk.Listbox(
    janela,
    width=90,
    height=9,
    font=("Arial", 10),
    bg=BRANCO,
    fg=CINZA,
    selectbackground=VERDE,
    relief="flat"
)
lista.pack(fill="x", padx=30, pady=10)


# BOTÕES DE AÇÃO
botoes = tk.Frame(janela, bg=FUNDO)
botoes.pack(pady=10)

tk.Button(
    botoes,
    text="Cadastrar",
    command=cadastrar,
    bg=VERDE,
    fg=BRANCO,
    width=14
).pack(side="left", padx=5)

tk.Button(
    botoes,
    text="Salvar edição",
    command=salvar_edicao,
    bg="#1976d2",
    fg=BRANCO,
    width=14
).pack(side="left", padx=5)

tk.Button(
    botoes,
    text="Editar",
    command=editar,
    width=12
).pack(side="left", padx=5)

tk.Button(
    botoes,
    text="Detalhes",
    command=detalhes,
    width=12
).pack(side="left", padx=5)

tk.Button(
    botoes,
    text="Excluir",
    command=excluir,
    bg="#c62828",
    fg=BRANCO,
    width=12
).pack(side="left", padx=5)


# INICIAR SISTEMA
carregar_produtos()
atualizar_lista()

janela.mainloop()