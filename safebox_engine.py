"""
- import requests: Importa a ferramenta que permite ao Python "navegar na internet" e acessar sites/APIs.
- import re: Importa "Expressões Regulares" (Regex), uma ferramenta poderosa para encontrar padrões em textos (usamos para achar o ID MLB... no meio de um link gigante).
- ML_ACCESS_TOKEN: É a variável onde você cola a chave de acesso que o Mercado Livre te dá. Sem ela, a API não deixa você entrar.
"""
import requests
import re

# Cole seu token do Mercado Livre aqui (Ex: APP_USR-123...)
ML_ACCESS_TOKEN = "APP_USR-3298133118346356-120913-685d73949360f71d75292e062c0404c0-1760782564"

"""
- class SafeBoxEngine: Define o "molde" do nosso motor.
- def __init__(self): É a função que roda automaticamente quando o motor é ligado.
- self.ml_base_url: Guarda o endereço base da API do Mercado Livre.
- self.headers: Cria o "crachá de identificação". Toda vez que o código bater na porta do Mercado Livre, ele vai mostrar esse crachá (Authorization: Bearer ...) para provar que tem permissão.
"""

class SafeBoxEngine:
    def __init__(self):
        # Define o endereço base da API do Mercado Livre
        self.ml_base_url = "https://api.mercadolibre.com"
        
        # Configura o "Crachá de Acesso" (Headers)
        # 'Bearer' é o tipo de autenticação e 'application/json' o formato dos dados
        self.headers = {
            "Authorization": f"Bearer {ML_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

    def extrair_id(self, input_usuario):
        # Se o usuário não digitou nada, retorna string vazia
        if not input_usuario: return "ID-MANUAL"

        # Remove espaços em branco antes e depois (.strip)
        input_usuario = input_usuario.strip()

        # --- CORREÇÃO PARA O SEU ERRO DE ID ---
        # Alguns links contêm "item_id:MLB...", precisamos pegar esse especificamente
        match_specific = re.search(r'item_id:(MLB\d+)', input_usuario, re.IGNORECASE)
        if match_specific: return match_specific.group(1)

        # Usa Regex (expressão regular) para procurar o padrão "MLB" seguido de números
        # Exemplo: Transforma "https://produto.mercadolivre...MLB12345" apenas em "12345"
        match = re.search(r'(MLB\d+)', input_usuario.upper())
        
        # Se achou o padrão MLB dentro do link, retorna só o ID limpo
        if match: return match.group(1)
        
        # Se não achou padrão, retorna um marcador para usar modo manual
        return "ID-MANUAL"

    def calcular_preco_minimo(self, custo, impostos_pct, taxas_pct, margem_pct):
        try:
            # Soma todas as porcentagens (imposto + taxa plat + margem) e divide por 100
            # Ex: 10 + 15 + 20 = 45 -> 0.45
            total = (float(impostos_pct) + float(taxas_pct) + float(margem_pct)) / 100
            
            # Se as taxas somarem 100% ou mais (>= 1), é impossível calcular (divisão por zero ou negativa)
            if total >= 1: return None 
            
            # Fórmula de Markup Divisor:
            # Preço Venda = Custo / (1 - Taxas Totais)
            return float(custo) / (1 - total)
        except: return None

    def buscar_info_produto(self, item_id):
        """
        Busca Nome, Link e Foto usando a API Oficial com Token.
        """
        print(f"--- Buscando Dados Cadastrais: {item_id} ---")
        
        # Objeto de fallback para não quebrar o sistema se a API falhar
        fallback = {
            "sucesso": False,
            "titulo": f"Produto ID: {item_id}",
            "link": "#",
            "imagem": "",
            "tipo_anuncio": "Desconhecido",
            "taxa_sugerida": 0,
            "custo_fixo_ml": 0
        }

        if item_id == "ID-MANUAL": return fallback

        try:
            # 1. TENTA COMO ANÚNCIO ÚNICO (/items)
            url = f"{self.ml_base_url}/items/{item_id}"
            
            # Faz a requisição para a API do Mercado Livre (timeout para não travar)
            response = requests.get(url, headers=self.headers, timeout=3)
            
            # Se a resposta for 200 (Sucesso/OK)
            if response.status_code == 200:
                data = response.json()
                
                # Inteligência de Taxas (Clássico vs Premium)
                listing_type = data.get("listing_type_id", "gold_special")
                if listing_type == "gold_pro":
                    tipo_anuncio = "Premium (Parc. s/ Juros)"
                    taxa_estimada = 18.0
                elif listing_type == "gold_special":
                    tipo_anuncio = "Clássico"
                    taxa_estimada = 13.0
                else:
                    tipo_anuncio = "Outro"
                    taxa_estimada = 0.0

                # Custo fixo se for abaixo de 79
                preco_base = float(data.get("price", 0))
                custo_fixo = 6.0 if 0 < preco_base < 79 else 0.0

                # Pega a foto principal (tenta 'secure_url' primeiro, se não tiver, pega 'thumbnail')
                foto = data.get("pictures", [{}])[0].get("secure_url") or data.get("thumbnail")
                
                return {
                    "sucesso": True,
                    "titulo": data.get("title"),
                    "link": data.get("permalink"),
                    "imagem": foto,
                    "tipo_anuncio": tipo_anuncio,
                    "taxa_sugerida": taxa_estimada,
                    "custo_fixo_ml": custo_fixo
                }

            # --- CORREÇÃO: SE DER 404, TENTA CATÁLOGO ---
            if response.status_code == 404:
                url_prod = f"{self.ml_base_url}/products/{item_id}"
                response_prod = requests.get(url_prod, headers=self.headers, timeout=3)
                
                if response_prod.status_code == 200:
                    data = response_prod.json()
                    foto = data.get("pictures", [{}])[0].get("url")
                    return {
                        "sucesso": True,
                        "titulo": data.get("name"),
                        "link": data.get("permalink"),
                        "imagem": foto,
                        "tipo_anuncio": "Catálogo",
                        "taxa_sugerida": 0,
                        "custo_fixo_ml": 0
                    }

            # Se a API der erro, retorna vazio (a lógica original não tinha else explícito, mas implicitamente retorna None/Erro)
            return fallback

        except Exception as e:
            # Captura erros de conexão ou processamento
            print(f"Erro ao buscar produto: {e}")
            return fallback

    def analisar_risco(self, produto_id, preco_concorrente, custo_usuario, config_taxas):
        # 1. BUSCA AS INFORMAÇÕES VISUAIS (Token usado aqui)
        # Limpa o ID primeiro e depois busca na API
        id_limpo = self.extrair_id(produto_id)
        info = self.buscar_info_produto(id_limpo)
        
        # 2. MATEMÁTICA FINANCEIRA (Com o preço manual que você inseriu)
        try:
            preco_mercado = float(preco_concorrente)
        except:
            return {"status": "erro", "msg": "Preço do concorrente inválido."}
        
        # Calcula o preço mínimo necessário para atingir sua margem
        minimo = self.calcular_preco_minimo(
            custo_usuario, config_taxas["imposto"], config_taxas["taxa_plat"], config_taxas["margem"]
        )

        # Se o cálculo falhou (taxas muito altas), retorna erro
        if not minimo: return {"status": "erro", "msg": "Taxas > 100%."}

        # Calcula o lucro líquido projetado em Reais
        # Lucro = Preço Venda - (Imposto + Taxa ML aplicados sobre a venda) - Custo
        lucro = preco_mercado - (preco_mercado * ((float(config_taxas["imposto"]) + float(config_taxas["taxa_plat"]))/100)) - float(custo_usuario)
        
        # 3. EMPACOTAMENTO DO RESULTADO
        res = {
            "status": "sucesso",
            "titulo": info.get("titulo"),
            "link": info.get("link"),
            "imagem": info.get("imagem"),
            
            # Insights
            "tipo_anuncio": info.get("tipo_anuncio"),
            "taxa_detectada": info.get("taxa_sugerida"),
            "custo_fixo_extra": info.get("custo_fixo_ml"),

            "preco_buybox": preco_mercado,
            "seu_preco_minimo": round(minimo, 2),
            "lucro_projetado": round(lucro, 2)
        }

        # 4. SEMÁFORO (Análise de Risco)
        if preco_mercado < minimo:
            # Se o mercado vende por MENOS que o seu mínimo -> Prejuízo
            res.update({"nivel": "DANGER", "msg_seguranca": "PREJUÍZO REAL", "acao": "NÃO COMPETIR"})
        elif preco_mercado < (minimo * 1.05):
            # Se o mercado vende com uma folga menor que 5% -> Risco Alto
            res.update({"nivel": "WARNING", "msg_seguranca": "RISCO ALTO", "acao": "MONITORAR"})
        else:
            # Se tem margem de sobra -> Seguro
            res.update({"nivel": "SAFE", "msg_seguranca": "APROVADO", "acao": "COMPETIR"})

        return res