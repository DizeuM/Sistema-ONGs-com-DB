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




def VerificaCadastroDoador(key):

    if len(key) == 14:
        sqlBuscaDoador = "SELECT * FROM doadores WHERE cpf = %s"
    
    else:
        sqlBuscaDoador = "SELECT * FROM doadores WHERE doadorID = %s"
    
    buscaKey = (key,)
    mycursor.execute(sqlBuscaDoador, buscaKey)
    buscaResult = mycursor.fetchone()

    if buscaResult == None:
        return None
        
    else:
        return buscaResult




def CadastraDoador():

    def ValidaCPFcad(cpf):
        
        while len(cpf) != 11 and len(cpf) != 14:
            
            os.system('cls')
            print(f"Insira seu nome: {nome}")
            print("CPF invalido, tente novamente")
            cpf = input("Insira seu CPF: ")
            
        if len(cpf) == 11:
            
            cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
            return cpf
        
        else:
            
            return cpf

    print("[CADASTRO DOADOR]")
    nome = str(input("Insira seu nome: "))
    cpf = str(input("Insira seu CPF:"))
    cpf = ValidaCPFcad(cpf)
    email = str(input("Insira seu Email: "))
    telefone = str(input("Insira seu numero de telefone: "))
    
    sqlCadastra = "INSERT INTO doadores (nome, cpf, email, telefone) VALUES (%s, %s, %s, %s)"
    valores = (nome, cpf, email, telefone)
    mycursor.execute(sqlCadastra, valores)
    
    mydb.commit()
    
    return cpf




def Doar():
    
    os.system('cls')
    print("[DOAR]")
    
    entrada = str(input("Insira seu CPF ou ID: "))
    key = CPFouID(entrada)
    buscaResult = VerificaCadastroDoador(key)
    
    if buscaResult == None:
        
        os.system('cls')
        print("Doador nao encontrado, deseja cadastrar?")
        
        resp = input("\n[C] Cadastrar | [V] Voltar | [M] Ir para o menu principal\n")
        resp = resp.lower()
        match resp:
            
            case "c":
                os.system('cls')
                key = CadastraDoador()
                buscaResult = VerificaCadastroDoador(key)
    
                doadorID = buscaResult[0]
                doadorNome = buscaResult[1]
                doadorCpf = buscaResult[2]
            
            case "v":
                Doar()
                
            case _:
                from Menu import Menu
                Menu()
    
    doadorID = buscaResult[0]
    doadorNome = buscaResult[1]
    doadorCpf = buscaResult[2]

    os.system('cls')
    print("[DOAR]")
    print(f"A doação sera feita no nome de {doadorNome}, CPF: {doadorCpf}")
    
    resp = input("\n[C] Continuar | [V] Voltar | [M] Ir para o menu principal\n")
    resp = resp.lower()
    match resp:
        
        case "c":
            os.system('cls')
            print("[DOAR]\n")
            
            valorDoado = float(input("Qual valor será doado? "))
            
            while valorDoado <= 0:
                
                os.system('cls')
                print("[DOAR]\n")
                
                print("Valor invalido, insira um numero maior que 0")
                valorDoado = float(input("Qual valor será doado? "))
                
            sqlDoacao = "INSERT INTO doacoes (doadorID, valor) VALUES (%s, %s)"
            valores = (doadorID, valorDoado)

            mycursor.execute(sqlDoacao, valores)
            mydb.commit()
            
            os.system('cls')
            print("\nDOAÇÃO FEITA COM SUCESSO!")
            sleep(1)
            
            resp = input("\n[V] Registrar outra doacao | [M] Ir para o menu principal\n")
            resp = resp.lower()
            match resp:
                
                case "v":
                    Doar()
                
                case _:
                    from Menu import Menu
                    Menu()
                    
        case "v":
            Doar()
            
        case _:
            from Menu import Menu
            Menu()




def HistoricoDoador():
    
    os.system('cls')
    print("[HISTORICO DO DOADOR]")
    
    entrada = str(input("Insira seu CPF ou ID: "))
    key = CPFouID(entrada)
    buscaResult = VerificaCadastroDoador(key)
    
    if buscaResult == None:
        
        os.system('cls')
        print("Doador nao encontrado.")
        
        resp = input("\n[V] Voltar | [M] Ir para o menu principal\n")
        resp = resp.lower()
        match resp:

            case "v":
                Doar()
                
            case _:
                from Menu import Menu
                Menu()

    
    def detalheDoador():
        buscaResult = VerificaCadastroDoador(key)
        
        doadorID = buscaResult[0]
        doadorNome = buscaResult[1]
        doadorCpf = buscaResult[2]
        doadorEmail = buscaResult[3]
        doadorTelefone = buscaResult[4]
        
        os.system('cls')
        print("[HISTORICO DO DOADOR]\n")
                    
        sqlHist = "SELECT * FROM doacoes WHERE doadorID = %s"
        mycursor.execute(sqlHist, (doadorID,) )
        rows = mycursor.fetchall()

        sqlTotal = "SELECT SUM(valor) FROM doacoes WHERE doadorID = %s"
        mycursor.execute(sqlTotal, (doadorID,))
        totalDoado = mycursor.fetchall()
        
        if totalDoado == [(None,)]:
            
            totalDoado = 0
            mostrando = "[Não foi encontrada nenhuma doacao]"
            
        else:
            
            totalDoado = float(totalDoado[0][0])
            mostrando = "[Mostando 10 ultimas doacoes]"

        print(f"Nome: {doadorNome}")
        print(f"CPF: {doadorCpf}")
        print(f"Email: {doadorEmail}")
        print(f"Telefone: {doadorTelefone}")
        print(f"\nTOTAL DOADO: %.2f\n" %totalDoado)

        for x in rows[:-11:-1]:
            
            datahora = x[3]
            data = datahora.strftime("%d/%m/%Y")
            hora = datahora.strftime("%H:%M")
            print(data, hora, "| ID doador:", str(x[1]).ljust(2, ' '), "| Valor: ", str(x[2]).ljust(8, ' '))
        
        print(mostrando)
        resp = input("\n[E] Editar telefone | [V] Voltar | [M] Ir para o menu principal\n")
        resp = resp.lower()
        match resp:
            
            case "e":
                
                telefoneNovo = str(input("\nInsira seu telefone novo: "))
                
                sqlUpdate = "UPDATE doadores SET telefone = %s WHERE doadorID = %s"
                valores = (telefoneNovo, doadorID,)
                mycursor.execute(sqlUpdate, valores)
                mydb.commit()
                
                print("\nTelefone atualizado!")
                sleep(1)
                detalheDoador()
                
            case "v":
                HistoricoDoador()
            
            case _:
                from Menu import Menu
                Menu()
                
    detalheDoador()




