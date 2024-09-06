# estagio_RoboFEI
Como objetivo deste estágio, minha função era ser introduzido de maneira mais rápida e eficaz possível para ser apto a realizar qualquer função na área de programação, para ajudar a equipe a realizar testes, se preparar para as futuras competições ao longo do ano de 2024 e por fim realizar um projeto que seria futuramente definido.

Inicialmente, como recomendado pelo Cauan Souza capitão da RoboFEI @Home, realizei dois cursos de introdução no site “The construct” denominados “Python 3 for robotics” e “Linux for robotics”. Também assisti alguns vídeos de introdução a ROS enquanto reproduzia o que era ensinado.

Após isso, Souza junto com a integrante Gabriela me introduziram ao sistema do robô HERA, além de me ensinarem a rodar as Tasks (tarefas definidas para as competições) com finalidade de realizar testes, fazer anotações e correções se necessárias ou possíveis.

Alguns dias passados realizando testes e acompanhando o restante da equipe, foi definido junto ao professor Plinio Aquino qual seria o projeto a ser realizado. Sendo ele o desenvolvimento total da tarefa denominada “Stickler for the Rules”, uma Task de segundo estágio da competição Robocup 2024 que seria realizada no mês de julho na Holanda.

Essa tarefa consiste em, o robô ter a função de supervisionar uma festa dentro de uma casa, enquanto anda pelos cômodos e garante que 4 tarefas estejam sendo cumpridas, sendo elas:

No shoes inside the house (Sem calçados dentro de casa) - Caso haja um convidado com calçados dentro da casa, explicar ao convidado a regra, levá-lo até a entrada e solicitar a retirada dos calçados.

Forbidden room (Quarto proibido) - Há um cômodo proibido dentro da casa, caso haja um convidado neste cômodo, explicar ao convidado a regra e levá-lo até o cômodo mais próximo.

No littering (Sem lixo no chão) - Caso haja lixo no chão, identificar o convidado mais próximo ao lixo, explicar ao convidado a regra e pedir para recolher o lixo, e jogá-lo na lata de lixo.

Compulsory hydration (Hidratação compulsória) - Caso algum convidado não esteja segurando uma bebida, explicar ao convidado a regra, levá-lo até a cozinha e solicitar que pegue alguma bebida.

Como orientação do capitão da equipe inicialmente elaborei um arquivo resumo que continha as capacidades necessárias para o robô, uma descrição dissertativa de toda a lógica que seria realizada durante a tarefa e por fim um workflow representando essa mesma lógica. O conteúdo deste arquivo pode ser no visto em <a href="Stickler for the Rules.pdf">Stickler for the Rules</a>.

Em seguida, tive acesso a códigos de Tasks de competições anteriores para estudar, entender melhor como são utilizadas as funções de manipulação, visão e navegação na HERA, e usar como base para realizar meu projeto. Inicialmente estruturei a <a href="codigo_inicial.py">primeira versão</a> do código, onde a lógica desenvolvida anteriormente no arquivo resumo, foi passada para um código de programação efetivo.

Com a finalização do código inicial, o mesmo foi revisado e aprovado pelo Souza. Então em conjunto com ele, fomos modificando e corrigindo o código, adequando-o a uma lógica que fosse mais eficaz considerando o tempo limite para realização da tarefa, foram eliminadas lógicas repetitivas e desnecessárias por funções que ainda não tinha conhecimento, como por exemplo a utilização do predictor junto ao detector para detecção de pessoas, tornando desnecessária a função “for” após o detector para testar todos os objetos e separar as pessoas.

Após diversas mudanças e testes chegamos a uma <a href="codigo_final.py">versão final do código</a> que foi a utilizada na competição, atingindo a maior pontuação da Task entre as equipes da categoria.
