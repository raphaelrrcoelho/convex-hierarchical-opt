
# Can Machine Learning-Based Portfolios Outperform Traditional Risk-Based Portfolios? The Need to Account for Covariance Misspecification

> Resumo:

Técnicas atuais de alocação de portfólio são baseadas na otimização  **mean-variance**. Nestas, os pesos ótimos encontrados estão condicionados a previsão sobre os retornos e  riscos de cada ativo.
Por outro lado, as técnicas de alocação *Risk-Based* dependem apenas da previsão do risco através das matrizes de covariâncias.

 - Uma matriz de tamanho *N* necessita de *N(N+1)/2* observações i.i.d para estimação dos parâmetros.
 - Há evidência na literatura (Lopez de Prado,2016) de que a estrutura das correlações não permanecem constantes ao longo do tempo. Também existe a evidência de clusters de volatilidade.
 - Nos portfólios construídos a partir de teoria dos grafos, como no caso dos hierárquicos, não há necessidade da inversão da matriz de covariâncias. O que torna estas técninas menos instáveis (Ver capítulo 7, AFML).
 
 
 Sobre as variâncias dos portfólios em cada métrica os autores trazem:
 - O portfólio MVP possue a menor variância in-sample mas não possui a melhor performance out-of-sample.
 - O método HRP possui melhor performance out-of-sample em termos de variância.
 - HRP  e *Inverse Volatility Weighted*  são as técnicas com melhor performance quando utilizamos um estimador de covariância pobre.
 
 
 
 Neste artigo os autores encontram os seguintes pontos sobre a estimação da matriz de covariâncias:
 - A performance de todos os portfólios testados pelos autores, com relação a as suas respectivas funções objetivos, melhoram quanto o GARCH-DCC é utilizado na previsão.
 - A técnica **Maximum Diversification** é a que apresenta a maior sensibilidade em relação à previsão da matriz de covariâncias.
 
 
 
 
 
