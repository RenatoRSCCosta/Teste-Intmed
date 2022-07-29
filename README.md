
# Api Medicar

Api para agendamento de consultas do medicar

## Stack utilizada

**Back-end:** Python, Django e Django Rest Framework

**Database:** PostgreSql v14


## Variáveis de Ambiente

Para rodar esse projeto, você vai precisar adicionar as seguintes variáveis de ambiente no seu **.env**

`SECRET_KEY`
`DEBUG`
`PORT`
`HOST`
`PASSWORD`
`USER`
`NAME`

Obs: No projeto existe um arquivo .env.example para consulta, o arquivo **.env** utilizado no projeto está em anexo no email

## Instruções para rodar o projeto

* Instalar as dependências com o comando 
```bash
  pip install -r requirements.txt
```
* Rodar as migrations com o comando 
```bash
  python manage.py migrate
```
* Criar um super usuário com o comando 
```bash
  python manage.py createsuperuser
```
* Rodar a aplicação com o comando 
```bash
  python manage.py runserver
```

## Admin

Para visualizar a interface administrativa do Django, basta acessar o link [http://localhost:8000/admin](http://localhost:8000/admin/)

## Endpoints

Para visualizar os endpoints disponíveis, basta acessar o link [http://localhost:8000/swagger](http://localhost:8000/swagger/)


## Infraestrutura

O projeto utiliza uma base de dados **postgreSql** hospedada em um database cluster na Digital Ocean



