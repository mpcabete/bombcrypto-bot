<h1 align="center">

![Bomb Crypto Banner](https://raw.githubusercontent.com/vin350/bombcrypto-bot/main/images/readme/banner.jpg)

  <a>
    Bomb Crypto Bot
  </a>
</h1>

## 📋 Sobre
Este bot tem o seu código aberto, de forma que qualquer pessoa pode vê-lo, fazer uma fork, ou updates.

Desenvolvi esse bot inicialmente para o meu uso pessoal. Eu decidi publica-lo
aqui para ajudar o pessoal e com a esperança de ganhar um trocadinho com
doações.  Com o tempo mais e mais pessoas foram abrindo issues, pedindo ajuda,
e dando sugestões. Eu tento responder todo mundo, mas ultimamente tem sido
difícil acompanhar a demanda. 

Eu gostaria de manter este bot grátis e com o código aberto. Para que isso
seja possível eu estou criando algumas metas de doação para que o bot possa
ser financiado coletivamente. Atualmente eu atualizarei a barra das metas
manualmente de forma diária, talvez no futuro eu automatize o processo de
alguma forma.

- [x] 1 - Inserir um valor aleatório em todos os movimentos e os intervalos de
espera do bot para dificultar ainda mais sua detecção.

- [x] 2 - Implementar com o telegram para facilitar o gerenciamento.

- [x] 3 - Implementar Movimentos "Humanizados" para evitar detecção.

- [ ] 4 - Implementar uma tecla para fechar o bot.


``` 
- 06/12/21
             (15%)        (30%)         (50%)        (70%)      (85%)     (100%)
[XXXXXXXXXXXXXXX|XXXXXXXXXX|XXXXXXXXXXXXXX|XXXXXXXXXXX|XXX-------|------------] (500R$)
                                                          |
                                                        380R$
```

 
## 🎁 Wallet
### 0x29f3f79179C942d227ec38755c0C1Ea4976672C1

## ⚠️ Aviso

#### Os desenvolvedores do jogo se pronunciaram e agora o uso de auto clickers
e o uso de bots é oficialmente PROIBIDO. Não me responsabilizo por eventuais
penalidades sofridas por quem usar o bot, use por sua própria conta e risco.

## 🪟 Instalação:
### Baixe e instale o Python pelo site [https://www.python.org/downloads/](https://www.python.org/downloads/)


É importante marcar a opção para adicionar o
python ao PATH:
![Check Add python to PATH](https://raw.githubusercontent.com/vin350/bombcrypto-bot/main/images/readme/path.png)

### Realize o download do codigo no formato zip, e extraia o arquivo.

### Copie o caminho até a pasta do bot:

![caminho](https://raw.githubusercontent.com/vin350/bombcrypto-bot/main/images/readme/address.png)

### Abra o terminal.

Aperte a tecla do windows + r e digite "cmd":

![launch terminal](https://raw.githubusercontent.com/vin350/bombcrypto-bot/main/images/readme/cmd.png)

### Navegue até a pasta do bot:
Digite o comando "cd" + caminho que você copiou:

![cd](https://raw.githubusercontent.com/vin350/bombcrypto-bot/main/images/readme/cd.png)

### Instale as dependências:

```
pip install -r requirements.txt
```

  
![pip](https://raw.githubusercontent.com/vin350/bombcrypto-bot/main/images/readme/pip.png)

### Pronto! Agora é só iniciar o bot com o comando

```
python index.py
```

![run](https://raw.githubusercontent.com/vin350/bombcrypto-bot/main/images/readme/run.png)


## ⚒️ Como usar?

Abra o terminal, se ainda não tiver navegado para a pasta do bot dê novamente o comando

```
"cd" + caminho que você copiou
```

Para iniciar use o comando 

```
python index.py
```

Assim que ele iniciar ele vai começar mandando os bonecos trabalhar. Para que ele funcione é preciso que a janela do game esteja aparecendo na sua tela.
Ele vai constantemente checar se você foi desconectado para realizar o login novamente, e se o botão “new map” tá na tela para clicar nele.
A cada 15 minutos ele manda todos os heróis taralharem.

### **Como funciona?**

O bot não interage diretamente com o jogo, ele somente tira print da tela do
game para encontrar os botões e simula movimentos do mouse, isso faz com que
diferenciar o bot de um humano seja muito difícil.

## Ajustando o bot

### **Por que uns ajustes podem ser necessários?**

O bot usa reconhecimento de imagem para tomar decisões e movimentar o mouse e
clicar nos lugares certos. 
Ele realiza isso comparando uma imagem de exemplo com um screenshot da tela do
computador.
Este método está sujeito a inconsistências devido a diferenças na resolução da
sua tela e de como o jogo é renderizado no seu computador comparado com o
meu(o que usei para pegar as imagens exemplo).
É provável que o bot não funcione 100% logo de cara, e que você precise fazer
alguns ajustes aqui ou ali.

### **Quais sao os problemas?**

* **Falso negativo** - O bot deveria reconhecer uma imagem, por exemplo, o botão de
mandar para trabalhar, mas não reconheceu a imagem na screenshot.

* **Falso positivo** - O bot pensa que reconheceu a imagem que está procurando em um
lugar em que esta imagem não aparece.

Aqui tem uma [lista](#alguns-comportamentos-que-podem-indicar-um-falso-positivo-ou-negativo) de alguns problemas que podem ser ocasionados por falsos
positivos e negativos.

Para resolver estes problemas existem duas possibilidades, a regulagem do
parâmetro “threshold” no arquivo config.yaml ou a substituição da imagem de
exemplo na pasta “targets” para uma tirada no seu próprio computador:

  ### **Threshold na config**

  O parâmetro “threshold” regula o quanto o bot precisa estar confiante para
  considerar que encontrou a imagem que está procurando.
  Este valor de 0 a 1 (0% a 100%).
  Ex:

  Um threshold de 0.1 é muito baixo, ele vai considerar que encontrou a imagem
  que esta procurando em lugares que ela não está aparecendo ( falso positivo ).
  O comportamento mais comum pra esse problema é o bot clicando em lugares
  aleatórios pela tela. 


  Um threshold de 0.99 ou 1 é muito alto, ele não vai encontrar a imagem que
  está procurando, mesmo quando ela estiver aparecendo na tela. O comportamento
  mais comum é ele simplesmente não mover o cursor para lugar nenhum, ou travar
  no meio de um processo, como o de login.

  ### **Substituição da imagem na pasta targets**

  As imagens exemplo são armazenadas na pasta “images/targets”. Estas imagens foram
  tiradas no meu computador e podem estar um pouco diferente da que aparece no
  seu. Para substituir alguma imagem que não esta sendo reconhecida
  propriamente, simplesmente encontre a imagem correspondente na pasta targets,
  tire um screenshot da mesma área e substitua a imagem anterior. É importante
  que a substituta tenha o mesmo nome, incluindo o .png.

### **Alguns comportamentos que podem indicar um falso positivo ou negativo**

#### Falso positivo:

- Repetidamente enviando um herói que já esta trabalhando para trabalhar em um
  loop infinito.
  - Falso positivo na imagem “go-work.png”, o bot acha que esta vendo o botão
    escuro em um herói com o botão claro.

- Clicando em lugares aleatórios(geralmente brancos) na tela
  - Falso positivo na imagem sign-button.png

 
 #### Falso negativo:

- Não fazendo nada
	- Talvez o bot esteja tendo problemas com a sua resolução e não esta
    reconhecendo nenhuma das imagens, tente mudar a configuração do navegador
    para 100%.

- Não enviando os heróis para trabalhar
	- Pode ser um falso negativo na imagem green-bar.png caso a opção
    “select_heroes_mode” estiver como “green”.


### ⚠️ Algumas configuraçoes podem ser mudadas no arquivo config.yaml, nao se esqueça de reiniciar o bot caso mude as configuraçoes.

## 👍 Curtiu? Dê aquela fortalecida :)

### Wallet: 0x29f3f79179C942d227ec38755c0C1Ea4976672C1
