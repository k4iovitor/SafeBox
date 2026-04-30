# 🛡️ SafeBox

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/API-Mercado_Livre-FFE600?style=for-the-badge&logo=mercadolivre&logoColor=black" alt="Mercado Livre API" />
</p>

<div align="center">
  <img width="1280" height="599" alt="Interface Principal do SafeBox" src="https://github.com/user-attachments/assets/09e5e54b-4e94-418f-84c9-4c1da4fad2f1" />
</div>

---

## Sobre o Projeto

O mercado de e-commerce e marketplaces (como o Mercado Livre) vive uma "tempestade perfeita" para os vendedores. Com algoritmos predatórios, concorrência desleal (muitas vezes com players asiáticos subsidiados) e custos ocultos (taxas de plataforma, antecipação, impostos), muitos varejistas estão **vendendo muito, mas lucrando pouco** ou até tendo prejuízo para ganhar a *Buy Box*.

O **SafeBox** nasce para resolver essa dor. Ele é uma aplicação web focada na **saúde financeira** do vendedor. Diferente de precificadores comuns que focam apenas em volume e redução de preços, o SafeBox atua como um escudo: ele calcula o custo real e alerta, em tempo real, se entrar em uma guerra de preços vai gerar lucro ou prejuízo.

### Objetivos Principais

1. **Raio-X do Custo Real:** Revelar o custo invisível por trás de cada venda, calculando matematicamente o ponto exato onde a venda se torna tóxica (Markup Divisor).
2. **Monitoramento Defensivo:** Cruzar dados de custo do vendedor com as taxas oficiais do Mercado Livre (Classic/Premium) via API.
3. **Trava de Segurança (Semáforo de Risco):** Indicar visualmente e de forma clara a ação recomendada: *Competir*, *Monitorar* ou *Pausar*.

---

## Funcionalidades e Telas do Sistema

O motor matemático do SafeBox (`SafeBoxEngine`) analisa os dados e retorna o status da operação categorizado em três níveis de risco.

### 🟢 Nível SAFE: Venda Segura
Quando o preço praticado no mercado possui uma margem superior ao seu Preço Mínimo Viável. O sistema recomenda a competição.

<img width="1280" height="625" alt="Dashboard SafeBox - Nível de Venda Segura" src="https://github.com/user-attachments/assets/858c3b72-6ee5-40ea-b420-33f04f099c76" />

### 🟡 Nível WARNING: Alerta de Margem
Quando o preço da *Buy Box* está muito próximo do seu mínimo viável (margem de folga < 5%). O sistema sugere monitoramento diário.

<img width="1280" height="626" alt="Dashboard SafeBox - Alerta de Margem" src="https://github.com/user-attachments/assets/651cac72-7957-4227-bd13-fe3c2df5c3ee" />

### 🔴 Nível DANGER: Risco de Prejuízo
Quando a guerra de preços ultrapassa o seu custo total (produto + impostos + taxas + financeiro). O sistema bloqueia a ação, recomendando "Não Vender / Pausar", impedindo que o vendedor pague para trabalhar.

<img width="1280" height="630" alt="Dashboard SafeBox - Risco de Prejuízo" src="https://github.com/user-attachments/assets/7f3bf910-dbeb-4877-b203-6fc1c891f19e" />

---

## Como a Tecnologia Funciona

O projeto utiliza uma arquitetura simples e eficiente baseada em Python:

* **Frontend (UI/UX):** Interface construída com HTML5 e CSS3 (`style.css`), utilizando variáveis de ambiente, design responsivo, e feedback visual em cores semânticas (Verde, Amarelo, Vermelho) para rápida tomada de decisão.
* **Backend (Flask - `app.py`):** Criação de uma API RESTful (`/api/analisar-produto`) que recebe os inputs do usuário e devolve um JSON com os cálculos e o estado de risco.
* **Motor de Regras (`safebox_engine.py`):**
  * **Extração Inteligente:** Usa Expressões Regulares (`regex`) para encontrar IDs de produtos (ex: `MLB123456`) a partir de links completos.
  * **Integração API Mercado Livre:** Consome endpoints oficiais (`/items` e `/products`) via Token de Acesso para puxar foto, título e calcular a taxa automática (Clássico vs Premium) com base na categoria do anúncio.
  * **Cálculo de Markup:** Aplica matemática financeira para garantir que a soma das porcentagens (imposto, plataforma, financeiro e margem desejada) seja corretamente aplicada sobre o custo do produto.

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3.x, Flask, Requests, Regex (`re`)
* **Frontend:** HTML5, CSS3, JavaScript (Fetch API)
* **Integração:** API Oficial do Mercado Livre (REST)

---

## 🚀 Como rodar o projeto localmente

Siga os passos abaixo para testar o SafeBox em sua máquina:

**1. Clone este repositório:**
```bash
git clone [https://github.com/SEU_USUARIO/safebox.git](https://github.com/SEU_USUARIO/safebox.git)
