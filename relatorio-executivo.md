# Relatório executivo: Queimadas no Brasil (2024-2025)

**Para:** órgãos ambientais e Defesa Civil (organização contratante)
**Base:** 414.692 focos do satélite de referência do INPE, cruzados com o Censo 2022 do IBGE para os 5.570 municípios.

## 1. O que os dados revelam

- O fogo é **sazonal e concentrado**: 63% dos focos ocorrem entre agosto e outubro. O pior mês da série foi setembro/2024, com 83.154 focos.
- O fogo acompanha a **seca**: nos meses com mais dias sem chuva há mais focos em todos os biomas com volume relevante (Spearman de 0,52 na Amazônia a 0,88 no Cerrado).
- 60% dos focos ocorreram em condição de **risco de fogo crítico** (índice INPE acima de 0,95).
- Os focos caíram **51%** de 2024 (278.299) para 2025 (136.393). Mas 2024 foi um ano de seca extrema, então parte da queda é climática e não pode ser atribuída só a ações de combate.

## 2. Situações, regiões e grupos que merecem atenção

| Prioridade | Onde | Evidência |
|---|---|---|
| **Alta, tendência de alta** | **Matopiba e Caatinga** (MA, BA, PI, TO) | Caatinga **+16%** em 2025. Maranhão virou o estado com mais focos (24.300). Bahia +32%. Barra (BA) passou de 207 para 701 focos. |
| **Alta, volume** | Arco do desmatamento (sul do PA, norte do MT, AM, RO) | São Félix do Xingu, Altamira, Novo Progresso e Apuí lideram a série. PA e MT somam 33% dos focos. |
| **Média, recorrência** | 683 municípios do perfil **Hotspots** | Concentram 70% de todos os focos. |
| **Fiscalização** | 532 municípios do perfil **Baixo risco climático** | Só 11% dos focos em risco crítico: fogo fora da condição de seca, indício de queima por manejo ou ação humana. |

## 3. Padrões e tendências identificados

- **Deslocamento do fogo:** em 2025 a queda foi forte na Amazônia (-69%) e no Pantanal (-95%), mas o fogo cresceu na Caatinga (+16%) e no Pampa (+66%, ainda com volume baixo). **591 municípios** tiveram mais focos em 2025 do que em 2024.
- **Pico mais curto em 2025:** a concentração em agosto a outubro caiu de 66% para 55%, com focos mais espalhados ao longo do ano.
- **Perfis distintos:** a clusterização separou cinco perfis de município (Hotspots, Seca prolongada, Fogo intenso, Moderado e Baixo risco climático). Cada perfil pede uma resposta diferente.

## 4. Decisões que os dados permitem tomar

1. **Pré-posicionar brigadas em julho**, antes do pico, nos municípios Hotspots e Seca prolongada, priorizando pelo indicador de focos por 1.000 km² com volume mínimo de focos.
2. **Redirecionar parte dos recursos para o Matopiba e a Caatinga**, onde o fogo cresceu em 2025, em vez de repetir a distribuição de 2024, centrada na Amazônia.
3. **Fiscalização e educação ambiental** nos municípios de Baixo risco climático, onde o fogo não se explica pelo clima.
4. **Equipamento de maior porte** nos 123 municípios de Fogo intenso (FRP cerca de 4× a média), onde o fogo é mais severo.
5. **Alerta antecipado** quando os dias sem chuva subirem num bioma, dada a correlação forte, especialmente no Cerrado.

## 5. Resultados a acompanhar

| Indicador | Meta de acompanhamento | Fonte |
|---|---|---|
| Focos em agosto a outubro por bioma | Queda ano a ano, comparada a anos de clima semelhante | `focos_bioma_mes` |
| Focos nos municípios priorizados | Queda maior que a média nacional | `gold_municipios` |
| % de focos em risco crítico | Estável. Se cair com focos estáveis, o fogo está migrando para fora da seca | `silver_focos` |
| Municípios que mudam de perfil | Saída do perfil Hotspots | `clusters` |
| Focos na Caatinga e no Matopiba | Reverter a alta de 2025 | `focos_bioma_mes` |

O pipeline é reprodutível: basta reingerir os meses novos do INPE (`bronze.py` é idempotente) e rodar Silver, Gold e análises para atualizar todos os indicadores.

## Limitações

- Apenas dois anos de série. Para separar efeito do clima de efeito de política pública, é preciso estender o histórico (o INPE disponibiliza desde 2003).
- Focos de calor não equivalem a área queimada: um incêndio grande pode gerar vários focos.
- Os perfis de clusterização têm sobreposição (silhueta 0,25) e servem para priorizar, não para classificar de forma rígida.
