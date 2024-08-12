# Cryptids

*Cryptids* é um jogo de Supertrunfo baseado em criaturas misteriosas, teorias da conspiração e muitos outros contos obscuros...

## Execução 

Para executar o jogo, primeiro devem ser executados os contâineres do Docker Compose na pasta raiz do repositório:

```
sudo docker compose up -d --build
```
Então, basta executar os contâineres em diferentes terminais, com algumas peculiaridades.
É necessário que o servidor seja inicializado primeiro:
```

sudo docker exec -it server /bin/sh
```
Ou:
```

sudo docker exec -it server /bin/bash
```
Para executar os contâneres dos usuários, é necessário utilizar o seguinte comando para permitir a exibição de janelas criadas pelo Docker:
```

xhost +local:docker
```
E então podem ser executar os 3 clientes:
```

sudo docker exec -it bija /bin/sh
```
```

sudo docker exec -it thui /bin/sh
```
```

sudo docker exec -it patic /bin/sh
```
Agora, dentro de cada contâiner, execute:
```

python main.py
```
O servidor, como um agente passivo, apenas recebe e responde requisições.
A partir da tela inicial de login, os clientes podem entrar em suas respectivas contas para jogar partidas.
Contas estabelecidas:
- Username: bija, Senha: bija123
- Username: thui, Senha: thui123
- Username: patic, Senha: patick123

  Na tela de menu principal, basta abrir a tela de editar deck e escolher um deck válido para jogar. Ao retornar ao menu, clique na primeira opção para
  esperar demais jogadores para iniciar uma partida.
