'''
    Nome:       OscTransitorio.py
    Descrição:  
                ALGORITMO DE SUPORTE COM A FINALIDADE DE APLICAR O MÉTODO DA IGUALDADE DE ÁREAS IGUAIS E MÉTODO PASSO-A-PASSO PARA 
                A ESTABILIDADE TRANSITÓRIA DE UM GERADOR SÍNCRONO APÓS O DISTÚRBIO
    Autor:      Jonnathan Alves Ramos
    Disciplina: Dinâmica de Sistemas Elétricos
    Data:       08/10/2021 12:25

    Bibliotecas Externas: 
        • Numpy:      Biblioteca para cálculos de Arrays multidimensionais e numéricos
        • Matplotlib: Biblioteca para plotagem de gráficos
    
    Fontes:
        • Interpolação Polinomial: https://www.unioviedo.es/compnum/labs/PYTHON/Interpolation.html
        • Regressão Linear:        https://numpy.org/doc/stable/reference/generated/numpy.polyfit.html
        • Raízes de um polinômio:  https://numpy.org/doc/stable/reference/generated/numpy.roots.html
'''
import numpy             as np
import matplotlib.pyplot as plt

class gerador:
    '''
        Descrição:  Classe que tem a finalidade de criar um objeto que seus atributos de classe armazenam características de um gerador,
                    como também possui métodos próprios para a simulação da estabilidade transitórios
        Atributos:
            • self.f:                        Frequência                                                  [Hz]
            • self.H:                        Constante de Inércia                                        [s]
            • self.Pm:                       Potência Mecânica                                           [pu]
            • self.Pe_max_antes_disturbio:   Potência elétrica máxima transferível antes do distúrbio    [pu]
            • self.Pe_max_no_disturbio:      Potência elétrica máxima transferível no distúrbio          [pu]
            • self.Pe_max_apos_disturbio:    Potência elétrica máxima transferível após distúrbio        [pu]
            • self._do:                      Ângulo de potência antes do distúrbio                       [°]
            • self._dcc:                     Ângulo de chaveamento crítico                               [°]
            • self._tcc:                     Tempo de chaveamento crítico                                [°]
            • self._df:                      Ângulo de potência estabilizado após o distúrbio            [°]
            • self._dmax:                    Ângulo de potência máximo para a estabilidade               [°]
        Métodos:
            • def __init__(self, **kwargs):                             Inicialização da instância de classe
            • def Metodo_Areas_Iguais(self):                            Calculo do ângulo de chaveamento crítico pelo critério das Áreas Iguais
            • def Metodo_Passo_a_Passo(self, t_chaveamento, dt, tf):    Simulação da curva de oscilação do ângulo de potência pelo tempo
            • def Calculo_tcc(self, dt, tf):                            Calculo do tempo de chaveamento crítico
            • def __str__(self):                                        Printa na tela os dados da instância do gerador
    '''

    def __init__(self, **kwargs):
        '''
            Descrição:              Inicialização da instância de classe
            Atributos (**kwargs):   Dicionário contendo as variáveis OBRIGATÓRIAS a seguir:
                • f                             (float or int)
                • H                             (float or int)
                • Pm                            (float or int)
                • Pe_max_antes_disturbio        (float or int)
                • Pe_max_no_disturbio           (float or int)
                • Pe_max_apos_disturbio         (float or int)
        '''
        self.f                      = kwargs['f']                         
        self.H                      = kwargs['H']                         
        self.Pm                     = kwargs['Pm']                        
        self.Pe_max_antes_disturbio = kwargs['Pe_max_antes_disturbio']    
        self.Pe_max_no_disturbio    = kwargs['Pe_max_no_disturbio']       
        self.Pe_max_apos_disturbio  = kwargs['Pe_max_apos_disturbio']     
        self._do                    = (180/np.pi)*np.arcsin(self.Pm/self.Pe_max_antes_disturbio)   
        self._dcc                   = None
        self._tcc                   = 0
        self._df                    = None
        self._dmax                  = None
    def Metodo_Areas_Iguais(self):
        '''
            Descrição: Método para o cálculo do ângulo de chaveamento crítico pelo método das áreas iguais
        '''
        self._df = (180/np.pi)*np.arcsin(self.Pm/self.Pe_max_apos_disturbio)    
        dmax     = (180 - self._df)*np.pi/180                                   
        do       = self._do*np.pi/180                                           
        # Cálculo do ângulo crítico
        cosdcc  = (self.Pm*(do - dmax) + self.Pe_max_no_disturbio*np.cos(do) - self.Pe_max_apos_disturbio*np.cos(dmax))/(self.Pe_max_no_disturbio - self.Pe_max_apos_disturbio) 
        self._dcc     = (180/np.pi)*np.arccos(cosdcc)                           
        self._dmax    = dmax*(180/np.pi)
    def Metodo_Passo_a_Passo(self, t_chaveamento, dt, tf):
        '''
            Descrição: Simulação da curva de oscilação do ângulo de potência pelo tempo
            Atributos:
                • t_chaveamento:    Tempo que será retirado a falta do sistema elétrico                 (float or int)
                • dt:               Passo de tempo para cada iteração                                   (float or int)
                • tf:               Tempo de simulação final                                            (float or int)
            Retorno:
                • t:                Array de tempo                                                      (float)
                • d:                Array do ângulo de chaveamento                                      (float)
                • pol:              Array dos coeficiêntes do Polinômio característico de 10° ordem     (float)
        '''
        k       = (180*self.f/self.H)*dt**2                      
        t       = np.arange(0, tf+dt, dt)                        
        d       = np.zeros([len(t)])                             
        d[0]    = self._do                                       
        chaveou = False                                          
        ddn     = 0                                              
        t_chaveamento = tf+1 if (t_chaveamento == None) else t_chaveamento
        Pe      = 0
        Pe_max  = 0
        for n in range(0, len(t)):
            if t[n] == 0:
                ## SITUAÇÃO DO SISTEMA NA FALTA
                #  Cálculo logo antes do disturbio
                Pe_max    = self.Pe_max_antes_disturbio                            
                Pe        = Pe_max*np.sin(d[n]*np.pi/180)                          
                Pa        = self.Pm - Pe                                           
                ddn       = ddn + k*Pa                                             
                # Cálculo logo depois do disturbio
                Pe_max    = self.Pe_max_no_disturbio                               
                Pe2       = Pe_max*np.sin(d[n]*np.pi/180)                          
                Pa2       = self.Pm - Pe2                                          
                # Cálculo da média entre os estados antes e após o disturbio
                Pa_med    = (Pa + Pa2)/2                                           
                ddn       = ddn + k*Pa_med                                         
                Pe        = Pe_max*np.sin((d[n] + ddn)*np.pi/180)                  
            elif t[n] >= t_chaveamento and chaveou == False:
                ## SITUAÇÃO DO SISTEMA NA RETIRADA DA FALTA
                #  Cálculo logo antes da retirada da falta
                chaveou   = True                                                   
                Pa        = self.Pm - Pe                                          
                ddn       = ddn + k*Pa                                             
                d[n]      = d[n-1] + ddn                                           
                #  Cálculo logo depois da retirada da falta
                Pe_max    = self.Pe_max_apos_disturbio                             
                Pe2       = Pe_max*np.sin(d[n-1]*np.pi/180)                        
                Pa2       = self.Pm - Pe2                                         
                # Cálculo da média dos estados antes e após da retirada da falta
                Pa_med    = (Pa + Pa2)/2                                           
                ddn       = ddn + k*Pa_med                                         
                Pe        = Pe_max*np.sin((d[n] + ddn)*np.pi/180)                  
            else:
                ## SITUAÇÃO DO SISTEMA QUANDO NÃO HÁ DESCONTINUIDADE
                Pa        = self.Pm - Pe                                                                        
                ddn       = ddn + k*Pa                                             
                d[n]      = d[n-1] + ddn                                           
                Pe        = Pe_max*np.sin((d[n])*np.pi/180)                        
        pol    = np.polyfit(t, d, 10) 
        return t, d, pol               
    def Calculo_tcc(self, dt, tf):
        '''
            Descrição: Cálculo do tempo de chaveamento crítico
            Atributos:
                • dt:               Passo de tempo para cada iteração       (float or int)
                • tf:               Tempo de simulação final                (float or int)
        '''
        self.Metodo_Areas_Iguais()                                                 
        t, d, pol  = self.Metodo_Passo_a_Passo(None, dt, tf)                       
        pol[10]     = pol[10] - self._dcc                                          
        r          = np.roots(pol)                                                 
        r          = list((filter(lambda x: x.imag == 0 and x > 0 and x < tf, r))) 
        try:
            self._tcc = r[0].real                                                  
        except:
            self._tcc = None                                                       
    def __str__(self):
        '''
            Descrição: Printa na tela os dados da instância do gerador
            Retorno:
                • prt: Passo de tempo para cada iteração       (string)
        '''
        prt = '''\t DADOS DO GERADOR
                    f: \t\t\t\t\t{} \t [Hz]
                    H: \t\t\t\t\t{} \t [s]
                    Pm: \t\t\t\t{} \t  pu
                    Pe_max_antes_disturbio: \t\t{} \t  pu
                    Pe_max_no_disturbio: \t\t{} \t  pu
                    Pe_max_apos_disturbio: \t\t{} \t  pu
                    do: \t\t\t\t{:.2f} \t [º]
                    dcc: \t\t\t\t{:.2f} \t [°]
                    df:  \t\t\t\t{:.2f} \t [º]
                    dmax:\t\t\t\t{:.2f} \t [º]
                    tcc: \t\t\t\t{:.2f} \t [s]'''.format(
                                                      self.f, self.H, self.Pm,
                                                      self.Pe_max_antes_disturbio,
                                                      self.Pe_max_no_disturbio,
                                                      self.Pe_max_apos_disturbio,
                                                      self._do,
                                                      self._dcc,
                                                      self._df,
                                                      self._dmax,
                                                      self._tcc
                                                  )
        return prt

def Grafico_Area(gerador):
    '''
        Descrição:  Função de plotagem do gráfico de área do gerador
        Atributos:
            • gerador:    Recebe instância gerador quando é chamado     (class gerador)
    '''    
    angulo        = np.linspace(0, 180, 400)
    Pe_antes_dist = gerador.Pe_max_antes_disturbio*np.sin((np.pi/180)*angulo)
    Pe_no_dist    = gerador.Pe_max_no_disturbio*np.sin((np.pi/180)*angulo)
    Pe_apos_dist  = gerador.Pe_max_apos_disturbio*np.sin((np.pi/180)*angulo)
    Pm_gerador    = gerador.Pm*np.ones(len(angulo))

    anguloInicial = gerador._do
    anguloCritico = gerador._dcc
    anguloMax     = gerador._dmax

    reta_do   = np.linspace(0, Pm_gerador, 10)
    reta_dcc  = np.linspace(0, gerador.Pe_max_apos_disturbio*np.sin(anguloCritico*np.pi/180), 10)
    reta_dmax = np.linspace(0, gerador.Pe_max_apos_disturbio*np.sin(anguloMax*np.pi/180)    , 10)

    reta_PeMax_antes_dist = gerador.Pe_max_antes_disturbio*np.ones(10)
    reta_PeMax_no_dist    = gerador.Pe_max_no_disturbio*np.ones(10)
    reta_PeMax_apos_dist  = gerador.Pe_max_apos_disturbio*np.ones(10)

    plt.plot(angulo, Pe_antes_dist, color = 'green' , label = 'Pe antes')
    plt.plot(angulo, Pe_no_dist   , color = 'yellow', label = 'Pe durante')
    plt.plot(angulo, Pe_apos_dist , color = 'purple', label = 'Pe após')
    plt.plot(angulo, Pm_gerador   , color = 'brown' , label = 'Pm')

    plt.plot(anguloInicial*np.ones(10), reta_do  , '--', color = 'grey', linewidth=.9)
    plt.plot(anguloCritico*np.ones(10), reta_dcc , '--', color = 'black', linewidth=1)
    plt.plot(anguloMax*np.ones(10)    , reta_dmax, '--', color = 'black', linewidth=1)

    plt.plot(np.linspace(0, 90, 10), reta_PeMax_antes_dist, '--', color = 'black', linewidth=1)
    plt.plot(np.linspace(0, 90, 10), reta_PeMax_no_dist   , '--', color = 'black', linewidth=1)
    plt.plot(np.linspace(0, 90, 10), reta_PeMax_apos_dist , '--', color = 'black', linewidth=1)

    plt.text(anguloInicial, 0, 'δo'  , fontsize=12, color='black')
    plt.text(anguloCritico, 0, 'δcc' , fontsize=12, color='black')
    plt.text(anguloMax    , 0, 'δmax', fontsize=12, color='black')

    plt.xlim([0,180])
    plt.ylim([0, gerador.Pe_max_antes_disturbio+.1])
    plt.fill_between(
                        angulo,
                        Pe_no_dist,
                        Pm_gerador,
                        where = (angulo >= anguloInicial) & (angulo <= anguloCritico) & (Pm_gerador >= Pe_no_dist),
                        color = 'r'
                    )
    plt.fill_between(
                        angulo,
                        Pe_apos_dist,
                        Pm_gerador,
                        where = (angulo >= anguloCritico) & (Pe_apos_dist >= Pm_gerador),
                        color = 'b'
                    )
    plt.xlabel('δ[°]')                                                            
    plt.ylabel('Pm [pu]')  
    plt.grid()
    plt.legend()