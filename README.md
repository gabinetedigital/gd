## Dependencies

Ah, temos **várias** delas, você pode ver uma lista detalhada no arquivo
_DEPS_. A maioria dessas dependências são fáceis de instalar, mas por
favor nos envie um email caso você encontre dificuldades na instalação

Recomendamos que você use um sistema GNU/Linux como Debian/Ubuntu
Para que a instalação das dependências do python ocorra sem problemas
instale as seguintes dependências:

```bash
    $ apt-get install python-dev nginix uwsgi
    $ apt-get easy-install -U
```

Recomendamos a utilização do virtualenv ou virtualenvwrapper.  Para
utilizar o virtualenv siga os seguintes passos:

```bash
    $ virtualenv --no-site-packages /home/<youruser>/gabdigital
    $ source /home/<youruser>/gabdigital/bin/activate
```
Se optar pelo virtualenvwrapper:

```bash
    $ mkvirtualenv --no-site-packages <nome_do_seu_ambiente>
    $ workon <nome_do_seu_ambiente>
```

Após concluir o passo anterior você estará dentro do virtualenv.  Assim
poderá instalar facilmente todas as dependências com a ferramenta pip ou
easy_install ou o incrível e rápido [Curdling](https://github.com/clarete/curdling)

Caso opte pelo curdinling execute:

```bash
    $ easy_install curdling
```

em seguida

```bash
    $ curd install -r DEPS_PIP
```

## Configuração

Primeiramente, você deve definir as configurações da sua aplicação.  É
bem fácil. Copie o arquivo _gd/conf.py.sample_ como _gd/conf.py_ e então
edite como quiser. É fácil de entender. Você deve lembrar que isso é um
arquivo **python**, então deve respeitar as regras e sintaxe.

## Integração com o Wordpress

Nossa aplicação é integrada com o wordpress de duas formas: base de
usuários e o gestão de conteúdo. Para a integração funcionar é
necessário seguir os seguintes passos:

* Instalar e configurar o wordpress ( Não, não vamos explicar isso,
      por favor leia a documentação do wordpress )

* Instalar e habilitar os plugins disponíveis no nosso repositório:
  * exapi
  * wpgd
  * wpgp
  * wp-widgetgd
  * wp-govpergunta
  * wp-equipegd
  * wp-clippinggd
  * wp-oquegd
  * wp-govescuta

* Instalar e habilitar os plugins disponíveis nos repositórios do
  wordpress:
  * metabox (http://metabox.io/meta-box/) Versao >=4.3.3
  * nextgen-gallery (https://wordpress.org/plugins/nextgen-gallery/download/) Versao >=1.9.3

* Habilitar a interface xmlrpc no wordpress. "Configurações >
  Escrita > XML-RPC".

* Baixar e habilitar nosso tema
  https://github.com/gabinetedigital/GabDig


## Aplicações em Python

O próximo passa é configurar o restante do banco de dados.  Apenas
execute o seguinte comando no seu projeto:

```bash
    $ python ./gd/model.py
```

Após esse pequeno passo, tudo que você precisa é rodar o servidor de
desenvolvimento executando o comando:

```bash
    $ ./bin/gdappd
```

Agora você pode acessar o link http://localhost:5000 no seu navegador e
ver o sistema rodando.

## Buzzwatcher

Nós temos outro programa em python chamado **buzzwatcher**. Ele é o
responsável por pegar as informações das redes sociais sonbra a
audiência corrente. Atualmente ele suporta apenas o twitter.

De qualquer forma, execute o seguinte comando para rodar o
**buzzwatcher**:

```bash
    $ ./bin/buzzwatcherd
```

Lembre-se isso não é tudo que você precisa fazer para criar uma
audiência.  Primeiro é necessário criar uma nova audiência no admin do
wordpress.  Tenha certeza que está tudo configurado corretamente,
incluindo o conta do twitter.

Aproveite!
