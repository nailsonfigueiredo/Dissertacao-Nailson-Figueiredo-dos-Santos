# Dissertacao-Nailson-Figueiredo-dos-Santos

Este repositório contém os arquivos de simulação do EnergyPlus, scripts de geração de ocupação, algoritmos de Machine Learning para estimativa de ocupação e notebooks para análise de consumo energético e conforto térmico promovidas no trabalho de dissertação "Estimativa de ocupação em ambientes climatizados com foco em eficiência energética utilizando aprendizado de máquina" apresentado ao Programa de Pós Graduação em Engenharia de Sistemas de Energia.

# 📂 Estrutura do Repositório

```text
.
├── Horario Dinamico/            # Simulação EnergyPlus: Desligamento/acionamento dinâmico baseado na estimativa de ocupação
├── Setpoint Dinamico/           # Simulação EnergyPlus: Ajuste dinâmico de setpoint baseado na estimativa de ocupação
├── Setpoint e Horario Dinamico/ # Simulação EnergyPlus: Junção do acionamento e setpoint dinâmicos baseados na estimativa de ocuoação
├── Setpoint e Horario Fixo/     # Simulação EnergyPlus (Baseline) com setpoint e horário fixo para estimativa de ocupação
│   └── Occupancy_Estimation.ipynb # Notebook de pré-processamento dos dados, treinamento e testes dos modelos de Machine Learning
├── Ocupacao.py                  # Script Python para geração dos padrões aleatórios de ocupação
├── ocupacao.csv                 # Perfil de ocupação gerado
└── Analise Energia e Conforto.ipynb # Notebook para processamento e comparação dos resultados de conforto térmico e energia de cada simulação.
