
"""
 MSC 62F03

 Pedro Cruz

Usage 1:
    sage E62F03_mean_001.sage

Usage 2:
    $ sage
    sage: attach E62F03_mean_001.sage
     - - edit E62F03_mean_001.sage - -
    sage: enter

"""

#Load meg library
from meg.all import *

meg_store.defaults('pt_pt','latex')


latex_template = r"""
%PROBLEM

% Teste de Hipóteses, Média, População Normal, teste Bilateral, Variância Desconhecida. Pequena amostra fornecida. 
% Caso de rejeição. Método da Região Crítica.

Admite-se que a quantidade de nicotina (medida em mg) existente num cigarro de determinada marca tem distribuição Normal.
Observaram-se $ N@ $ cigarros da referida marca tendo-se retirado a seguinte amostra
\[
  onAmostra
\]
Teste, ao nível de $\alpha=inAlpha$, as hipóteses
\[
H_0:\, \mu=inMu@ \quad\text{vs}\quad H_1:\, \mu\neq inMu@
\]
usando o Método da Região Crítica.


%ANSWER


Temos que $X\frown N(\mu,\sigma^2)$ onde os parâmetros da média populacional $\mu$ e variância $\sigma^2$ são desconhecidos.
Então podemos usar a seguinte relação
\[
T=\frac{\bar X - \mu}{S_c/\sqrt n} \,|\, H_0 \frown t_{n-1}
\]
em que $t_{n-1}$ designa a distribuição t-student com $n-1$ graus de liberdade.
Em virtude da hipótese alternativa $H_1$ ser uma desigualdade então a 
região crítica é bilateral e fica definida por:
\[
RC= ]-\infty,t_{\alpha/2,n-1}[ \cup ]t_{1-\alpha/2,n-1},+\infty[
\]
Pela simetria da distribuição t-student temos
$t_{\alpha/2,n-1} = - t_{1-\alpha/2,n-1}$
e consultando uma tabela ou calculadora $t_{1-\alpha/2,n-1} = t_{onRightAlpha,onN1} = onTcrit$.
A região crítica fica assim definida por:
\[
RC= ]-\infty,-onTcrit[ \cup ]+onTcrit,+\infty[
\]
Vamos agora verificar se o valor da estatística de teste $T$ está em RC.
Com base na amostra calculamos o valor das estatísticas:
\begin{itemize}
\item $\displaystyle \bar x=(1/n)\sum_{i=1}^n x_i=onSMean$ 
\item $\displaystyle s_c=(1/(n-1))\sum_{i=1}^n (x_i-\bar x)^2=onSDev$
\end{itemize}
de onde
\[
t_{obs} = \frac{\bar x - \mu}{s_c/\sqrt n} = onTobs
\]
Em virtude de $t_{obs} \in$RC temos razões para rejeitar que $H_0\,:\,\mu = inMu$.
"""




class E62F03_mean_001(Exercise):
    """
    Create an exercise for testing hipotheses for mean based on t-student distribution.

    Authors:
    - Pedro Cruz (2010) initial version

    """

    #This below forces the class to be stored and not only the instance.
    _template = latex_template

    def make_random(self,seed):
        #Call base class function
        Exercise.make_random(self,seed)

        # Data Generation        #Test value
        self.inTestValue = runif(2,7,1) #population mean
        self.onPopStDev = runif(RDF(0.05),RDF(0.7),2) #population stdev 
        #Sample
        self.inSize = iunif(5,16)
          # $\bar x \frown N(\mu, \sigma^2/n)$
        self.inSampleMean = rnorm(self.inTestValue,self.onPopStDev / sqrt(self.inSize),2)
        if self.inSampleMean == self.inTestValue:
            self.inSampleMean = self.inSampleMean*RDF(1.01) # imagination! This must be checked.
            
        self.inSampleStDevC = runif( self.onPopStDev/RDF(2.0), RDF(3.0)*self.onPopStDev/RDF(2.0), 2)

        #Significance Level
        d = iunif(0,2)
        if d==0:
            self.inAlphaPercent = 1
        elif d==1:
            self.inAlphaPercent = 5
        else:
            self.inAlphaPercent = 10


    def solve(self):
        #Call base class
        Exercise.solve(self)
        #Checks
        #    
        #Solve
        self.onAlpha     = RDF(self.inAlphaPercent)/100.0
        self.ontCritical = fround(r.qt(1-self.onAlpha/2.0,self.inSize-1),4) #4 digits at right
        self.ontObs = fround( (self.inSampleMean-self.inTestValue) * sqrt(self.inSize) / self.inSampleStDevC,4 )
        self.onReject = abs(self.ontObs) > self.ontCritical

        self.otBilatPerc = Percent(1-self.onAlpha/2.0)



#For tests
exerc_gen_instance = E62F03_mean_001()


#Creates an instance from E62F03_mean_001 and store the CLASS bytecode on the database.
#The instance does not contain the _template so it's useless to store it.
meg_store.save( E62F03_mean_001 )


exer = meg_store.get( E62F03_mean_001 )


print exer.random_instance()



