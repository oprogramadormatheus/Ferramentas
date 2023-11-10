import PySimpleGUI as sg
import asyncio
import httpx
import random

def Janela():
    sg.theme('Black')
    SG01 = sg.Text('Número', font=('Verdana', 10, 'bold'))
    SG02 = sg.Text('Número', font=('Verdana', 10, 'bold'))
    SG03 = sg.Input(enable_events=True, size=(18, 0), font=('Verdana', 10, 'bold'), key='SG03')
    SG04 = sg.Input(enable_events=True, size=(8, 0), font=('Verdana', 10, 'bold'), key='SG04')
    SG05 = sg.Input(enable_events=False, expand_x=True, expand_y=True, font=('Verdana', 10, 'bold'), key='SG05')
    SG06 = sg.Input(enable_events=False, expand_x=True, expand_y=True, font=('Verdana', 10, 'bold'), key='SG06')
    SG07 = sg.Input(enable_events=False, expand_x=True, expand_y=True, font=('Verdana', 10, 'bold'), key='SG07')
    SG08 = sg.Input(enable_events=False, expand_x=True, expand_y=True, font=('Verdana', 10, 'bold'), key='SG08')
    SG09 = sg.Input(enable_events=False, expand_x=True, expand_y=True, font=('Verdana', 10, 'bold'), key='SG09')
    SG10 = sg.Button('Checar', expand_x=True, expand_y=False, font=('Verdana', 10, 'bold'), key='SG10')
    SG11 = sg.Button('Checar', expand_x=True, expand_y=False, font=('Verdana', 10, 'bold'), key='SG11')
    SG12 = sg.Button('Gerar', expand_x=True, expand_y=False, font=('Verdana', 10, 'bold'), key='SG12')
    SG13 = sg.Frame('Checar Números', [[SG01, SG03, SG10], [SG05], [SG06]], expand_x=True, expand_y=True, font=('Verdana', 10, 'bold'))
    SG14 = sg.Frame('Checar BINs', [[SG02, SG04, SG11], [SG07], [SG08]], expand_x=True,expand_y=True, font=('Verdana', 10, 'bold'))
    SG15 = sg.Frame('Gerar Números', [[SG12], [SG09]], expand_x=True, expand_y=True, font=('Verdana', 10, 'bold'))
    Interface = [[sg.TabGroup([[sg.Tab('Ferramentas', [[SG13], [SG14], [SG15]])]], font=('Verdana', 10, 'bold'))]]
    Janela = sg.Window('Ferramentas', Interface, icon='Logo.ico')
    return Janela

def Luhn(Base):
    Separar_Base = list()
    Converter_Base = list()
    Nova_Base = list()
    for Contador_Valor in Base:
        Separar_Base.append(int(Contador_Valor))
    for Contador_Separar in range(0, len(Separar_Base)):
        if Contador_Separar % 2 == 0:
            Contador_Vezes = Separar_Base[Contador_Separar] * 2
            Converter_Base.append(str(Contador_Vezes))
        else:
            Contador_Vezes = Separar_Base[Contador_Separar] * 1
            Converter_Base.append(str(Contador_Vezes))
    for Contador_Converter in Converter_Base:
        if len(Contador_Converter) == 2:
            for Valor_Interno in Contador_Converter[0]:
                Montante_Valores = int(Contador_Converter[0]) + int(Contador_Converter[1])
                Nova_Base.append(Montante_Valores)
        else:
            Nova_Base.append(int(Contador_Converter))
    Novo_Montante = sum(Nova_Base)
    if Novo_Montante % 10 == 0:
        return True
    else:
        return False
    
async def Buscar(Base):
    URL = 'https://api.apilayer.com/bincheck/{}'.format(Base)
    Chave = {'APIKEY': 'wQtUxsKRUSZaYutvswVFVXCEUF3I1nhE'}
    try:
        async with httpx.AsyncClient(timeout=5) as API:
            Resposta = await API.get(URL, headers=Chave)
            try:
                Dados = Resposta.json()
                return Dados['scheme']
            except Exception:
                return 'Não Encontrado'
    except Exception:
        return 'Aguarde'
  
async def Rodar():
    Cores = ('#FB181D', '#009400', '#4D4D4D')
    Retorno_Janela = Janela()
    while True:
        Eventos, Valores = Retorno_Janela.read()

        def Retorno(Local, Cor, Texto=''):
            Retorno_Janela[Local].update(background_color=Cor)
            Retorno_Janela[Local].update(Texto)
            
        if Eventos == sg.WIN_CLOSED:
            break
        if Eventos == 'SG03':
            Valores_Inseridos = Valores['SG03']
            if not Valores_Inseridos.isnumeric() or len(Valores_Inseridos) > 16:
                Retorno_Janela['SG03'].update(Valores_Inseridos[:-1])
        if Eventos == 'SG04':
            Valores_Inseridos = Valores['SG04']
            if not Valores_Inseridos.isnumeric() or len(Valores_Inseridos) > 6:
                Retorno_Janela['SG04'].update(Valores_Inseridos[:-1])
        if Eventos == 'SG10':
            try:
                Valores_Inseridos = Valores['SG03']
                Retorno('SG06', Cores[2])
                if len(Valores_Inseridos) != 16:
                    Retorno('SG05', Cores[0], 'Dados Incorretos')
                else:
                    Retorno('SG05', Cores[1], 'Dados Corretos')
                    Retorno_Luhn = Luhn(Valores_Inseridos)
                    Retorno_Janela['SG03'].update('')
                    if Retorno_Luhn:
                        Retorno('SG06', Cores[1], 'True')
                    else:
                        Retorno('SG06', Cores[0], 'False')
            except Exception:
                Retorno('SG05', Cores[0], 'Erro') 
        if Eventos == 'SG11':
            try:
                Valores_Inseridos = Valores['SG04']
                Retorno_Janela['SG08'].update('')
                if len(Valores_Inseridos) != 6:
                    Retorno('SG07', Cores[0], 'Dados Incorretos')
                else:
                    Retorno_Buscar = await Buscar(Valores_Inseridos)
                    if Retorno_Buscar == 'Não Encontrado':
                        Retorno_Janela['SG04'].update('')
                        Retorno('SG07', Cores[0], Retorno_Buscar)
                    elif Retorno_Buscar == 'Aguarde':
                        Retorno('SG07', Cores[2], Retorno_Buscar)
                    else:
                        Retorno_Janela['SG04'].update('')
                        Retorno_Janela['SG08'].update(Retorno_Buscar)
                        Retorno('SG07', Cores[1], 'Dados Corretos')
            except Exception:
                Retorno('SG07', Cores[0], 'Erro')   
        if Eventos == 'SG12':
            Retorno_Janela['SG09'].update('')
            while True:
                Valores_Gerados = str(random.randint(1000000000000000, 9999999999999999))
                Retorno_Luhn = Luhn(Valores_Gerados)
                if Retorno_Luhn:
                    Retorno_Janela['SG09'].update(Valores_Gerados)
                    break
    Retorno_Janela.close()
asyncio.run(Rodar())
