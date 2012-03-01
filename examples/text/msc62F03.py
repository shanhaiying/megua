#-*- coding: iso-8859-15 -*-
r"""
MSC 62F03   (1980-now) Hypothesis testing


References:
[1] http://www.ams.org/mathscinet/search/mscbrowse.html?pc=62F


AUTHORS:

- Pedro Cruz (2010-04-23): initial version

"""

#*****************************************************************************
#       Copyright (C) 2010 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************

# Main package, ex module
from meg.ex import Exercise,runif,iunif

#Helper functions for MSC 62
from meg.msc62 import *




class E2F03_mean_002(Exercise):
    """
    Teste de Hipóteses, Média, População Normal, teste Bilateral, Variância Desconhecida. 
    Pequena amostra fornecida. Caso de rejeição. Método da Região Crítica (Região de Rejeição).

    Authors:
    - Pedro Cruz (2010) initial version

    """

    def make_random(self,seed):
        #Call base class function
        Exercise.make_random(self,seed)

        # Data Generation
        # Case of rejection
        #Test value
        self.inAlpha = random_alpha_01()
        #Sample
        self.inN = iunif(5,10)
        self.inAmostra = r.rnorm(self.inN,10,20)._sage_() #diminuir nr casas decimais
        
    

        #Significance Level
        d = iunif(0,2)
        if d==0:
            self.inAlphaPercent = 1
        elif d==1:
            self.inAlphaPercent = 5
        else:
            self.inAlphaPercent = 10


    def solve(self):
        r"""
        Solves it!

        Examples:
        ::
            sage: stat_th_000 = StatTH000()
            sage: stat_th_000.make_random(10)
            sage: print stat_th_000
            {'inSampleMean': 4.54, 'inSize': 10, 'inTestValue': 4.5, 'inSampleStDevC': 0.18, 'inAlphaPercent': 5}
            sage: stat_th_000.solve()
            sage: print stat_th_000
            {'otBilatPerc': '97.5', 'inTestValue': 4.5, 'inSampleMean': 4.54, 'inAlphaPercent': 5, 'ontObs': 0.7027, 'onPopStDev': 0.25, 'inSize': 10, 'onFreedom': 9, 'ontCritical': 2.2622, 'inSampleStDevC': 0.18, 'onReject': False}

        """
        #Call base class
        Exercise.solve(self)
        #Checks
        #    
        #Solve
        self.onAlpha        = RDF(self.inAlphaPercent)/100.0
        self.ontCritical = fround(r.qt(1-self.onAlpha/2.0,self.inSize-1),4) #4 digits at right
        self.ontObs = fround( (self.inSampleMean-self.inTestValue) * sqrt(self.inSize) / self.inSampleStDevC,4 )
        self.onReject = abs(self.ontObs) > self.ontCritical

        #self.ex_dict["onPopStDev"]=self.onPopStDev
        #self.ex_dict["ontCritical"] = self.ontCritical
        #self.ex_dict["ontObs"] = self.ontObs
        #self.ex_dict["onReject"] = self.onReject
        #self.ex_dict["otBilatPerc"] = Percent(1-self.onAlpha/2.0)
        #self.ex_dict["onFreedom"] = self.inSize-1
        self.otBilatPerc = Percent(1-self.onAlpha/2.0)


e2F03_mean_002 = E2F03_mean_002('e2F03_mean_002') 




# ===
# End
# ===

