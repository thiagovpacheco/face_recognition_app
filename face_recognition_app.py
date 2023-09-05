import os
import os.path
import pickle
import cv2
import face_recognition
import util
from modelos_deteccao import teste
from PySimpleGUI import PySimpleGUI as sg
import sqlite3
import time



sg.theme('TanBlue')

class AplicativoFaceID:

    def __init__(self):
        self.janela_principal = sg.Window('Aplicativo Face ID')
        sg.theme('TanBlue')
        self.verificacao_realizada = False
        self.usuario_verificado = None
        self.window_was_hidden = False  

        layout = [
            [sg.Text(text='SISTEMA DE RECONHECIMENTO FACIAL:', justification='center')],
            [sg.Button('Verificação de Reconhecimento Facial', key='verificacao_facial', size=(50, 3))],
            [sg.Button('Consultar Cadastros', key='consultar_cadastro', size=(50, 3), button_color='blue')],
            [sg.Button('Marcar Ponto', key='marcar_ponto', size=(50, 3))],
            [sg.Button('Consultar Pontos', key='consultar_pontos', size=(50, 3), button_color='blue')],
            [sg.Button('Fechar', size=(50, 3), button_color='red')]
        ]
        
        self.janela_principal.layout(layout)

        self.diretorio_db = './Pessoas_Cadastradas'
        if not os.path.exists(self.diretorio_db):
            os.makedirs(self.diretorio_db)

        self.conexao_db = sqlite3.connect('cadastros.db')
        self.cursor_db = self.conexao_db.cursor()

        self.cursor_db.execute('''CREATE TABLE IF NOT EXISTS cadastros
                                 (cpf TEXT PRIMARY KEY,
                                  nome TEXT NOT NULL,
                                  sobrenome TEXT NOT NULL,
                                  senha TEXT NOT NULL)''')
        self.conexao_db.commit()

        self.conexao_pontos_db = sqlite3.connect('pontos.db')
        self.cursor_pontos_db = self.conexao_pontos_db.cursor()

        self.cursor_pontos_db.execute('''CREATE TABLE IF NOT EXISTS pontos_marcados
                                        (nome_usuario TEXT NOT NULL,
                                         horario TEXT NOT NULL,
                                         data TEXT NOT NULL)''')
        self.conexao_pontos_db.commit()

    def iniciar(self):
        if self.formulario_login():
            while True:
                event, valores = self.janela_principal.read()

                if event == sg.WINDOW_CLOSED or event == 'Fechar':
                    break
                elif event == 'consultar_cadastro':
                    if not self.verificacao_realizada:
                        self.janela_principal.hide()
                        util.msg_box('Atenção', 'Faça o Reconhecimento Facial para consultar os cadastros.')
                        self.janela_principal.un_hide()
                        continue
                    self.janela_principal.hide()
                    self.consultar_cadastro()
                    self.janela_principal.un_hide()
                    self.verificacao_realizada = False
                elif event == 'marcar_ponto':
                    if not self.verificacao_realizada:
                        self.janela_principal.hide()
                        util.msg_box('Atenção', 'Faça o Reconhecimento Facial para marcar o ponto.')
                        self.janela_principal.un_hide()
                        continue
                    self.janela_principal.hide()
                    self.marcar_ponto()
                    self.janela_principal.un_hide()
                    self.verificacao_realizada = False
                elif event == 'consultar_pontos':
                    if not self.verificacao_realizada:
                        self.janela_principal.hide()
                        util.msg_box('Atenção', 'Faça o Reconhecimento Facial para consultar os pontos marcados.')
                        self.janela_principal.un_hide()
                        continue
                    self.janela_principal.hide()
                    self.consultar_pontos()
                    self.janela_principal.un_hide()
                    self.verificacao_realizada = False   
                elif event == 'verificacao_facial':
                    self.janela_principal.hide()
                    self.verificacao_facial()
                    self.janela_principal.un_hide()
             

            self.janela_principal.close()
            self.conexao_db.close()

    def marcar_ponto(self):
        if self.usuario_verificado is None:
            util.msg_box('Atenção', 'Faça o Reconhecimento Facial para marcar o ponto.')
            return

        nome_usuario = self.usuario_verificado
        horario_atual = time.strftime('%H:%M:%S')
        data_atual = time.strftime('%Y-%m-%d')  

    
        self.cursor_pontos_db.execute("INSERT INTO pontos_marcados (nome_usuario, horario, data) VALUES (?, ?, ?)",
                                     (nome_usuario, horario_atual, data_atual))
        self.conexao_pontos_db.commit()

        mensagem = f'Ponto marcado com sucesso!\n {nome_usuario} às {horario_atual} em {data_atual}.'
        util.msg_box('Ponto Marcado', mensagem)

    def consultar_pontos(self):
        if self.usuario_verificado is None:
            util.msg_box('Atenção', 'Faça o Reconhecimento Facial para consultar os pontos.')
            return

    
        self.cursor_pontos_db.execute("SELECT nome_usuario, horario, data FROM pontos_marcados")
        resultados = self.cursor_pontos_db.fetchall()

       
        data = resultados
        header = ['Nome do Usuário', 'Horário', 'Data']  
        layout = [
            [sg.Table(values=data, headings=header, display_row_numbers=False,
                    auto_size_columns=False, num_rows=len(data), col_widths=[30, 15, 15], 
                    justification='center', alternating_row_color='lightgray',
                    key='-TABLE-')],
            [sg.Button('Fechar', size=(10, 1), button_color='red', font=('Helvetica', 12))]
        ]

        janela_consultar_pontos = sg.Window('Consultar Pontos Marcados', layout,
                                        size=(700, 150), finalize=True) 

        while True:
            event, _ = janela_consultar_pontos.read()

            if event == sg.WINDOW_CLOSED or event == 'Fechar':
                break

        janela_consultar_pontos.close()

    def formulario_login(self):
        layout = [
            [sg.Text(text='SISTEMA DE RECONHECIMENTO FACIAL', justification='center')],
            [sg.Text('Nome de Usuário', size=(15, 1)), sg.Input(key='nome_login', size=(30, 1))],
            [sg.Text('Senha', size=(15, 1)), sg.Input(key='senha_login', size=(30, 1), password_char='*')],
            [sg.Button('Entrar', key='entrar', size=(50, 2))],
            [sg.Button('Cadastrar Novo Usuário', key='cadastrar_usuario', size=(50, 2))],
            [sg.Button('Alterar Usuário', key='alterar_usuario', size=(50, 2))],
            [sg.Button('Excluir Usuário', key='excluir_usuario', size=(50, 2))],
            [sg.Button('Fechar', key='fechar', size=(50, 2), button_color='red')]
        ]


        janela_login = sg.Window('Login').layout(layout)
        janela_cadastro_aberta = False 

        while True:
            event, valores = janela_login.read()

            if event == sg.WINDOW_CLOSED or event == 'Fechar':
                break
            elif event == 'entrar':
                nome_login = valores['nome_login']
                senha_login = valores['senha_login']

                if self.realizar_login(nome_login, senha_login):
                    janela_login.close()
                    return True
            elif event == 'cadastrar_usuario' and not janela_cadastro_aberta:
                janela_cadastro_aberta = True  
                janela_login.hide()  
                self.registrar_novo_usuario()  
                janela_login.un_hide()  
                janela_cadastro_aberta = False  
            elif event == 'alterar_usuario':
                janela_login.hide()
                self.alterar_usuario()
                janela_login.un_hide()
            elif event == 'excluir_usuario':
                janela_login.hide()
                self.excluir_usuario()
                janela_login.un_hide()
            elif event == 'fechar':
                break

        janela_login.close()
        return False

    def realizar_login(self, nome, senha):
        self.cursor_db.execute("SELECT * FROM cadastros WHERE nome = ? AND senha = ?", (nome, senha))
        resultado = self.cursor_db.fetchone()
        if resultado:
            self.verificacao_realizada = True
            self.usuario_verificado = None  
            return True
        else:
            sg.popup_error('Nome de usuário ou senha incorretos.')
            return False


    def registrar_novo_usuario(self):
       
        layout = [
            [sg.Text(text='INSIRA OS DADOS ABAIXO: ', justification='center')],
            [sg.Text('Nome', size=(9, 1)), sg.Input(key='nome', size=(53, 1))],
            [sg.Text('Sobrenome', size=(9, 1)), sg.Input(key='sobrenome', size=(25, 1)),
            sg.Text(text='CPF', size=(3, 1)), sg.Input(key='cpf', size=(18, 1))],
            [sg.Text('Senha', size=(9, 1)), sg.Input(key='senha', size=(15, 1), password_char='*'),
            sg.Text('Confirmação Senha', size=(15, 1)), sg.Input(key='confirmar_senha', size=(15, 1), password_char='*')],
            [sg.Button('Tirar foto e salvar', key='cadastrar', size=(20, 2)),
             sg.Button('Importar foto e salvar', key='importar_foto', size=(20, 2)),
             sg.Button('Cancelar', key='cancelar', size=(20, 2), button_color= 'red')]
        ]

        janela_cadastrar_usuario = sg.Window('Cadastrar Novo Usuário').layout(layout)

        while True:
            event, valores = janela_cadastrar_usuario.read()

            if event == sg.WINDOW_CLOSED or event == 'cancelar':
                break
            elif event == 'cadastrar':
                if self.validar_cadastro(valores):
                    nome = valores['nome']
                    sobrenome = valores['sobrenome']
                    self.capturar_fotografia(nome, sobrenome, valores)
                    janela_cadastrar_usuario.close()
                    self.formulario_login()
            elif event == 'importar_foto':
                if self.validar_cadastro(valores):
                    nome = valores['nome']
                    sobrenome = valores['sobrenome']
                    self.importar_fotografia(nome, sobrenome, valores)
                    janela_cadastrar_usuario.close()
                    self.formulario_login()

        janela_cadastrar_usuario.close()

    def validar_cadastro(self, valores):
        nome = valores['nome']
        sobrenome = valores['sobrenome']
        senha = valores['senha']
        confirmar_senha = valores['confirmar_senha']

        if not nome or not sobrenome or not senha or not confirmar_senha:
            util.msg_box('Erro', 'Todos os campos devem ser preenchidos.')
            return False

        if senha != confirmar_senha:
            util.msg_box('Erro', 'As senhas não coincidem.')
            return False

        nome_completo = f'{nome} {sobrenome}'
        caminho_arquivo = os.path.join(self.diretorio_db, f'{nome_completo}.pickle')

        if os.path.exists(caminho_arquivo):
            util.msg_box('Erro', 'Usuário já cadastrado.')
            return False

        return True

    def alterar_usuario(self):
        
        layout_login = [
            [sg.Text('Nome de Usuário', size=(15, 1)), sg.Input(key='nome_usuario')],
            [sg.Text('Senha', size=(15, 1)), sg.Input(key='senha_usuario', password_char='*')],
            [sg.Button('Ok', key='login'), sg.Button('Cancelar', key='cancelar', button_color='red')],
        ]

        janela_login = sg.Window('Login').layout(layout_login)

        while True:
            event_login, valores_login = janela_login.read()

            if event_login == sg.WINDOW_CLOSED or event_login == 'cancelar':
                break
            elif event_login == 'login':
                nome_usuario = valores_login['nome_usuario']
                senha_usuario = valores_login['senha_usuario']

                
                self.cursor_db.execute("SELECT * FROM cadastros WHERE nome = ? AND senha = ?", (nome_usuario, senha_usuario))
                resultado = self.cursor_db.fetchone()

                if resultado:
                    
                    layout_alterar_usuario = [
                        [sg.Text('ALTERE SOMENTE UM DADO DO USUÁRIO POR VEZ:', justification='center')],
                        [sg.Text('Nome de Usuário', size=(15, 1)), sg.Input(key='novo_nome', size=(53, 1), default_text=resultado[1])],
                        [sg.Text('Sobrenome', size=(15, 1)), sg.Input(key='novo_sobrenome', size=(25, 1), default_text=resultado[2]),
                        sg.Text(text='CPF', size=(15, 1)), sg.Input(key='novo_cpf', size=(18, 1), default_text=resultado[0])],
                        [sg.Text('Senha', size=(15, 1)), sg.Input(key='nova_senha', size=(15, 1), password_char='*', default_text=resultado[3]),
                        sg.Text('Confirmar Senha', size=(15, 1)), sg.Input(key='confirmar_senha', size=(15, 1), password_char='*', default_text=resultado[3])],
                        [sg.Button('Tirar foto e salvar', key='alterar', size=(20, 2)),
                        sg.Button('Importar foto e salvar', key='importar_foto', size=(20, 2)),
                        sg.Button('Cancelar', key='cancelar_alterar', size=(20, 2), button_color='red'),
                        sg.Button('Salvar Dados', key='salvar', size=(20, 2))],
                    ]

                    janela_alterar_usuario = sg.Window('Alterar Dados de Usuário').layout(layout_alterar_usuario)

                    while True:
                        event_alterar, valores_alterar = janela_alterar_usuario.read()

                        if event_alterar == sg.WINDOW_CLOSED or event_alterar == 'cancelar_alterar':
                            break
                        elif event_alterar == 'salvar':
                            novo_nome = valores_alterar['novo_nome']
                            novo_sobrenome = valores_alterar['novo_sobrenome']
                            novo_cpf = valores_alterar['novo_cpf']
                            nova_senha = valores_alterar['nova_senha']
                            confirmar_senha = valores_alterar['confirmar_senha']

                            if nova_senha != confirmar_senha:
                                sg.popup_error('As senhas não coincidem. Tente novamente.')
                            else:
                                
                                nome_usuario_atual = resultado[1]
                                sobrenome_atual = resultado[2]
                                if novo_nome != nome_usuario_atual or novo_sobrenome != sobrenome_atual:
                                    
                                    novo_nome_arquivo = f"{novo_nome} {novo_sobrenome}.pickle"
                                    nome_arquivo_atual = f"{nome_usuario_atual} {sobrenome_atual}.pickle"

                                    
                                    if novo_nome != nome_usuario_atual:
                                        os.rename(os.path.join('./Pessoas_Cadastradas', nome_arquivo_atual),
                                                os.path.join('./Pessoas_Cadastradas', novo_nome_arquivo))

                                
                                if novo_nome != nome_usuario_atual or novo_sobrenome != sobrenome_atual:
                                    self.atualizar_arquivo_pickle(nome_usuario_atual, sobrenome_atual, novo_nome, novo_sobrenome)
                                    


                                
                                if novo_nome:
                                    self.cursor_db.execute("UPDATE cadastros SET nome = ? WHERE nome = ?", (novo_nome, nome_usuario))
                                if novo_sobrenome:
                                    self.cursor_db.execute("UPDATE cadastros SET sobrenome = ? WHERE nome = ?", (novo_sobrenome, nome_usuario))
                                if novo_cpf:
                                    self.cursor_db.execute("UPDATE cadastros SET cpf = ? WHERE nome = ?", (novo_cpf, nome_usuario))
                                if nova_senha:
                                    self.cursor_db.execute("UPDATE cadastros SET senha = ? WHERE nome = ?", (nova_senha, nome_usuario))

                                self.conexao_db.commit()

                                util.msg_box('Sucesso', f'Dados do usuário "{nome_usuario}" foram alterados com sucesso.')
                                break

                    janela_alterar_usuario.close()
                    break
                else:
                    sg.popup_error('Nome de usuário ou senha incorretos.')

        janela_login.close()

    
    def atualizar_arquivo_pickle(self, nome_anterior, sobrenome_anterior, novo_nome, novo_sobrenome):
        
        nome_arquivo_anterior = f"{nome_anterior} {sobrenome_anterior}.pickle"
        novo_nome_arquivo = f"{novo_nome} {novo_sobrenome}.pickle"

        
        caminho_arquivo_anterior = os.path.join(self.diretorio_db, nome_arquivo_anterior)
        caminho_novo_arquivo = os.path.join(self.diretorio_db, novo_nome_arquivo)

        if os.path.exists(caminho_arquivo_anterior):
            try:
                
                os.rename(caminho_arquivo_anterior, caminho_novo_arquivo)

                
                if os.path.exists(caminho_novo_arquivo):
                    
                    with open(caminho_novo_arquivo, 'rb') as novo_arquivo:
                        dados_atualizados = pickle.load(novo_arquivo)

                    
                    dados_atualizados['nome'] = novo_nome
                    dados_atualizados['sobrenome'] = novo_sobrenome

                    
                    with open(caminho_novo_arquivo, 'wb') as novo_arquivo:
                        pickle.dump(dados_atualizados, novo_arquivo)

                    
                    os.remove(caminho_arquivo_anterior)

                    return True
                else:
                    return False
            except Exception as e:
                print(f"Erro ao renomear o arquivo: {str(e)}")
                return False
        else:
            print(f"Arquivo anterior '{caminho_arquivo_anterior}' não encontrado.")
            return False
        
    def excluir_usuario(self):
        
        layout_login = [
            [sg.Text('Nome de Usuário', size=(15, 1)), sg.Input(key='nome_usuario')],
            [sg.Text('Senha', size=(15, 1)), sg.Input(key='senha_usuario', password_char='*')],
            [sg.Button('Ok', key='login'), sg.Button('Cancelar', key='cancelar', button_color='red')],
        ]

        janela_login = sg.Window('Login').layout(layout_login)

        while True:
            event_login, valores_login = janela_login.read()

            if event_login == sg.WINDOW_CLOSED or event_login == 'cancelar':
                break
            elif event_login == 'login':
                nome_usuario = valores_login['nome_usuario']
                senha_usuario = valores_login['senha_usuario']

                
                self.cursor_db.execute("SELECT * FROM cadastros WHERE nome = ? AND senha = ?", (nome_usuario, senha_usuario))
                resultado = self.cursor_db.fetchone()

                if resultado:
                    
                    nome_arquivo = f'{resultado[1]} {resultado[2]}.pickle'
                    caminho_arquivo = os.path.join(self.diretorio_db, nome_arquivo)

                    if os.path.exists(caminho_arquivo):
                        os.remove(caminho_arquivo)

                    
                    self.cursor_db.execute("DELETE FROM cadastros WHERE nome = ?", (nome_usuario,))
                    self.conexao_db.commit()

                    sg.popup('Usuário excluído com sucesso.')
                    break
                else:
                    sg.popup_error('Nome de usuário ou senha incorretos.')

        janela_login.close()

    def capturar_fotografia(self, nome, sobrenome, valores):
        nome_arquivo = f'{nome} {sobrenome}.pickle'
        caminho_arquivo = os.path.join(self.diretorio_db, nome_arquivo)

        if os.path.exists(caminho_arquivo):
            sg.popup('Usuário já cadastrado.')
            return

        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()

            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            cv2.imshow('Capturar Fotografia Facial', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        
        face_locations = face_recognition.face_locations(frame_rgb)
        if len(face_locations) == 0:
            util.msg_box('Ops...', 'Nenhuma face foi encontrada na imagem.')
        else:
            embeddings = face_recognition.face_encodings(frame_rgb, face_locations)[0]

            with open(caminho_arquivo, 'wb') as arquivo:
                pickle.dump(embeddings, arquivo)

            self.salvar_cadastro(valores)

            sg.popup('Fotografia capturada e dados salvos com sucesso.')


    def importar_fotografia(self, nome, sobrenome, valores):
        nome_arquivo = f'{nome} {sobrenome}.pickle'
        caminho_arquivo = os.path.join(self.diretorio_db, nome_arquivo)

        if os.path.exists(caminho_arquivo):
            sg.popup('Usuário já cadastrado.')
            return

        file_types = [("Imagens", "*.jpg *.jpeg *.png")]
        foto_path = sg.popup_get_file('Selecione uma imagem contendo o rosto do usuário', file_types=file_types)

        if foto_path:
            image = cv2.imread(foto_path)

            
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            
            face_locations = face_recognition.face_locations(image_rgb)  
            if len(face_locations) == 0:
                util.msg_box('Ops...', 'Nenhuma face foi encontrada na imagem.')
            else:
                embeddings = face_recognition.face_encodings(image_rgb, face_locations)[0]  

                with open(caminho_arquivo, 'wb') as arquivo:
                    pickle.dump(embeddings, arquivo)

                self.salvar_cadastro(valores)

                sg.popup('Fotografia importada e dados salvos com sucesso.')
            

    def salvar_cadastro(self, valores):
        cpf = valores['cpf']
        nome = valores['nome']
        sobrenome = valores['sobrenome']
        senha = valores['senha']

        
        self.cursor_db.execute("INSERT INTO cadastros (cpf, nome, sobrenome, senha) VALUES (?, ?, ?, ?)",
                            (cpf, nome, sobrenome, senha))
        self.conexao_db.commit()

    def consultar_cadastro(self):
        if self.usuario_verificado is None:
            util.msg_box('Atenção', 'Faça o Reconhecimento Facial para consultar os cadastros.')
            return

        
        layout = [
            [sg.Text(text=f'Bem-vindo(a), {self.usuario_verificado}!', justification='center')],
            [sg.Button('Consultar', key='consultar', size=(50, 2))],
            [sg.Button('Fechar', key='fechar', size=(50, 2), button_color='red')]
        ]

        janela_consultar_cadastro = sg.Window('Consultar Cadastros').layout(layout)

        while True:
            event, valores = janela_consultar_cadastro.read()

            if event == sg.WINDOW_CLOSED:
                break
            elif event == 'consultar':
                if not self.verificacao_realizada:
                    util.msg_box('Atenção', 'Faça o Reconhecimento Facial para consultar os cadastros.')
                else:
                    self.exibir_todos_os_cadastros()
                break
            elif event == 'fechar':
                break

        janela_consultar_cadastro.close()


    def exibir_todos_os_cadastros(self):
        
        self.cursor_db.execute("SELECT cpf, nome, sobrenome FROM cadastros")
        resultados = self.cursor_db.fetchall()

        
        data = resultados
        header = ['CPF', 'Nome', 'Sobrenome']
        layout = [
            [sg.Table(values=data, headings=header, display_row_numbers=False,
                    auto_size_columns=False, num_rows=len(data), col_widths=[15, 30, 30],
                    justification='center', alternating_row_color='lightgray',
                    key='-TABLE-')],
            [sg.Button('Fechar', size=(10, 1), button_color='red', font=('Helvetica', 12))]
        ]

        janela_todos_os_cadastros = sg.Window('Usuários Cadastrados', layout,
                                        size=(700, 150), finalize=True)

        while True:
            event, _ = janela_todos_os_cadastros.read()

            if event == sg.WINDOW_CLOSED or event == 'Fechar':
                break

        janela_todos_os_cadastros.close()

    def verificacao_facial(self):
        
        cap = cv2.VideoCapture(0)

        start_time = time.time()  
        embeddings = None  
        encontrou_correspondencia = False  

        while True:
            ret, frame = cap.read()

            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            
            cv2.imshow('Camera', frame)

            current_time = time.time()
            elapsed_time = current_time - start_time

            
            if elapsed_time >= 3:
                
                face_locations = face_recognition.face_locations(frame_rgb)  

                if len(face_locations) == 1:
                    embeddings = face_recognition.face_encodings(frame_rgb, face_locations)[0]

                    
                    encontrou_correspondencia = False
                    for nome_pickle in os.listdir(self.diretorio_db):
                        if nome_pickle.endswith(".pickle"):
                            caminho_arquivo_pickle = os.path.join(self.diretorio_db, nome_pickle)

                            with open(caminho_arquivo_pickle, 'rb') as file:
                                embeddings_cadastrado = pickle.load(file)

                            distancia = face_recognition.face_distance([embeddings_cadastrado], embeddings)

                            if distancia[0] < 0.6:
                                encontrou_correspondencia = True
                                self.verificacao_realizada = True  
                                self.usuario_verificado = nome_pickle.replace('.pickle', '')  
                                util.msg_box('Verificação Facial', f'Usuário: {self.usuario_verificado}\nDistância: {distancia[0]}')
                                break
                    
                if encontrou_correspondencia:
                    break
                else:
                    
                    label = teste(
                        imagem=frame,
                        diretorio_modelo=r'C:\Users\Thiago Vellasco\Desktop\Projetos VS Code\resources\anti_spoof_models',
                        id_dispositivo=0
                    )

                    if label == 1:
                        util.msg_box('Verificação Facial', 'Usuário não identificado.\nTente novamente.')
                    else:
                        util.msg_box('Ei, você é um impostor!', 'Você é fake!')
                    break
            
            cv2.imshow('Camera', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

    def verificar_login(self, usuario, senha, resultado):
        
        usuario_armazenado = resultado[1]
        senha_armazenada = resultado[3]

        if usuario == usuario_armazenado and senha == senha_armazenada:
            return True
        else:
            util.msg_box('Erro', 'Nome de usuário ou senha incorretos.')
            return False

app = AplicativoFaceID()
app.iniciar()