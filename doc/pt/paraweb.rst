


Exercícios para a web
=====================



A estrutura dum exercício para a web (siacua ou moodle) é  seguinte:

::

   %summary Secção; Subsecção ; Subsubsecção

   Texto que descreve o exercício, catalogação e autoria.

   %problem Um Nome Sugestivo

   O problema parameterizado.
 
   %answer    

   BLOCO DE ESCOLHA MÚLTIPLA

   RESPOSTA COMPLETA

   class nome_do_exercicio(Exercise):

   <4 espaços> def make_random(s):

   <4 espaços> def solve(s):



O "BLOCO DE ESCOLHA MÚLTIPLA" tem (agora) a seguinte sintaxe:

.. code-block:: xml

   <multiplechoice>
   <choice> $$vresposta$$ </choice>
   <choice> $$errada1$$ </choice>
   <choice> $$errada2$$ </choice>
   <choice> $$errada3$$ </choice>
   </multiplechoice>


com qualquer número de <choice> e em que a primeira é sempre a única correta!

A "RESPOSTA COMPLETA" é todo o texto que ocorre depois do bloco de escolha múltipla.


Exercício Completo
------------------

Ilustra-se agora um exercício completo para escolha múltipla:

::

    %summary Demonstração; Escolha múltipla     

    Comandos para selecionar texto a apresentar.
    Não se consideram todos os casos neste exercício de demonstração.

     
    %problem Exemplo 

    O resultado de $av/bv$ é:

    %answer

    <multiplechoice>
    <choice> $$vresposta$$ </choice>
    <choice> $$errada1$$ </choice>
    <choice> $$errada2$$ </choice>
    <choice> $$errada3$$ </choice>
    </multiplechoice>

    A resposta é $vresposta$. Faltaria detalhar os passos de uma divisão para esta resposta ficar completa.

.. code-block:: python

    class E12X34_numeros_001(Exercise):
        
        def make_random(s):
            s.av = ur.iunif(1,10)
            s.bv = ur.iunif(20,30)
        def solve(s):
            s.vresposta= (s.av / s.bv).n(digits=3) #arredonda a parte decimal a 3 algarismos.
            #Opções Erradas
            s.errada1 = s.vresposta*0.9
            s.errada2 = s.vresposta*1.2
            s.errada3 = s.vresposta*1.3





Escolha de texto
----------------

Suponha que quer escrever uma de duas frases na resolução detalhada ou outra parte do exercício:

* o limite não existe.
* o limite existe e o seu valor é $valor$.

Para estes casos, ou outros com mais hipóteses, veja o seguinte exemplo que utiliza a seguinte sintaxe:


.. code-block:: html

   <showone variavel>
    <thisone Caso sem limite  - isto é comentário>
        O limite não existe.
    </thisone>
    <thisone Caso em que o limite existe - isto é comentário>    
        O limite existe e o seu valor é \$valor\$.
    </thisone>
   </showone>


.. code-block:: python

    class E12X34................
        s.variavel = 0 ou 1 para decidir sobre o limite.



Gráficos
--------


Consideramos duas tecnologias para os gráficos:

* LaTeX e o pacote TikZ
* Gráficos do Sage Mathematics


Para utilizar os **gráficos do Sage** considere as duas etapas seguintes.

1. Em qualquer parte do texto coloque o nome do gráfico, por exemplo centrado:

.. code-block:: html

   <center>
   fig1
   </center>

2. Na parte da programação (make_random ou solve) faça:

.. code-block:: python

   s.param1 = ur.iunif(1,5) #um possível parâmetro.
   g1 = plot(sin(s.param1*x),x, color='blue')
   g2 = plot(cos(s.param1*x),x, color='red') 
   s.fig1 = s.sage_graphic( g1+g2, "fig1", dimx=7, dimy=7) #7cm

Desta maneira será produzido um gráfico parameterizado. 

Pode-se encontrar infomação sobre gráficos em Sage aqui:

* `Plot 2d <http://www.sagemath.org/doc/reference/plotting/index.html>`_: gráficos de funções e construções gráficas;
* `Plot 3d <http://www.sagemath.org/doc/reference/plot3d/index.html>`_: o mesmo para 3d.



Para utilizar o **LaTeX** procede-se em dois passos.

1. Na parte do texto (%problem ou %answer ou opções) coloque:

::

   <latex 100%>
      COMANDOS LATEX OU COMANDOS TIKZ
      que possivelmente dependam de parâmetros.
   </latex>

2. Na parte da programação dar valores ao parâmetros (como habitual, isto é, não é necessário chamar nenhum comando especial).

O valor 100% indica que o desenho aparece na escala normal mas pode ser modificado, aumentando ou reduzindo, sendo que estas transformações podem sempre piorar um pouco a qualidade.

Qualquer comando normal de LaTeX pode ser usado (incluindo uma demonstração inteira) ou então podem ser usados pacotes gráficos como é o caso do 
`Tikz <http://paws.wcu.edu/tsfoguel/tikzpgfmanual.pdf>`_  . Outra maneira de usar o TikZ é construir gráficos no Geogebra e exportar em TikZ para
o exercício.

Este é um caso:

.. code-block:: latex


    \definecolor{qqqqcc}{rgb}{0,0,0.8}
    \definecolor{qqqqff}{rgb}{0,0,1}
    \definecolor{ccqqqq}{rgb}{0.8,0,0}
    \definecolor{ttzzqq}{rgb}{0.2,0.6,0}

    \begin{tikzpicture}[line cap=round,line join=round,>=triangle 45,x=unx1@f{f}cm,y=uny1@f{f}cm]


    \draw[->,color=black] (v11@f{f},0) -- (v21@f{f},0) node [anchor=north east] { $x$};
    \foreach \x in {}
    \draw[shift={(\x,0)},color=black] (0pt,2pt) -- (0pt,-2pt) node[right,above] {\footnotesize $x$};
    \draw[->,color=black] (0,v12@f{f}) -- (0,v22@f{f}) node [anchor=north east] {$ y$};
    \draw[color=black] (0pt,-5pt) node[left] {\footnotesize $0$};


    \clip(v11@f{f},v12@f{f}) rectangle (v21@f{f},v22@f{f});

    \draw[color=ttzzqq,line width=1.2pt,smooth,samples=100,domain=ext1@f{f}:ext2@f{f}] plot(\x,{a1+b1/((1*\x)+d1)});
    \draw[color=qqqqcc,line width=1pt,smooth,samples=100,domain=ext1@f{f}:ext2@f{f}] plot(\x,{slopes1@f{f}*(\x-ix0)+iy0@f{f}});
    \draw[color=ccqqqq,line width=1pt,smooth,samples=100,domain=ext1@f{f}:ext2@f{f}] plot(\x,{slopet1@f{f}*(\x-ix0)+iy0@f{f}});

    \begin{scriptsize}
    \fill [color=qqqqff] (ix0,iy0@f{f}) circle (1.5pt);
    \draw[color=qqqqff] (labelA1,iy0@f{f}) node[left,below] {$A$};
    \fill [color=qqqqff] (ix1,iy1@f{f}) circle (1.5pt);
    \draw[color=qqqqff] (ix1,iy1@f{f}) node[right,above] {$B$};
    \end{scriptsize}
    \end{tikzpicture}

Neste exemplo acima, existem imensos parâmetros, dado que a figura resultante é complexa. São exemplos: *v11@f{f}* em que @f{f} arredonda o número,
ou então *ix0* ou ainda *labelA1*.

ou uma tabela em LaTeX pode ser também convertida numa imagem:

.. code-block:: latex

    \begin{tabular}{c|c|c}
    \hline
    par1 & par2 & par3 \\
    \hline
    \end{tabular}

em que *par1*, *par2*, e *par3* são parâmetros a serem calculados na parte da programação.



