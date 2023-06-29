import os
from AreaDoador import *
from AreaFuncionario import *

                
def Menu():
        
    os.system('cls')
    head = " SISTEMA ONG "
    print(head.center(60, '-'))
    
    menuResult = input("\n[1] Registrar doacao\n[2] Verificar historico do doador\n[3] Area do funcionario\n\n")
    match menuResult:
        
        case "1":
            Doar()
        
        case "2":        
            HistoricoDoador()

        case "3":
            AreaFuncLogin()
            
        case _:
            Menu()

Menu()