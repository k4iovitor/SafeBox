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

<img width="1280" height="626" alt="Dashboard - Alerta para Investir" src="https://github.com/user-attachments/assets/138460b6-3b17-4126-a1fd-7aeec747b634" />

### 🟡 Nível WARNING: Alerta de Margem
Quando o preço da *Buy Box* está muito próximo do seu mínimo viável (margem de folga < 5%). O sistema sugere monitoramento diário.

<img width="1472" height="888" alt="Dashboard SafeBox - Alerta de Margem" src="https://github.com/user-attachments/assets/f095293c-947f-4e54-b08b-ac20e5370edf" />

### 🔴 Nível DANGER: Risco de Prejuízo
Quando a guerra de preços ultrapassa o seu custo total (produto + impostos + taxas + financeiro). O sistema bloqueia a ação, recomendando "Não Vender / Pausar", impedindo que o vendedor pague para trabalhar.

<img width="1280" height="626" alt="Dashboard SafeBox - Risco de Prejuízo" src="https://github.com/user-attachments/assets/be100029-b89d-4a5f-a552-137fbf1c38f1" />

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

## Tecnologias Utilizadas

* **Backend:** Python 3.x, Flask, Requests, Regex (`re`)
* **Frontend:** HTML5, CSS3, JavaScript (Fetch API)
* **Integração:** API Oficial do Mercado Livre (REST)

---

## Como rodar o projeto localmente

Para executar o SafeBox em sua máquina, você precisará ter o [Python](https://www.python.org/downloads/) instalado e uma conta no Mercado Livre para gerar o Token de acesso à API.

### Como obter o Token da API do Mercado Livre
A aplicação precisa de uma chave de acesso para consultar os dados dos produtos oficialmente pelo Mercado Livre.

1. Acesse o portal de desenvolvedores: [Mercado Livre Developers](https://developers.mercadolivre.com.br/devcenter).
2. Faça login com a sua conta do Mercado Livre.
3. Clique em **"Criar Aplicação"**.
4. Preencha os dados básicos (Nome, Nome curto e Descrição).
5. Em **URI de redirect**, você pode colocar `https://localhost` (como é um ambiente de teste, qualquer URL válida funciona).
6. Nos escopos, marque a opção para **"Ler"** (Read) dados da API.
7. Após criar a aplicação, você verá as credenciais. Copie o **Access Token** (Ele geralmente começa com `APP_USR-...`).

**Clone este repositório:**
```bash
git clone [https://github.com/SEU_USUARIO/safebox.git](https://github.com/SEU_USUARIO/safebox.git)
