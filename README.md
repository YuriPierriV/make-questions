# Make Questions

  Para rodar esse novo código é necessario dar os comando nessa ordem:
```
  chmod +x wait-for-it.sh
  docker compose build
  docker compose up -d
```


## Alinhamentos

- Siga o passo a passo para [instalar o WSL](https://github.com/codeedu/wsl2-docker-quickstart)
- Instale o docker via WSL2 pela [Documentação](https://docs.docker.com/desktop/install/ubuntu/)

- Faça um git clone do nosso repositório:

Para facilitar prefiro usar o VSCode para fazer essa parte, para isso apenas abra o terminal do WSL2 e escreva:

```
  code .
```
Verifique se está acessando os arquivos pelo WSL: Ubunto na parte inferior esquerda do VSCode. Clique no seu perfil e faça login com seu github. Após logado, acesse o terminal (Ctrl+Shift+') e escreva os seguintes códigos:

```
  git clone https://github.com/YuriPierriV/make-questions.git
```
- Caso não tenha sido feito o login corretamente vai aparecer uma mensagem solicitando usuario e senha. Aperte Ctrl+C e faça o login pelo VSCode.

- Caso efetuado a clonagem:

```
  cd make-questions/
  code .
```
Vai abrir uma nova janela agora já nos arquivos do repositório e vinculado com o github.

# GitHub

Vamos usar o github para fazer o gerenciamento, sincronização e controle do código. Para isso alguns comandos básicos para que cada um não precise perder muito tempo com isso:

- Mostra quais arquivos foram modificados, quais estão pendentes para serem adicionados ao próximo commit e fornece informações sobre o estado geral do projeto:

```
    git status
```

- Adicionar todas as mudanças (novos arquivos, alterações e exclusões) feitas nos arquivos do projeto à área de preparação. Indica quais alterações deseja incluir no próximo commit:

```
    git add .
```

-  Confirmar as mudanças selecionadas com "git add", realiza o Commit. A opção "-m" adiciona uma mensagem explicativa das alterações, mantendo um histórico claro no projeto (É importante pra manter um controle depois):

```
    git commit -m "Mensagem"
```

-  Cria uma nova branch (Linha de desenvolvimento independente que pode ser utilizada para mexer em novos recursos e corrigir bugs sem afetar o código principal). A opção "-b" cria a nova branch e "nova-branch" é o nome que você atribui a ela:

```
    git checkout -b nova-branch
```

-  Envia commits da sua ramificação local para um repositório remoto."Origin" é o repositório remoto, e "branch" é o nome da branch que você vai enviar:

```
    git push origin branch
```

-  Obtem as mudanças mais recentes de um repositório remoto. Primeiro, ele baixa as alterações do repositório remoto (usando "origin" para o repositório remoto) e, em seguida, mescla essas alterações na sua ramificação local:

```
    git pull origin branch
```
## Tecnologias

 - [HTML5](https://htmldog.com/guides/)
 - [CSS](https://htmldog.com/guides/css/)
 - [BootStrap](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
 - [Flask](https://flask.palletsprojects.com/en/3.0.x/)
 - [Docker](https://docs.docker.com/)

## Documentação de cores

| Cor               | Hexadecimal                                                |
| ----------------- | ---------------------------------------------------------------- |
| Neon Blue       | ![#010A14](https://via.placeholder.com/10/010A14?text=+) #010A14 |
| Cornflower blue   | ![#031D3A](https://via.placeholder.com/10/031D3A?text=+) #031D3A |
| Jordy Blue       | ![#041D8B](https://via.placeholder.com/10/041D8B?text=+) #041D8B |
| Periwinkle       | ![#0733F6](https://via.placeholder.com/10/0733F6?text=+) #0733F6 |
| Light cyan       | ![#CCC9DC](https://via.placeholder.com/10/CCC9DC?text=+) #CCC9DC |


https://developer.mozilla.org/en-US/docs/Web/API/Element/classList

