Departamento de Informática e Estatística
Curso de Sistemas de Informação
Disciplina de Sistemas Inteligentes
Profa. Nathalia da Cruz Alves
Trabalho Prático 1 - Métodos de Busca
O propósito do trabalho é implementar o algoritmo de busca A* e UCS e analisar
experimentalmente seu funcionamento em um problema de busca escolhido pela
equipe. O problema ou jogo a ser utilizado é de tema livre e deve ser adequado à
aplicação de algoritmos de busca e permitir a implementação e comparação das
diferentes estratégias solicitadas neste trabalho. A equipe deverá escolher um
problema no qual seja possível definir claramente:
● O espaço de estados.
● O estado inicial.
● O estado ou condição objetivo.
● As ações/movimentos possíveis.
Recomenda-se que o problema escolhido possua escopo e complexidade semelhantes
aos de problemas clássicos de busca em espaço de estados. O problema não precisa
ser um quebra-cabeça, mas deverá possuir um espaço de estados suficientemente
grande para que seja possível observar diferenças de desempenho entre UCS e as
diferentes versões do A*.
Entregáveis
A1. Arquivo de implementação (.ipynb)
A implementação deverá ser desenvolvida em um Jupyter Notebook. O notebook
deverá permitir a execução dos algoritmos UCS e A* a partir de uma configuração
inicial do problema e deverá apresentar de forma clara os resultados obtidos.
Sugere-se utilizar como base o material disponibilizado nas aulas práticas. O notebook
deverá conter:
A1.1 Células de texto contendo o nome dos estudantes (incluindo uma frase
descrevendo a contribuição de cada um para o trabalho), explicação do
problema escolhido com a descrição do espaço de estados, estado inicial,
estado ou condição objetivo e ações/movimentos possíveis.
A1.2 Células de código com a implementação dos algoritmos:
a. UCS - Busca de Custo Uniforme, sem heurística.
b. A* com uma heurística não admissível.
c. A* com uma heurística admissível (sem ser h=0).
d. Desafio opcional (1 ponto extra): implementar o A* utilizando uma
heurística admissível e consistente mais precisa que a heurística
admissível obrigatória.
A1.3 Saídas das células de código apresentando a solução encontrada, ou
seja, o menor caminho ou a sequência de ações necessária para atingir o
objetivo, quando o algoritmo utilizado garantir uma solução ótima. Ao final de
cada execução, deverá também ser apresentado: (A) Total de nodos visitados;
(B) Tamanho do caminho/solução; (C) Tempo de execução, em segundos; (D)
Maior tamanho da fronteira durante a execução.
A2. Vídeo de apresentação: o vídeo deverá ser entregue por meio de um link
disponibilizado no Youtube ou Google Drive. A duração deve ser de, no máximo, 8
minutos explicando brevemente:
A2.1 O problema ou jogo utilizado, incluindo o espaço de estados, estado
inicial, estado ou condição objetivo e as ações/movimentos possíveis.
A2.2 Quais os métodos ou funções principais e suas relações com o algoritmo
A*, incluindo como foi gerenciada a fronteira, ou seja, quais verificações foram
feitas antes de adicionar um estado na fronteira (explicar e mostrar os
respectivos trechos de código).
A2.3 Descrição das heurísticas e comparação da faixa de valores e da
precisão delas com um caso fácil e um difícil.
A2.4 Breve análise do desempenho da implementação com uma tabela
comparativa usando as informações da saída (especificados conforme os itens A
a D de A1.3) das variações implementadas com exatamente os mesmo casos.
Caso tenha sido utilizado algum referencial teórico ou prático, o mesmo deverá ser
informado (incluindo-se repositórios, e quaisquer códigos-fonte). Recomenda-se que
utilizem ferramentas de IA generativas apenas para auxiliar na pesquisa, nesse caso,
também citem qual ferramenta foi utilizada e para qual finalidade. Importante: a
avaliação considera todo o trabalho realizado, não apenas uma saída correta.
Se for detectado plágio de qualquer forma ou o trabalho apresente uso de IA excessivo,
todos os envolvidos receberão nota 0 e não será possível entregar o trabalho
novamente. Além disso, o fato será avisado à coordenação do curso.
O trabalho foi planejado para ser desenvolvido por grupos de 2 a 3 estudantes.
Prazo para entrega: 27/09/2026
Temas-exemplos
1. Puzzles e quebra-cabeças
a. Pocket Cube
b. 15-puzzle
c. Lights Out
d. Torre de Hanói
e. Jarras de água
f. Outros puzzles de estados discretos
2. Navegação
a. Labirinto em uma matriz
b. Robô em um mapa
c. Personagem em uma dungeon
d. Navegação em uma cidade simplificada
e. Navegação em um edifício
f. Outros tipos de exploração de ambientes
3. Planejamento
a. Organização de caixas em um depósito
b. Organização de produtos em prateleiras
c. Empilhamento de objetos
d. Organização de livros
e. Outros problemas de planejamento
Observação: O trabalho não tem como objetivo desenvolver um jogo completo, o jogo ou
problema escolhido deve servir como domínio para a implementação e análise dos algoritmos
de busca.