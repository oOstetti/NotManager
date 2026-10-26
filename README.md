Gerenciador de Notificações e Relatórios Fotográficos
Aplicativo desktop em Python para organizar notificações de regularização de infraestrutura e gerar relatórios fotográficos em PDF.

O projeto nasceu de uma necessidade prática no trabalho de um provedor de internet: reunir notificações da Copel e fotos enviadas pelos técnicos, organizar as evidências e produzir um documento para encaminhamento, sem depender da montagem manual de pastas e PDFs.
Projeto independente, sem vínculo oficial com a Copel. A aplicação organiza os documentos; o envio da resposta continua sendo feito pelo usuário.

Funcionalidades
- Cadastro e edição de notificações com identificação, título, data de emissão e observação opcional.
- Lista lateral com pesquisa por identificação ou título.
- Filtros de notificações em andamento, arquivadas ou todas.
- Painel de trabalho que reúne os dados, o documento original e as fotos.
- Importação do PDF original por seleção de arquivo ou arrastar e soltar.
- Abertura, substituição e remoção do PDF anexado.
- Importação de várias fotos com miniaturas.
- Ordenação das fotos por arrastar e soltar ou pelos botões de posição.
- Abertura de uma foto com dois cliques no aplicativo associado do Windows.
- Remoção de fotos do relatório.
- Configuração do nome e logo da empresa para a capa.
- Prévia do relatório dentro do aplicativo.
- Exportação do relatório e armazenamento de uma cópia no histórico interno.
- Arquivamento e reabertura das notificações.
- Exclusão de notificações com confirmação.
- Aviso sobre alterações de dados não salvas ao trocar de notificação ou fechar o programa.
- Persistência local com SQLite e cópias gerenciadas dos arquivos importados.
Formato do relatório
O PDF exportado segue esta sequência:
Ordem	Conteúdo
1	Capa com nome e logo da empresa, título, identificação, data de emissão e observação, quando preenchida
2 em diante	Todas as páginas do PDF original, preservadas na ordem do documento
Depois do original	Uma foto por página, na ordem definida na galeria


As páginas geradas da capa e das fotos usam formato A4. O documento original mantém os tamanhos de suas páginas. As fotos são ajustadas proporcionalmente, sem corte, com correção de orientação EXIF quando disponível.

Exemplo: capa + notificação original de duas páginas + cinco fotos = relatório de oito páginas.
Tecnologias
Tecnologia	Responsabilidade
Python	Lógica da aplicação e operações com arquivos
PySide6 / Qt Widgets	Interface desktop, eventos e arrastar e soltar
Qt PDF	Exibição da prévia do relatório na aplicação
SQLite / sqlite3	Persistência de notificações, configurações e ordem das fotos
Pillow	Leitura e tratamento das imagens
ReportLab	Geração da capa e das páginas de fotos
pypdf	Composição do PDF final com o documento original


O SQLite faz parte da biblioteca padrão do Python e não exige um servidor separado.
Requisitos
- Windows: ambiente usado no desenvolvimento.
- Python 3.12: versão usada no projeto, com ambiente informado de Python 3.12.9.
- PySide6: versão informada no ambiente de desenvolvimento, 6.12.0.
- Um leitor de PDF e um visualizador de imagens associados no Windows para abrir arquivos externamente.
- VS Code é opcional; os comandos também podem ser executados pelo PowerShell.
A aplicação usa armazenamento local e não exige conexão com serviços externos durante o uso normal. A instalação das dependências exige acesso aos pacotes ou uma instalação local previamente preparada.
Instalação no Windows
1. Obter o código
Clone ou baixe este repositório e abra a pasta do projeto no terminal. Confira se ela contém main.py, database.py e documents.py.
2. Criar o ambiente virtual
py -3.12 -m venv .venv
3. Instalar as dependências
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install PySide6 Pillow reportlab pypdf
Se o repositório já tiver um requirements.txt versionado, utilize-o no lugar da instalação individual:
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
4. Executar
.\.venv\Scripts\python.exe main.py
Os comandos usam diretamente o Python do ambiente virtual, sem depender da ativação da .venv no PowerShell.
5. Configurar o VS Code
1. Instale a extensão Python da Microsoft, caso ainda não esteja disponível.
2. Pressione Ctrl + Shift + P.
3. Selecione Python: Select Interpreter.
4. Escolha .venv\Scripts\python.exe.
5. Execute com Python: Run Python File in Terminal.
O comando Run Code, da extensão Code Runner, pode usar outro interpretador se não estiver configurado para este ambiente.
Tutorial de uso
1. Configurar a empresa
No topo da janela, clique em Empresa, informe o nome, selecione o logo e salve.

O nome e o logo são necessários para gerar o relatório. O aplicativo guarda uma cópia do logo selecionado, permitindo reutilizá-lo nas próximas notificações.
2. Criar uma notificação
Clique em + Nova notificação e preencha:
Campo	Uso
Identificação	Código, protocolo ou nome usado para reconhecer e pesquisar a notificação
Título	Texto que será exibido na capa do relatório
Data de emissão	Data do relatório exportado; pode ser ajustada pelo usuário
Observação	Texto opcional da capa


Clique em Salvar alterações. Após o primeiro salvamento, as áreas de documento e fotos ficam disponíveis.

A data de emissão é a data do relatório. Ela não representa um prazo de atendimento ou a data de recebimento da notificação.
3. Anexar o PDF original
Arraste um PDF para a área Documento original ou clique em Adicionar PDF.

Depois da importação:
- Abrir exibe o documento no leitor associado do Windows.
- Substituir PDF permite trocar o documento após confirmação.
- O menu ⋯ → Remover PDF retira a cópia anexada.
Cada notificação possui um PDF original por vez, que pode conter várias páginas. Nesta versão, utilize documentos sem proteção por senha.
4. Adicionar as fotos
Arraste imagens do Explorador de Arquivos para a galeria ou use Adicionar fotos. Os formatos aceitos são JPG, JPEG, PNG e WEBP.
- Arraste as miniaturas para ajustar a ordem.
- Use Anterior e Próxima para mover a foto selecionada na sequência.
- Dê dois cliques para abrir uma imagem no visualizador do Windows.
- Use Remover foto para retirá-la do relatório, após confirmação.
A importação e a ordenação são salvas imediatamente. Não é necessário cadastrar endereços nem associar cada foto a um poste nesta versão.
5. Conferir a prévia
Clique em Prévia do relatório. O aplicativo salva os dados do formulário e monta a visualização com os arquivos atuais.

Para gerar a prévia ou exportar, são necessários:
- Identificação e título preenchidos.
- Nome e logo da empresa configurados.
- Um PDF original anexado.
- Ao menos uma foto.
Use Voltar à edição para retornar ao painel.
6. Exportar
Clique em Exportar PDF, escolha o nome e a pasta de destino e confirme.

Além do arquivo no destino escolhido, o aplicativo guarda uma cópia no histórico interno da notificação. O botão Histórico lista as exportações disponíveis por data e hora e permite abri-las.

Após exportar, você pode optar por arquivar a notificação. A exportação não faz o envio automático à Copel ou ao CES.
7. Arquivar ou reabrir
Use Arquivar para retirar uma notificação da lista de trabalho em andamento, mantendo os dados e arquivos.

Para acessá-la novamente, selecione Arquivadas ou Todas na lista lateral. O botão Reabrir notificação devolve o registro ao andamento.
8. Excluir uma notificação
Use Excluir notificação ao lado de Arquivar e confirme a exclusão definitiva.

A exclusão remove o cadastro, as associações das fotos e a pasta interna da notificação, incluindo documento anexado, fotos e histórico de relatórios. Os arquivos de origem e os PDFs exportados para outras pastas são preservados.

Se um arquivo estiver bloqueado por outro programa, o aplicativo poderá informar que a limpeza de uma pasta interna ficou pendente.
Como os dados são salvos
Na configuração atual de database.py, os dados ficam em:
C:\Users\SEU_USUARIO\AppData\Local\GestorNotificacoes\
A organização interna é:
GestorNotificacoes/
├── notificacoes.db
├── company/
│   └── arquivos de logo
└── notifications/
    └── ID_DA_NOTIFICACAO/
        ├── original.pdf
        ├── photos/
        │   └── imagens importadas
        └── reports/
            └── relatórios exportados
O banco guarda os registros, as configurações e a ordem das fotos. Os documentos e as imagens ficam no disco, associados ao ID da notificação.
Operação	Momento do salvamento
Dados da notificação	Ao clicar em Salvar alterações; também antes da prévia e da exportação
PDF e fotos importados	Imediatamente após a importação
Ordem e remoção de fotos	Imediatamente após a ação
Configurações da empresa	Ao salvar a janela Empresa
Relatório	Ao exportar, com uma cópia adicional no histórico


Observação de implementação: remover uma foto da galeria exclui sua associação no banco, mas a cópia interna permanece no disco nesta versão. Ela deixa de entrar no relatório. A exclusão completa da notificação remove também sua pasta interna.
Backup e restauração
1. Feche o programa e os documentos internos que estiverem abertos.
2. Copie a pasta inteira GestorNotificacoes para um local de backup.
3. Guarde separadamente os PDFs exportados para outras pastas, se necessário.
Para restaurar, feche o aplicativo e recoloque o conjunto do banco e dos arquivos no caminho esperado. Preserve uma cópia dos dados atuais antes de substituí-los.

As configurações atuais guardam o caminho absoluto do logo. Ao transferir o backup para outro usuário ou computador, pode ser necessário selecionar novamente o logo em Empresa.
Estrutura do código
projeto/
├── main.py
├── database.py
├── documents.py
├── README.md
├── requirements.txt   # gerar a partir do ambiente do projeto
├── .gitignore         # criar antes do primeiro commit
└── .venv/             # ambiente local, fora do Git
Arquivo	Responsabilidade
main.py	Interface, fluxo de uso, galeria, configurações, composição dos relatórios, histórico, arquivamento e exclusão
database.py	Caminho de armazenamento, conexão SQLite e estrutura inicial das notificações
documents.py	Validação, cópia e substituição do PDF original


A main.py atual concentra parte dos serviços para simplificar esta etapa do desenvolvimento. Uma evolução possível é separar interface, acesso a dados e geração de relatórios em módulos próprios.

Os módulos photos.py e photo_dialog.py, utilizados em uma etapa anterior, não são necessários para a versão atual com painel integrado.
Fluxo interno
1. A inicialização prepara o banco e acrescenta as estruturas necessárias à versão atual.
2. O usuário seleciona ou cria uma notificação.
3. Os arquivos são copiados para a pasta gerenciada do registro.
4. A ordem da galeria é persistida no SQLite.
5. O ReportLab cria a capa e as páginas de fotos.
6. O pypdf intercala o documento original entre a capa e as fotos.
7. O relatório é gravado no destino escolhido e copiado para o histórico interno.
Publicação no GitHub
Registrar as dependências
Com as dependências instaladas no ambiente virtual do projeto, gere o arquivo:
.\.venv\Scripts\python.exe -m pip freeze | Set-Content -Encoding utf8 requirements.txt
Revise o resultado antes de publicar. Se o ambiente tiver dependências de outros projetos, elas também aparecerão no arquivo.
Criar o .gitignore
Crie um arquivo chamado .gitignore na raiz, com o conteúdo abaixo, antes de adicionar os arquivos ao Git:
# Ambiente virtual e cache Python
.venv/
venv/
__pycache__/
*.py[cod]

# Configurações e segredos locais
.env
.env.*
!.env.example

# Dados de execução e bancos locais
*.db
*.db-journal
*.db-shm
*.db-wal
*.sqlite
*.sqlite3
GestorNotificacoes/

# Pastas locais de documentos, exportações e testes manuais
uploads/
exports/
backups/
tmp/

# Empacotamento
build/
dist/
*.spec

# Sistema operacional
Thumbs.db
.DS_Store
O .gitignore não ignora indiscriminadamente todas as imagens e PDFs, pois o projeto pode receber screenshots e exemplos fictícios de documentação. Revise os arquivos selecionados para não publicar notificações reais, fotos de clientes, dados internos ou logos sem autorização.

Importante: adicionar .venv/ ao .gitignore não remove essa pasta de commits anteriores. Se ela já estiver no histórico, especialmente após um push rejeitado por arquivos grandes, é necessário corrigir esse histórico antes de tentar publicar novamente. Evite usar git push --force sem avaliar os commits existentes e quem utiliza o repositório.
Conferir e fazer o commit
Para um projeto que ainda não possui um repositório Git local:
git init
Depois de criar e revisar o .gitignore e o requirements.txt:
git status --short
git add main.py database.py documents.py README.md requirements.txt .gitignore
git diff --cached --stat
git commit -m "Adiciona gerenciador de notificações e relatórios fotográficos"
A lista explícita de arquivos ajuda a evitar a inclusão acidental do ambiente virtual ou de documentos de trabalho. Se o projeto já possui um remoto, confira-o com git remote -v e use o fluxo de publicação do repositório existente.
Solução de problemas
Problema	O que conferir
ModuleNotFoundError: No module named 'PySide6'	Execute com .\.venv\Scripts\python.exe main.py e confira o interpretador do VS Code
Import circular entre database e documents	database.py não deve importar documents.py; a interface importa ambos
Falta de database.py ou documents.py	Mantenha os três arquivos Python na mesma pasta
Arquivos não podem ser removidos ou substituídos	Feche leitores de PDF e visualizadores que possam estar bloqueando o arquivo
Relatório não é gerado	Confira os campos obrigatórios, a configuração da empresa, o PDF original e pelo menos uma foto
Textos da capa são muito longos	Reduza o título ou a observação; a capa foi projetada para uma única página
Logo não aparece após transferir o projeto	Selecione novamente o logo em Empresa; o banco de dados é separado do código
Arrastar a imagem de outro aplicativo não funciona	Salve o arquivo e arraste-o do Explorador de Arquivos, ou use Adicionar fotos


Validação e estágio do projeto
Projeto em desenvolvimento, voltado inicialmente ao uso local por um usuário. Foram realizados testes pontuais da migração do banco, composição e sequência das páginas do relatório, tratamento de data ausente e exclusão isolada de notificações. Isso não equivale a uma suíte automatizada completa de interface ou à validação de todos os formatos possíveis de arquivo.
Roteiro de conferência manual
1. Criar uma notificação e conferir sua persistência após reiniciar.
2. Editar os dados e testar salvar, descartar e cancelar ao navegar.
3. Importar, substituir e abrir o PDF original.
4. Adicionar fotos, ordenar e conferir a sequência após reiniciar.
5. Gerar a prévia e exportar; conferir capa, todas as páginas originais e uma foto por página.
6. Abrir uma exportação pelo Histórico.
7. Arquivar, pesquisar e reabrir uma notificação.
8. Excluir uma notificação fictícia e conferir que outras notificações e exportações externas permanecem.
Limites atuais e possíveis evoluções
Atualmente, o aplicativo não possui sincronização em nuvem, controle de acesso, envio automático ao CES, relacionamento entre fotos e endereços, cálculo de prazos ou instalador distribuído. Relatórios extensos são processados na própria interface e podem ocupar a janela durante a geração.

Possíveis próximos passos:
- Separar a lógica em módulos de interface, serviços e persistência.
- Processar importação e geração de PDF em segundo plano.
- Adicionar progresso e cancelamento de operações longas.
- Criar backup e restauração pela interface.
- Implementar limpeza controlada de arquivos sem associação.
- Criar testes automatizados e um processo de empacotamento para Windows.
Esses itens são sugestões de evolução, não funcionalidades já implementadas.
Autor
Desenvolvido por Felipe Ostetti Ferri, a partir de uma necessidade operacional no trabalho com redes e infraestrutura de telecomunicações, como projeto de aplicação prática de Python e desenvolvimento desktop.
Licença
Uma licença de distribuição ainda deve ser escolhida pelo autor e adicionada em um arquivo LICENSE. A disponibilização do código em um repositório público não substitui essa definição.
