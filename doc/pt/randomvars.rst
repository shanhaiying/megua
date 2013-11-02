

.. _randomvars:

.. `yahoo <http://yahoo.com>`_


Valores e objetos aleatórios
============================

Esta secção é sobre a geração aleatória de valores. 
Não há uma única maneira de criar valores ou objectos aleatórios em virtude da multiplicidade de bibliotecas e domínios. 
Apresenta-se neste texto uma lista de possibilidades entre várias. A lista apresenta algumas funções das seguintes bibliotecas:

* módulo **ur** (conjunto de rotinas que fazem parte do MEGUA);
* funções das bibliotecas **Sage** Mathematics;
* funções da biblioteca ``random`` escrita para a linguagem **Python**;


A biblioteca :doc:`Unified Random <ur>` que "gere" a criação de números aleatórios e pode contem informação adicional que não está nesta página.



Inteiros
--------


**MEGUA** - Biblioteca `Unified Random <ur>`_

.. function::  ur.iunif(a,b)

   Retorna um inteiro aleatório *N* tal que ``a <= N <= b`` (a partir da distribuição uniforme).


::

   sage: ur.iunif(1,11)
   11


.. function::  ur.iunif_nonset(a,b,nonset)

   Retorna um inteiro aleatório *N* tal que ``a <= N <= b`` e *N* não esteja em ``nonset``.


::

   sage: ur.iunif_nonset(-11,11,[-1,0,1])
   -2




**Sage**  - Biblioteca `Integer Ring <http://www.sagemath.org/doc/reference/rings_standard/sage/rings/integer_ring.html>`_

.. function:: ZZ.random_element(a,b)

   Retorna um inteiro aleatório *N* tal que ``a <= N < b`` (a partir da distribuição uniforme).

:: 

   sage: ZZ.random_element(1,11) #random integer in [1,11[ (open at right)
   10


**Python**  - Biblioteca `random <http://docs.python.org/2/library/random.html>`_

.. function:: random.randint(a, b)

   Retorna um inteiro aleatório *N* tal que ``a <= N <= b`` (a partir da distribuição uniforme).

::

   sage: random.randint(1,11)
   11


 
Reais
-----

**MEGUA** - Biblioteca `Unified Random <ur>`_

.. function::  ur.runif(a,b,prec)

   Retorna um número real aleatório *N* tal que ``a <= N <= b`` (a partir da distribuição uniforme) em que a parte decimal tem ``prec`` casas decimais. 

::

   sage: ur.runif(1,11,2)
   9.12



**Sage**  - Biblioteca `Double Precision Real Numbers <http://www.sagemath.org/doc/reference/rings_numerical/sage/rings/real_double.html>`_

.. function:: RDF.random_element(min=-1, max=1)

   Retorna um real aleatório *N* com a "precisão dupla" tal que ``a < N < b``.
   Se não forem passados os argumentos min e max então são considerados os valores -1 e 1.

::

   sage: RDF.random_element()
   -0.37186974842


A biblioteca `Arbitrary Precision Real Numbers <http://www.sagemath.org/doc/reference/rings_numerical/sage/rings/real_mpfr.html>`_ fornece outra maneira.

Na seguinte instrução ``RealField(15)`` a precisão é de 15 bits o que equivale, aproximadamente, a números de 4 algarismos:

:: 

   sage: RealField(15).random_element() #entre -1 e 1
   -0.5366
   sage: RealField(15).random_element(20,30) #entre 20 e 30
   27.17


**Python**  - Biblioteca `random <http://docs.python.org/2/library/random.html>`_

.. function:: random.uniform(a, b)

   Retorna um real aleatório *R* tal que ``a <= R <= b`` quando  ``a <= b`` e ``b <= N <= a`` quando ``b < a``.
   (usa a precisão máxima da máquina)

::

   sage: random.uniform(1,3)
   1.1344190566690746



Listas (ou sequências)
----------------------


**MEGUA** - Biblioteca `Unified Random <ur>`_

.. function::  ur.random_element(lista)

   Retorna um elemento ao acaso da lista.



**Python**  - Biblioteca `random <http://docs.python.org/2/library/random.html>`_

.. function:: random.choice(seq)

   Retorna um elemento da lista (ou sequência) *seq* se não for vazia. Se *seq* for uma lista vazia ocorre o erro :exc:`IndexError`.


::
    
   sage: random.choice( 'a','b','c')
   'b'
   sage: random.choice( [exp(1),sin(1),sqrt(2)] )
   sin(1)




