Salve familia, n sei q q ta rolando nesse chat maluco ai pq tava trabalhando no bot. Consegui fazer funcionar, to mto feliz!!!
Eu ainda preciso resolver uns probleminhas pra ele ficar mais consistente, vou dar um tempinho aqui e mais tarde volto a programar.
Quem quiser testar ele ta upado pra branch puzzle
Essa versao do bot eu tirei todo o codigo e deixei só o de resolver o capcha, pra testar vc inicia ele com o capcha na tela já
Eu tive q dar esses 2 comandos aqui:

pip uninstall opencv-python pip install --upgrade opencv-python==4.5.3.56

Essa madruga sepa ja consigo arrumar os ultimos detalhes e dar o merge!

Se algum dev quiser brincar ai axo q tem umas função "show" comentada q se vc
descomentar ele vai mostrar o q o bot ta vendo na hora.
O probleminha que tenho que resolver eh que as vezes o bot, enquanto esta
procurando a pecinha cinza acaba "entendendo" que o espaço em branco é a
pecinha, preciso ver um jeito de ou tirar os espaços em brancos da imagem
recortada, ou fazer um check pra ver se o que ele encontrou esta em branco.

