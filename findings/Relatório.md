# Research em Especificação Incorreta

### Introdução:

Neste trabalho elaboramos uma pesquisa sobre especificação incorreta de matrizes de covariância e o impacto sobre portfólios baseados em risco.
A primeira classe destes portfólios foram os baseados em métodos convexos de otimização: 

- Equal Risk contribution
- Inverse Variance
- Maximum Decorrelation
- Maximum Diversification
- Minimum volatility

Já a segunda classe de portfólios é a baseada em métodos de clusterização:
- Hierarchical Equal Risk Contribution
- Hierarchical Risk Parity

Lopez de Prado (2018) alerta  que os portfólios baseados em métodos convexos sofrem pela falta de estabilidade devido ao número de condição da matriz de covariâncias. 
Este número aumenta na medida que cresce o número de ativos correlacionados na carteira do gestor. Implicando que a inversa da matriz de covariâncias torna-se instável, o que acarreta em erros de estimação nos pesos do portfólio. O autor denominou este fato de a maldição de Markowitz, dado que um alto grau correlação nos investimentos,
mais diversificação se faz necessária  conduzindo a maiores erros de estimação.

Por outro lado, autores  como Jain *et al.*(2019) e Ardia *et al.*(2017)  têm alertado para a quantificação do risco da especificação incorreta da matriz de covariâncias em portfólios que são baseados em risco. O que pode incorrer em portfólios totalmente diferentes daqueles objetivados quando utiliza-se métodos baseados em matriz de covariâncias.

Os métodos ERC e HRP foram avaliados no trabalho de  Jaeger *et al.*(2020), os autores fizeram uma regressão `xgboost` para explicar o spread  *Calmar Ratio (HRP) - Calmar Ration (ERC)*.  E concluiram  heterogeneidade dos *drawdowns*  dos ativos de maior risco do portfólio fortaleciam o HRP.
Já o ERC depende mais da correlação negativa entre os instrumentos de renda fixa e de maior volatilidade na carteira.



### Metodologia 

A verificação da sensibilidade foi feita através do experimento de Monte Carlo. Esta é uma técnica bastante utilizada quando desejamos avaliar propriedades de estimadores como viés, variância, eficiência assintótica e etc. A primeira parte do estudo que é relativa  a estimação e simulação do GARCH-DCC foi feita utilizando a linguagem `R`com o pacote `rmgarch`. Em `Python` fizemos o cálculo dos pesos dos portfólios sob cada especificação da matriz de covariâncias e também o cálculo dos erros.

Os estimadores da Matriz de covariâncias:

- *SAMPLE* : Baseado nas covariâncias amostrais entre cada classe de ativo.
-  *EWMA*: Exponential weighted moving average (EWMA) é um modelo que estima a covâriância dando ponderação maior para as observações mais recentes.
-  *GARCH-DCC*: Modelo introdudzido por Engle (2002), amplamente utilizado como processo gerador de ativos correlacionados  e com variância condicional. Nesta modelagem tanto a volatilidade quanto a correlação das classes de ativos são variantes no tempo. 



A rotina computacional para a avaliação da sensibilidade foi feita como segue:

- Ajustamos/Calibramos o GARCH-DCC para as 12 classes de ativos que compõe a carteira da Solaris;
- Simulamos 1717 observações de cada ativo da nossa carteira;
- Calculamos a covariância verdadeira baseada nas 1717 observações geradas anteriormente;
- Calculamos a covariância amostral com 1716 observações simuladas;
- Ajustamos um GARCH-DCC com 1716 observações simuladas e fazemos a previsão para T+1;
- Calculamos a covariância EMWA com 1716 observações simuladas;
- Computamos os pesos do portfólio verdadeiro para cada um dos 7 métodos estudados;
- Computamos os pesos do portfólio utilizando o estimador amostral;
- Computamos os pesos do portfólio utilizando o GARCH-DCC;
- Computamos os pesos do portfólio utilizando a EWMA;
- Computamos o erro/distância dos portfólios sob cada matriz de covariância estimada para o portfólio verdadeiro;
- **Repetimos os passos acima 1000 vezes**.

A métrica de erro utilizada para computar as distâncias entre o portfólio verdadeiro e os estimados sob cada matriz de covariâncias foi a norma L-1:

![error](error.png)



### Discussão e Análise de Resultados  

A seguir plotamos  os box-plots para cada erro em  obtido em cada uma das 1000 réplicas de Monte Carlo sob cada especificação da matriz de covariâncias.

![Boxplot](box_plot.png)

Destaca-se a variabilidade dos erros dos métodos HERC, máxima descorrelação e máxima diversificação.

|Erro Computado|  Mediana | 
|--------------|--------:|
|ERC_EWMA|0.10|
|**ERC_DCC**|**0.02**|
|ERC_SAMPLE|0.15|
|MAXDEC_EWMA|0.52|
|**MAXDEC_DCC**|**0.13**|
|MAXDEC_SAMPLE|0.27|
|MAXDIV_EWMA| 0.58|
|**MAXDIV_DCC**|**0.19**|
|MAXDIV_SAMPLE|0.40|
|INVVOL_EWMA|0.02|
|**INVVOL_DCC**|**0.003**|
|INVVOL_SAMPLE|0.03|
|MINVVOL_EWMA|0.0017|
|**MINVVOL_DCC**|**0.000**|
|MINVVOL_SAMPLE|0.004|59
|HRP_EWMA|0.015|
|**HRP_DCC**|**0.004**|
|HRP_SAMPLE|0.022|
|HERC_EWMA|1.008|
|**HERC_DCC**|**0.0236**|
|HERC_SAMPLE|0.406|


Os resultados mostram que tanto para os métodos baseados em otimizadores convexos quanto para os baseados em *clustering* a estimação da volatilidade através do GARCH-DCC diminui o erro de estimação dos pesos, um resultado evidente pois este foi o processo gerador dos nossos dados.
 
 - O HERC mostrou bastante sensibilidade à estimação da covariância com o método EWMA. O erro foi 97.6% maior em relação ao GARCH-DCC e 59.65% ao estimador amostral.
 - Os pesos do HRP estimados considerando EWMA  são 70.9%  maior do que considerando o GARCH-DCC, e 43.28% menor em comparação com o estimador amostral.
 - Os pesos estimados em relação ao método da volatilidade mínima  apresentam baixa sensibilidade a especificação da matriz de covariâncias.
 - Para o inverso da variância, o estimador amostral é o que apresenta o pior desempenho, sendo 79.76% maior que o GARCH-DCC  e 30.21% que o EWMA.
 - O máxima descorrelação teve melhor ajuste com o GARCH-DCC, mas o estimador EWMA mostrou-se  48.8% maior que o amostral e 75.17% que o GARCH-DCC.
 - O método da máxima diversificação apresenta alta variabilidade nos erros computados, sendo o estimador EWMA 30.3% maior  que o estimador amostral.
 - Os pesos estimados do portfólio Equal Risk Contribution apresentaram maior sensibilidade em relação ao estimador amostral, sendo 32.07% maior que o estimador EMWA. 


### Conclusões

Em nosso estudo, os métodos que se mostraram mais robustos em relação à  especificação matriz de covariância foram o Mínima-Variância, Inverso da Variância e o HRP.
O resultado no que tange ao MVP difere do encontrado em Ardia * et al.* (2017), já com em relação a robustes do Inverso da Variância chegamos nas mesmas conclusões que os autores. 

Os métodos convexos que não são diretamente baseados/funções da matriz de covariâncias apresentaram bastante sensibilidade em relação a especificação, implicando em variância elevada dos erros entre o portfólio verdadeiro e o estimado. Para os portfólios da máxima descorrelação e máxima diversificação, a evidência obtida através da
simulação mostra que na ausência do GARCH-DCC, melhor utilizar a matriz de covariância amostral.  Os métodos baseados *clustering* diferem em relação à especificação da matriz. O HRP é um método que tem baixa sensibilidade com erros do portfólio próximos a zero. A pesar da alta variabilidade da mediana dos erros, o HERC pode ser investigado com outras composições de medidas de distância e de métricas de risco. 


