
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




## 🔗 Links
[![github](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://github.com/RenatoRSCCosta)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/renato-costa-95b18a1a4/)



## Referência

 - [Django Docs](https://docs.djangoproject.com/en/4.0/)
 - [Django Rest Framework Docs](https://www.django-rest-framework.org/)
 - [Alura - Formação Django](https://www.alura.com.br/formacao-django)
 - [Alura - Formação Django REST Api](https://www.alura.com.br/formacao-django-rest)
