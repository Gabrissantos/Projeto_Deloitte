" PROJETO DELOITTE"  

1. Introdução

Este projeto tem como objetivo criar um sistema de monitoramento de equipamentos, permitindo visualizar o status dos dispositivos e emitir alertas quando dispositivos estão em estado crítico. 

2. Ferramentas e Plataformas Utilizadas

Anaconda: Utilizado para criar e gerenciar o ambiente de desenvolvimento Python.
Flask: Um microframework para criar a API backend.
SQLite: Um banco de dados leve usado para armazenar os dados dos dispositivos.
HTML/CSS/JavaScript: Utilizados para o frontend, criando a interface do usuário.
Chart.js: Biblioteca JavaScript para gráficos, usada para visualizar os dados de status dos dispositivos.
Flask-CORS: Para permitir requisições entre o frontend e o backend.
Flask-Migrate: Para gerenciar as migrações do banco de dados.

3. Configuração Inicial

3.1.  Anaconda

Baixe e instale o Anaconda

No projeto foi utilizado o prompt anaconda

3.2 Crie um novo ambiente

conda create -n meu_projeto_flask python=3.9
conda activate meu_projeto_flask

3.3  Instalando Dependências

pip install flask flask_sqlalchemy flask_migrate flask_cors

4. Desenvolvimento Backend 

4.1. Estrutura do Projeto

Crie uma estrutura de pastas como a seguinte:

Projeto_Deloitte/ 
  App.py/ 
    app.py
    insert_data.py
    templates/ 
      index.html 
    Migrations/ 
      env.py

5. Código Backend (app.py)

6. Banco de dados e migrações 

6.1 instale alembic 

  pip install alembic

6.2 configure o alembic 

  flask db init

  flask db migrate -m "Initial migration."

  flask db upgrade

6.3 Execute

  flask run 

7. Frontend (index.html) 

8. Inserção de dados (insert_data.py)

9. Execução da aplicação 

8.1 Ative o ambiente anaconda 

   conda activate meu_projeto_flask 

8.2 Inicie a aplicação direto do diretório 

  python app.py

8.3 inicie a inserção de dados 

  python insert_data.py 

8.4 abra o navegador

   http://127.0.0.1:5000/

Agora você deve ver a interface do dashboard, que atualiza automaticamente a cada 30 segundos, exibindo os dispositivos ativos, os dispositivos com erros, gráfico de status dos dispositivos e apresentando mensagens para abrir chamado técnico quando existir status "critical"
  



