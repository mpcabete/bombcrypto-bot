Fork do projeto https://github.com/mpcabete/bombcrypto-bot com minhas modificações.

- Alterado forma como o bot executa as ações para detectar primeiro a tela para só depois realizar as operações (evitando processamento desnecessario)
- Corrigido bug de metamask abrir atrás do navagador
- Adicionado interação com telegran (obg @kerferber)
- Adicionado feature para enviar as opções do captcha para o telegram e receber a resposta para proseguir com o processamento do bot (ideia do @testaxb3)


Para rodar é necessario instalar o tesseract e apontar o local de instalação, variavel acima no main(). Também pode simplesmentar apagar as referencias do tesseract, caso esteja tendo problemas, e enviar apenas uma print das coins. o tesseract está sendo usado apenas pra ler a imagem e descobrir o saldo de bcoins.

quem for analisar o código me desculpa pelo uso de português e inglês alternando entre os dois, no nome das variaveis e comentários. Conforme o cansaço vai batendo eu vou virando grindo e depois volto a ser br. É intermitente (programador sabe como que é).
