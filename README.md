# product-fast-api

> Descrição:
### Restful API desenvolvida para o teste da Tech Solutio. Realiza autentição, registro de usuário, logout e crud de produtos. O SGBD é Postgresql e há também a utilização de Redis (NoSql) para salvar a lista de produtos em cache.

> Execução:
### Instale o docker no seu desktop e rode o seguinte comando:
~~~
docker compose up
~~~

> Migrações:
#### Faça as migrações com os seguintes comandos.

#### Acessar container:
~~~
docker exec -it flask_app sh
~~~

#### Iniciar aplicação no container:
~~~
export FLASK_APP=run.py
~~~

#### Define o modo de execução:
~~~
export FLASK_ENV=development
~~~

#### Cria pasta de migrations caso não haja:
~~~
flask db init 
~~~

#### Fazer uma migração:
~~~
flask db migrate -m "Initial migration"
~~~

#### Subir migração:
~~~
flask db upgrade
~~~

> Documentação:
#### Por fim acesse a documentação do swagger da api
~~~
http://127.0.0.1:5000/api/v1/docs
~~~


>>
