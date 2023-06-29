import os
from Connector import *
from time import sleep

def CPFouID(cpf):
     
    if len(cpf) == 11:
        
        cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        return cpf
    
    if len(cpf) == 14:
        
        return cpf
        
    else:
        
        id = cpf
        return id




def VerificaCadastroFucionario(key, senha):

    if len(key) == 14:
        sqlBuscaFunc = "SELECT * FROM funcionarios WHERE cpf = %s"
    
    else:
        sqlBuscaFunc = "SELECT * FROM funcionarios WHERE funcionarioID = %s"
    
    buscaKey = (key,)
    mycursor.execute(sqlBuscaFunc, buscaKey)
    buscaResult = mycursor.fetchone()

    if buscaResult != None:
        funcionarioSenha = buscaResult[2]
        if senha == funcionarioSenha:
            
            return buscaResult
        
        else:
            return None
        
    else:
        return None




def AreaFuncLogin():
    
    os.system('cls')
    print("[AREA DO FUNCIONARIO]\n")
    
    entrada = str(input("Insira seu CPF ou ID: "))
    senha = str(input("Senha: "))
    global key
    key = CPFouID(entrada)
    global buscaResult
    buscaResult = VerificaCadastroFucionario(key, senha)
    
    if buscaResult == None:

        os.system('cls')
        print("Login ou senha inválidos")

        resp = input("\n[V] Voltar | [M] Ir para o menu principal\n")
        resp = resp.lower()
        match resp:

            case "v":
                AreaFuncLogin()
                
            case _:
                from Menu import Menu
                Menu()
                
    AreaFunc()  




def AreaFunc():
        os.system('cls')
        print("[AREA DO FUNCIONARIO]")
        print(f"[{buscaResult[1]} | ID: {buscaResult[0]}]\n")
        
        sqlTotal = "SELECT SUM(valor) FROM doacoes"
        mycursor.execute(sqlTotal)
        totalDoado = mycursor.fetchall()
        totalDoado = float(totalDoado[0][0])
        
        sqlTotal = "SELECT SUM(valor) FROM despesas"
        mycursor.execute(sqlTotal)
        totalRetirado = mycursor.fetchall()
        
        if totalDoado == [(None,)]:
            saldo = 0
        
        if totalRetirado == [(None,)]:
            saldo = totalDoado
            
        else:
            totalRetirado = float(totalRetirado[0][0])
            saldo = totalDoado - totalRetirado
            
        print(f"SALDO ATUAL: R$ %.2f\n" %saldo)
        
        
        menuResult = input("[1] Registrar saida de dinheiro\n[2] Historicos doacoes e retiradas\n[3] Manutenção de funcionarios\n\n[4] Deslogar e voltar para o menu principal\n\n")
        match menuResult:
            
            case "1":
                Retirada()
            
            case "2":        
                Historicos()

            case "3":
                Funcionarios()
                
            case "4":
                from Menu import Menu
                Menu()
                
                
            case _:
                AreaFunc()
               
               
               
                
def Retirada():
    
    os.system('cls')
    print("[REGISTRAR SAIDA DE DINHEIRO]\n")
    
    valorRetirado = float(input("Qual valor será retirado? "))
    
    while valorRetirado <= 0:
    
        os.system('cls')
        print("[REGISTRAR SAIDA DE DINHEIRO]\n")
        
        print("Valor invalido, insira um numero maior que 0")
        valorRetirado = float(input("Qual valor será retirado? "))

    os.system('cls')
    print("[REGISTRAR SAIDA DE DINHEIRO]\n")
    
    print(f"Qual valor será retirado? {valorRetirado }")
    descricao = input("Descricao de saida: ")
    
    sqlSaida = "INSERT INTO despesas (descricao, valor, funcionarioresponsavelID) VALUES (%s, %s, %s)"
    valores = (descricao, valorRetirado, key)
    mycursor.execute(sqlSaida, valores)
    mydb.commit()
    
    os.system('cls')
    print("\nSAIDA REGISTRADA COM SUCESSO!")
    sleep(1)
    
    resp = input("\n[V] Registrar outra saida | [M] Ir para o menu principal\n")
    resp = resp.lower()
    match resp:
        
        case "v":
            Retirada()
        
        case _:
            AreaFunc()
    
    

    
def Historicos():
    
    def HistoricoDoacao():
        
        sqlHistTotal = "SELECT * FROM doacoes"
        mycursor.execute(sqlHistTotal)
        
        rows = mycursor.fetchall()
        
        sqlTotalValor = "SELECT SUM(valor) FROM doacoes"
        mycursor.execute(sqlTotalValor)
        totalDoado = mycursor.fetchall()
        totalDoado = float(totalDoado[0][0])
            
        os.system('cls')
        print("[HISTORICO DE DOACOES]\n")
        
        print(f"TOTAL DOADO: %.2f\n" %totalDoado)
        
        linha = 1
        for x in rows[:-11:-1]:
            
            datahora = x[3]
            data = datahora.strftime("%d/%m/%Y")
            hora = datahora.strftime("%H:%M")
            print(data, hora, "| ID doador:", str(x[1]).ljust(2, ' '), "| Valor: ", str(x[2]).ljust(8, ' '))
            
            if linha != 10:
                linha += 1
        
        print("[Mostando 10 ultimas doacoes]")
        resp = input("\n[V] Voltar | [M] Ir para o menu principal\n")
        resp = resp.lower()
        match resp:

            case "v":
                Historicos()
            
            case _:
                AreaFunc()
                    
                    
    def HistoricoRetiradas():
        
        sqlHistTotal = "SELECT * FROM despesas"
        mycursor.execute(sqlHistTotal)
        
        rows = mycursor.fetchall()
        
        os.system('cls')
        print("[HISTORICO DE DOACOES]\n")
        
        linha = 1
        for x in rows[:-11:-1]:
            
            datahora = x[4]
            data = datahora.strftime("%d/%m/%Y")
            hora = datahora.strftime("%H:%M")
            print(data, hora, " | Funcionario:", str(x[1]).ljust(2, ' '), "| Valor:", str(x[3]).ljust(8, ' '), "|", x[2])
            
            if linha != 10:
                linha += 1
                
        print("[Mostando 10 ultimas retiradas]")
        resp = input("\n[V] Voltar | [M] Ir para o menu principal\n")
        resp = resp.lower()
        match resp:

            case "v":
                Historicos()
            
            case _:
                AreaFunc()
                    
        
        
        
    os.system('cls')
    print("[HISTORICOS]\n")
        
    resp = input("[1] Historico de doacoes\n[2] Historico de retiradas\n\n[M] Ir para o menu principal\n")
    resp = resp.lower()
    match resp:
        
        case "1":
            HistoricoDoacao()
            
        case "2":
            HistoricoRetiradas()
        
        case _:
            AreaFunc()
    
    
    
    
def Funcionarios():
    
    os.system('cls')
    print("[AREA DO FUNCIONARIO]")
    print("Digite o numero do funcionario para ver os detalhes\n")
    
    sqlBuscaFunc = "SELECT * FROM funcionarios"
    mycursor.execute(sqlBuscaFunc)
    rows = mycursor.fetchall()

    for x in rows:
        print("ID:", str(x[0]).ljust(2, ' '), "| Nome:", x[1].ljust(10, ' '), "| Telefone:", x[5])
    
    resp = str(input("\n[M] Voltar para o menu\n"))
    if resp.isdigit():
        
        sqlFunc = "SELECT * FROM funcionarios WHERE funcionarioID = %s"
        mycursor.execute(sqlFunc, (resp,) )
        detalhes = mycursor.fetchone()
        
        if detalhes != None:
            
            def detalheFunc(resp):
                
                sqlFunc = "SELECT * FROM funcionarios WHERE funcionarioID = %s"
                mycursor.execute(sqlFunc, (resp,) )
                detalhes = mycursor.fetchone()
                
                funcionarioID = detalhes[0]
                funcionarioNome = detalhes[1]
                funcionarioCpf = detalhes[3]
                funcionarioEmail = detalhes[4]
                funcionarioTelefone = detalhes[5]
                
                os.system('cls')
                print("[DETALHES DO FUNCIONARIO]\n")
                
                print(f"ID: {funcionarioID}")
                print(f"Nome: {funcionarioNome}")
                print(f"CPF: {funcionarioCpf}")
                print(f"Email: {funcionarioEmail}")
                print(f"Telefone: {funcionarioTelefone}")
                
                print("\n[E] Editar telefone | [D] Desligar Funcionario")
                resp = input("[V] Voltar          | [M] Ir para o menu principal\n")
                resp = resp.lower()
                match resp:
                    
                    case "d":
                        os.system('cls')
                        
                        print(f"Tem certeza que deseja desligar {funcionarioNome} de ID: {funcionarioID}? ")
                        resp = input("\n[1] Sim | [V] Voltar | [M] Ir para o menu principal\n")
                        match resp:
                            
                            case "1":
                                
                                try:
                                    sqlDelete = "DELETE FROM funcionarios WHERE funcionarioID = %s"
                                    valores = f"{funcionarioID}",
                                    mycursor.execute(sqlDelete, valores)
                                    mydb.commit()
                                
                                    print("Funcionario desligado.")
                                    sleep(1)
                                    Funcionarios()
                                
                                except:
                                    print("\n*Voce nao pode se excluir*")
                                    sleep(1)
                                    resp = funcionarioID
                                    detalheFunc(resp)
                                    
                            
                            case "v":
                                resp = funcionarioID
                                detalheFunc(resp)
                                
                            case _:
                                Funcionarios()
                    case "e":
                        telefoneNovo = str(input("\nInsira seu telefone novo: "))
                        
                        sqlUpdate = "UPDATE funcionarios SET telefone = %s WHERE funcionarioID = %s"
                        valores = (telefoneNovo, funcionarioID,)
                        mycursor.execute(sqlUpdate, valores)
                        mydb.commit()
                        
                        print("\nTelefone atualizado!")
                        sleep(1)
                        resp = funcionarioID
                        detalheFunc(resp)
                        
                    
                    case "v":
                        Funcionarios()
                    
                    case _:
                        AreaFunc()
                        
            detalheFunc(resp)
                
        else:
            Funcionarios()
    
    else:
        
        resp = resp.lower()
        match resp:
            
            case "m":
                AreaFunc()

            
            case _:
                AreaFunc()
