#Aplicativo de Reconhecimento Facial e Controle de Ponto
Este é um aplicativo de reconhecimento facial e controle de ponto desenvolvido em Python. Com ele, você pode realizar o reconhecimento facial para autenticação, cadastrar novos usuários, alterar informações de usuários existentes, excluir usuários, marcar pontos de entrada e saída, e consultar os cadastros e pontos marcados.

##Funcionalidades
###Reconhecimento Facial:
Para realizar o reconhecimento facial, clique no botão "Verificação de Reconhecimento Facial". O sistema usará a câmera para capturar seu rosto e verificar sua identidade. Caso seja identificado com sucesso, você poderá acessar as demais funcionalidades.
Consultar Cadastros
Clique no botão "Consultar Cadastros" para visualizar uma lista de todos os usuários cadastrados no sistema.
###Marcar Ponto:
Utilize o botão "Marcar Ponto" para registrar a hora e a data do seu ponto de entrada ou saída no trabalho. O sistema associará o ponto ao seu usuário.
###Consultar Pontos:
Clique no botão "Consultar Pontos" para verificar os pontos marcados por todos os usuários.
###Cadastrar Novo Usuário:
Se você é um administrador, pode cadastrar novos usuários. Para isso, clique no botão "Cadastrar Novo Usuário" na tela de login. Preencha os campos obrigatórios, como nome, sobrenome, CPF e senha. Você pode tirar uma foto ou importar uma imagem do usuário para o reconhecimento facial.
###Alterar Usuário:
Administradores podem alterar informações de usuários existentes. Para isso, faça o login como administrador e clique no botão "Alterar Usuário". Você pode atualizar dados como nome, sobrenome, CPF e senha. Lembre-se de que você só pode alterar um dado por vez.
###Excluir Usuário:
Os administradores também podem excluir usuários. Faça o login como administrador, clique no botão "Excluir Usuário" e insira o nome de usuário e senha do usuário a ser excluído.
###Requisitos:
Para executar este aplicativo, é necessário ter Python instalado, bem como as seguintes bibliotecas:
OpenCV == 4.6.0.66
OS ( módulo )
PySimpleGUI	== 4.60.5
SQLite sqlite3 ==3.7.15
Pickle ( módulo )
face_recognition ==1.3.0
easydict==1.9
numpy==1.17.0
tqdm==4.31.1
torchvision==0.4.0
torch==1.2.0
opencv_python==4.2.0.34
Pillow==7.1.2
tensorboardX==2.0

###Instruções de Uso:
Clone este repositório para sua máquina.
Certifique-se de que todos os requisitos estejam instalados.
Execute o arquivo face_recognition_app.py para iniciar o aplicativo.
###Observações:
O reconhecimento facial é baseado nas imagens cadastradas. Certifique-se de que as imagens estejam bem iluminadas e que o rosto esteja bem visível durante o cadastro.
As senhas são armazenadas de forma criptografada no banco de dados.
A cada alteração de dados do usuário, o sistema atualiza o nome do arquivo de imagem associado ao usuário e o banco de dados.
Certifique-se de que a câmera esteja funcionando corretamente para o reconhecimento facial.
