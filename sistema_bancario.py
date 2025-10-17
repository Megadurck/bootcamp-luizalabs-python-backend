# -----------------------------
# Lista de usuários e contador de contas
# -----------------------------
usuarios = []
numero_conta = 1
AGENCIA_FIXA = "25"  # Número fixo da agência do banco

# -----------------------------
# Funções do sistema
# -----------------------------
def exibir_menu():
    menu = """
[u] Criar usuário
[c] Cadastrar conta
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """
    return input(menu).strip().lower()

def criar_usuario():
    """Cria um usuário e adiciona à lista de usuários."""
    nome = input("Informe o nome do usuário: ").strip()
    cpf = input("Informe o CPF (somente números): ").strip()
    nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ").strip()

    # Verificar se CPF já existe
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            print("Erro: CPF já cadastrado!")
            return None

    usuario = {
        "nome": nome,
        "cpf": cpf,
        "nascimento": nascimento,
        "contas": []  # Lista de contas vinculadas
    }

    usuarios.append(usuario)
    print(f"Usuário {nome} criado com sucesso!")
    return usuario

def buscar_usuario_por_cpf(cpf):
    """Retorna o usuário correspondente ao CPF ou None se não existir."""
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None

def cadastrar_conta(usuario):
    """Cria uma conta bancária vinculada ao usuário com número no formato '0001' e agência fixa."""
    global numero_conta

    tipo = input("Informe o tipo de conta [corrente/poupança]: ").strip().lower()
    if tipo not in ["corrente", "poupança"]:
        print("Tipo de conta inválido! Use 'corrente' ou 'poupança'.")
        return None

    # Formata o número da conta com 4 dígitos
    conta_numero = str(numero_conta).zfill(4)

    conta = {
        "agencia": AGENCIA_FIXA,
        "numero": conta_numero,
        "tipo": tipo,
        "saldo": 0,
        "limite": 500,
        "extrato": "",
        "numero_saques": 0
    }

    usuario["contas"].append(conta)
    print(f"Conta {tipo} agência {AGENCIA_FIXA} número {conta_numero} criada para {usuario['nome']} com sucesso!")

    numero_conta += 1
    return conta

def depositar(saldo, extrato):
    valor = float(input("Informe o valor do depósito: "))
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato

def sacar(saldo, extrato, numero_saques, limite, LIMITE_SAQUES):
    valor = float(input("Informe o valor do saque: "))

    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= LIMITE_SAQUES

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato, numero_saques

def exibir_extrato(saldo, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

# -----------------------------
# Função principal
# -----------------------------
def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3

    while True:
        opcao = exibir_menu()

        if opcao == "u":
            criar_usuario()
        elif opcao == "c":
            if not usuarios:
                print("Não há usuários cadastrados! Crie um usuário primeiro.")
            else:
                cpf = input("Informe o CPF do usuário para vincular a conta: ").strip()
                usuario = buscar_usuario_por_cpf(cpf)

                if usuario:
                    cadastrar_conta(usuario)
                else:
                    print("Usuário não encontrado. Verifique o CPF e tente novamente.")

        elif opcao == "d":
            saldo, extrato = depositar(saldo, extrato)
        elif opcao == "s":
            saldo, extrato, numero_saques = sacar(saldo, extrato, numero_saques, limite, LIMITE_SAQUES)
        elif opcao == "e":
            exibir_extrato(saldo, extrato)
        elif opcao == "q":
            print("Saindo do sistema...")
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

# -----------------------------
# Ponto de entrada do programa
# -----------------------------
if __name__ == "__main__":
    main()
