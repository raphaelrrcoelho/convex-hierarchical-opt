# The Hierarchical Equal Risk Contribution Portfolio (HERC) - 2016

Thomas Raffinot propõe um novo método, baseado na noção de hierarquia, que tenta diversificar a alocação de capital e também a de risco.

* As matrizes de correlações não possuem em si mesma quaisquer estruturas hierárquicas,  isto implica em variação irrestrita dos pesos ao longo de todas as classes de ativos. Desta forma, esta é uma das razões destas técnicas de otimização de portfólios não conseguirem performar melhor que o *Naive 1/N* portfólio. Na estrutura hierárquica, apenas as correlações que importam são retidas.

> HCAA

O Hierarchical Clustering based Asset Allocation (HCAA). Busca obter um trade-off entre diversificação ao longo de todos os investimentos e diverfisicação ao longo dos clusters de investimenos sob múltiplos níveis hierárquicos. O HCAA é realizando em 4 passos:

* Passo 1: Clusterização Hierárquica
* Passo 2: Seleção ótima do número de clusters baseando-se no Gap Index [Tibshirani 2001].
* Passo 3: Alocação de capital ao longo dos clusters.
* Passo 4: Alocação de capital dentro de cada cluster.

> HRP

O HRP inicia reorganizando a matriz de covariância, colocando investimentos similares juntos. Após a reorganização, a distribuição ótima dos pesos segue uma alocação adotando a variância inversa entre ativos descorrelacionados.  

* Os 3 passoa para a geração do HRP.

* Passo 1: Geração da Minimum Spanning Tree (MST).
* Passo 2: Quasi-Diagonalização.
* Passo 3: Biseção Recursiva.

> HERC

* O HERC combina e aprimora a abordagem de Machine Learning do HCAA com a bissecção recursiva do HRP.

* O Hierarchical "1/N" tem com objetivo se manter simples e não focar somente nos clusterings, mas a todas as hierarquias associadas a estes clusters. O princípio é o de obter uma diversificação dos pesos, ao distribuir o capital igualmente ao longo de cada hierarquia de clusters, de forma que todos os ativos correlacionados recebam o mesmo percentual alocado que um único ativo descorrelacionado.

* Os resultados demonstraram que o HERC "1/N" se mostrou difícil de ser superado. Porém, portfólios HERC baseados em métricas de downside, conseguem obter melhores performances ajustadas ao risco, especialmente portfolios que adotam como *risk measure* o Conditional Drawdown at Risk (CDaR).