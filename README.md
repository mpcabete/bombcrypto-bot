Fork do projeto https://github.com/mpcabete/bombcrypto-bot com minhas modificações.

- Alterado forma como o bot executa as ações para detectar primeiro a tela para só depois realizar as operações (evitando processamento desnecessario)
- Corrigido bug de metamask abrir atrás do navagador
- Adicionado interação com telegran (obg @kerferber)
- ~~Adicionado feature para enviar as opções do captcha para o telegram e receber a resposta para proseguir com o processamento do bot (ideia do @testaxb3)~~(11/12/2021)
- Adicionado função para fazer curvas aleatório no mouse para tentar não parecer um robô usando. (10/12/2021)
- Adicionado reconhecimento de imagem para tratar do captcha. (testando ainda...) agradecimento especial ao @Nucito pela disponibilização do CaptchaSolver (11/12/2021)
- Feito correção do botão new map que não estava clicando (12/12/2021 12:34)

** OBS: caso o bot não clique em algum lugar você precisa alterar a imagem correspondente na pasta targets, com certeza vai ter alguma diferença do seu. Por exemplo eu utilizo background escuro e metamask em ingles....**

** É bom gostarem de ler. tem um arquivo LEIAME dentro da pasta train_model com o que precisa fazer.**

Para rodar é necessario instalar o tesseract e apontar o local de instalação, variavel acima no main(). Também pode simplesmentar apagar as referencias do tesseract, caso esteja tendo problemas, e enviar apenas uma print das coins. o tesseract está sendo usado apenas pra ler a imagem e descobrir o saldo de bcoins.
