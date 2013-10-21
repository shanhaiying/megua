

Guia Rápido
===========


Este é um guia das etapas principais para a construção de um exercício parameterizado.

Começar com a ideia teórica do exercício:

1. Escrever o problema e seus parâmetros.
2. Escrever de imediato a resolução completa baseada nos parâmetros definidos no problema.
3. Só depois as opções de escolha múltipla (se estiver a escrever para a web).



Após a etapa teórica, vem a criação de um novo exercício no servidor:

1. Aceda ao site `megua.org <http://www.megua.org>`_ e faça *login*; usar o chrome ou firefox preferencialmente; se é docente e pretende um login contacte `Pedro Cruz <http://www.ua.pt/dmat/pageperson.aspx?id=1183>`_.
2. Abrir um qualquer exercício que já exista na sua conta;
3. Faça ``File Copy Worksheet``;
4. Mude o nome (click no nome). Se é aluno de mestrado a sugestão do nome é Mestrado:seuprimeironome_001
5. Faça ``share`` (botão no canto superior direito) com os utilizadores do projeto em que está.

Depois:

1. Alterar secções em ``%summary ....``, escrever um sumário do que é o exercício e catalogar (ver abaixo).
2. Criar problema (e seus parâmetros) em ``%problem <nome sugestivo para o estudante>``.
3. Alterar nome do exercício usando um formato análogo a ``class E97H60_determinantes_001`` em que 97H60 deve ser escolhido da MSC (ver abaixo).
4. Criar resolução completa (e seus parâmetros) em ``%answer``.


Informação extra resumida (vendo o worksheet apenas):

1. make_random: cria valores para a parte do problema
2. solve: calcula valores para a resolução e opções de escolha múltipla
3. shift enter: avalia e grava se não existirem erros
4. Click no link que diz HTML

Documentação sobre o Sage:

http://www.sagemath.org/help.html#SageStandardDoc



Mathematics Subject Classification
----------------------------------

Os exercícios devem ser catalogados com o sistema de classificação para a matemática conhecido por 
*Mathematics Subject Classification* (MSC2010). Pode usar-se mais que uma área mas uma delas deverá ser a principal.

Para a criação de material educativo é normal que a principal área esteja dentro nesta classe::

  97-XX Mathematics education

dentro da qual se encontram os domínios principais para os quais se pretendem desenvolver exercícios.

A classificação completa encontra-se em `msc2010.org <http://msc2010.org/mscwiki/index.php?title=MSC2010>`_.




