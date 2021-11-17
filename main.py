'''
    Nome:       main.py
    Descrição:  ALGORITMO EXECUTÁVEL COM A FINALIDADE DE APLICAR O MÉTODO DO CRITÉRIOS DA IGUALDADE DE ÁREAS 
                MÉTODO PASSO-A-PASSO PARA A ESTABILIDADE TRANSITÓRIA DE UM GERADOR SÍNCRONO APÓS O DISTÚRBIO
    Autor:      Jonnathan Alves Ramos
    Disciplina: Dinâmica de Sistemas Elétricos
    Data:       09/10/2021 12:25

    Arquivo Externo:
        • OscTransitorio.py
'''

from   OscTransitorio    import *

## CONSTANTES COMUNS AOS GERADORES SÍNCRONOS
tf                     = 1
dt                     = 0.01
f                      = 60
H                      = 5
Pe_max_antes_disturbio = 1.8
Pe_max_no_disturbio    = 0.65
Pe_max_apos_disturbio  = 1.4625

## ESPECIFICAÇÃO E CÁLCULO DO Tcc e Dcc O GERADOR COM Pm = 0.8 pu
geradorPM1 = gerador(
                        f                      = f,
                        H                      = H,
                        Pm                     = 0.8,
                        Pe_max_antes_disturbio = Pe_max_antes_disturbio,
                        Pe_max_no_disturbio    = Pe_max_no_disturbio,
                        Pe_max_apos_disturbio  = Pe_max_apos_disturbio
                    )
geradorPM1.Calculo_tcc(dt, tf)

## ESPECIFICAÇÃO E CÁLCULO DO Tcc e Dcc O GERADOR COM Pm = 0.9 pu
geradorPM2 = gerador(
                        f                      = f,
                        H                      = H,
                        Pm                     = 0.9,
                        Pe_max_antes_disturbio = Pe_max_antes_disturbio,
                        Pe_max_no_disturbio    = Pe_max_no_disturbio,
                        Pe_max_apos_disturbio  = Pe_max_apos_disturbio
                    )
geradorPM2.Calculo_tcc(dt, tf)

## ESPECIFICAÇÃO E CÁLCULO DO Tcc e Dcc O GERADOR COM Pm = 1.0 pu
geradorPM3 = gerador(
                        f                      = f,
                        H                      = H,
                        Pm                     = 1,
                        Pe_max_antes_disturbio = Pe_max_antes_disturbio,
                        Pe_max_no_disturbio    = Pe_max_no_disturbio,
                        Pe_max_apos_disturbio  = Pe_max_apos_disturbio
                    )
geradorPM3.Calculo_tcc(0.01, 1)

## ESPECIFICAÇÃO E CÁLCULO DO Tcc e Dcc O GERADOR COM Pm = 1.1 pu
geradorPM4 = gerador(
                        f                      = f,
                        H                      = H,
                        Pm                     = 1.1,
                        Pe_max_antes_disturbio = Pe_max_antes_disturbio,
                        Pe_max_no_disturbio    = Pe_max_no_disturbio,
                        Pe_max_apos_disturbio  = Pe_max_apos_disturbio
                    )
geradorPM4.Calculo_tcc(dt, tf)

## ESPECIFICAÇÃO E CÁLCULO DO Tcc e Dcc O GERADOR COM Pm = 1.2 pu
geradorPM5 = gerador(
                        f                      = f,
                        H                      = H,
                        Pm                     = 1.2,
                        Pe_max_antes_disturbio = Pe_max_antes_disturbio,
                        Pe_max_no_disturbio    = Pe_max_no_disturbio,
                        Pe_max_apos_disturbio  = Pe_max_apos_disturbio
                    )
geradorPM5.Calculo_tcc(dt, tf)

## DADOS PRINTADOS NO CONSOLE

print('Pm = {}:'.format(geradorPM1.Pm))
print(geradorPM1)
print('Pm = {}:'.format(geradorPM2.Pm))
print(geradorPM2)
print('Pm = {}:'.format(geradorPM3.Pm))
print(geradorPM3)
print('Pm = {}:'.format(geradorPM4.Pm))
print(geradorPM4)
print('Pm = {}:'.format(geradorPM5.Pm))
print(geradorPM5)

## PLOTAGEM DOS GRÁFICOS DE ÁREA DOS GERADORES
plt.figure(1)
Grafico_Area(geradorPM1)
plt.title('Critério da igualdade de áreas com Pm = 0.8') 

#  Gerador 2 (Pm = 0.9 pu)
plt.figure(2)
Grafico_Area(geradorPM2)
plt.title('Critério da igualdade de áreas com Pm = 0.9')

#  Gerador 3 (Pm = 1.0 pu)
plt.figure(3)
Grafico_Area(geradorPM3)
plt.title('Critério da igualdade de áreas com Pm = 1.0') 

#  Gerador 4 (Pm = 1.1 pu)
plt.figure(4)
Grafico_Area(geradorPM4)
plt.title('Critério da igualdade de áreas com Pm = 1.1') 

#  Gerador 5 (Pm = 1.2 pu)
plt.figure(5)
Grafico_Area(geradorPM5)
plt.title('Critério da igualdade de áreas com Pm = 1.2') 

## PLOTAGEM DAS CURVAS DOS ÂNGULOS DE POTÊNCIA DO MÉTODO PASSO A PASSO SEM A RETIRADA DA FALTA
t, plt1, pol1 = geradorPM1.Metodo_Passo_a_Passo(None, dt, tf)
t, plt2, pol2 = geradorPM2.Metodo_Passo_a_Passo(None, dt, tf)
t, plt3, pol3 = geradorPM3.Metodo_Passo_a_Passo(None, dt, tf)
t, plt4, pol4 = geradorPM4.Metodo_Passo_a_Passo(None, dt, tf)
t, plt5, pol5 = geradorPM5.Metodo_Passo_a_Passo(None, dt, tf)

plt.figure(6)
plt.plot(t, plt1, color = 'green' , label = 'Pm = 0.8 pu')
plt.plot(t, plt2, color = 'yellow', label = 'Pm = 0.9 pu')
plt.plot(t, plt3, color = 'purple', label = 'Pm = 1.0 pu')
plt.plot(t, plt4, color = 'brown' , label = 'Pm = 1.1 pu')
plt.plot(t, plt5, color = 'red'   , label = 'Pm = 1.2 pu')
plt.xlim([0, tf])
plt.title('Curvas dos Ângulos de Potência sem a retirada da falta')  
plt.xlabel('t[s]')                                                              
plt.ylabel('δ[°]')  
plt.grid()
plt.legend()

## VARIAÇÃO DO ÂNGULO DE CHAVEAMENTO CRÍTICO E TEMPO DE CHAVEMENTO CRÍTICO EM RELAÇÃO A POTÊNCIA MECÂNICA
p_m  = [geradorPM1.Pm, geradorPM2.Pm, geradorPM3.Pm, geradorPM4.Pm, geradorPM5.Pm]
d_cc = [geradorPM1._dcc, geradorPM2._dcc, geradorPM3._dcc, geradorPM4._dcc, geradorPM5._dcc]
t_cc = [geradorPM1._tcc, geradorPM2._tcc, geradorPM3._tcc, geradorPM4._tcc, geradorPM5._tcc]

pm_plot     = np.linspace(min(p_m) - .1,  max(p_m) + .1, 100)            
pol_dcc     = np.polyfit(p_m, d_cc, 3)                                   
dcc_plot    = np.polyval(pol_dcc, pm_plot)                               
pol_tcc     = np.polyfit(p_m, t_cc, 3)                                   
tcc_plot    = np.polyval(pol_tcc, pm_plot)                               

plt.figure(7)
plt.plot(pm_plot, dcc_plot)
plt.plot(p_m, d_cc, 'ro')
plt.xlim([min(pm_plot), max(pm_plot)])
plt.title('Ângulo de Chaveamento Crítico em relação a Potência Mecânica') 
plt.xlabel('Pm[pu]')                                                              
plt.ylabel('δcc[°]')  
plt.grid()

plt.figure(8)
plt.plot(pm_plot, tcc_plot)
plt.plot(p_m, t_cc, 'ro')
plt.xlim([min(pm_plot), max(pm_plot)])
plt.title('Tempo de Chaveamento Crítico em relação a Potência Mecânica') 
plt.xlabel('Pm[pu]')                                                              
plt.ylabel('tcc[s]')  
plt.grid()

## VARIAÇÃO DAS CURVAS DO ÂNGULO DE CHAVEAMENTO NO TEMPO  EM 0.01 SEGUNDOS ABAIXO DO TEMPO DO CHAVEAMENTO CRÍTICO DE CADA Pm
t, plt1, pol1 = geradorPM1.Metodo_Passo_a_Passo(geradorPM1._tcc - 0.01, dt, tf)
t, plt2, pol2 = geradorPM2.Metodo_Passo_a_Passo(geradorPM2._tcc - 0.01, dt, tf)
t, plt3, pol3 = geradorPM3.Metodo_Passo_a_Passo(geradorPM3._tcc - 0.01, dt, tf)
t, plt4, pol4 = geradorPM4.Metodo_Passo_a_Passo(geradorPM4._tcc - 0.01, dt, tf)
t, plt5, pol5 = geradorPM5.Metodo_Passo_a_Passo(geradorPM5._tcc - 0.01, dt, tf)


plt.figure(9)
plt.plot(t, plt1, color = 'green' , label = 'Pm = 0.8 pu')
plt.plot(t, plt2, color = 'yellow', label = 'Pm = 0.9 pu')
plt.plot(t, plt3, color = 'purple', label = 'Pm = 1.0 pu')
plt.plot(t, plt4, color = 'brown' , label = 'Pm = 1.1 pu')
plt.plot(t, plt5, color = 'red'   , label = 'Pm = 1.2 pu')
plt.xlim([0, tf])
plt.title('Curvas dos Ângulos de Potência em 0.01s antes do chaveamento crítico')  
plt.xlabel('t[s]')                                                              
plt.ylabel('δ[°]')  
plt.grid()
plt.legend()

## VARIAÇÃO DAS CURVAS DO ÂNGULO DE CHAVEAMENTO EM 0.01 SEGUNDOS ACIMA DO TEMPO DO CHAVEAMENTO CRÍTICO DE CADA Pm
t, plt1, pol1 = geradorPM1.Metodo_Passo_a_Passo(geradorPM1._tcc + 0.01, dt, tf)
t, plt2, pol2 = geradorPM2.Metodo_Passo_a_Passo(geradorPM2._tcc + 0.01, dt, tf)
t, plt3, pol3 = geradorPM3.Metodo_Passo_a_Passo(geradorPM3._tcc + 0.01, dt, tf)
t, plt4, pol4 = geradorPM4.Metodo_Passo_a_Passo(geradorPM4._tcc + 0.01, dt, tf)
t, plt5, pol5 = geradorPM5.Metodo_Passo_a_Passo(geradorPM5._tcc + 0.01, dt, tf)

plt.figure(10)
plt.plot(t, plt1, color = 'green' , label = 'Pm = 0.8 pu')
plt.plot(t, plt2, color = 'yellow', label = 'Pm = 0.9 pu')
plt.plot(t, plt3, color = 'purple', label = 'Pm = 1.0 pu')
plt.plot(t, plt4, color = 'brown' , label = 'Pm = 1.1 pu')
plt.plot(t, plt5, color = 'red'   , label = 'Pm = 1.2 pu')
plt.xlim([0, tf])
plt.title('Curvas dos Ângulos de Potência 0.01s após o chaveamento crítico')  
plt.xlabel('t[s]')                                                              
plt.ylabel('δ[°]')  
plt.grid()
plt.legend()

## SALVA OS GRÁFICOS NA PASTA ONDE ESTÁ O SCRIPT (Tirar os comentários para salvar as imagens)

for i in range(1, plt.gcf().number + 1):
    plt.figure(i)
    plt.savefig('fig_{}.png'.format(i))


## MOSTRA OS GRÁFICOS
plt.show()