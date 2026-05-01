"""
- Esse código é o backend de uma aplicação web escrita em Python usando o framework Flask. 
- Ele serve como uma API que recebe dados de um produto, calcula riscos/preços usando um "motor" externo (SafeBoxEngine) e devolve a resposta.
"""

"""
- from flask import Flask, render_template, request, jsonify: Importa as ferramentas necessárias do Flask:

    Flask: Para criar a aplicação.

    render_template: Para mostrar arquivos HTML (o frontend).

    request: Para receber dados enviados pelo usuário (JSON).

    jsonify: Para transformar as respostas do Python (dicionários) em formato JSON (texto estruturado) que o navegador entende.

- from safebox_engine import SafeBoxEngine: Importa uma classe personalizada de outro arquivo (safebox_engine.py). É aqui que está a lógica matemática pesada (o "cérebro" do sistema).
- app = Flask(__name__): Inicializa o aplicativo web.
- engine = SafeBoxEngine(): Cria uma instância do motor de cálculo para ser usada mais tarde.
"""
from flask import Flask, render_template, request, jsonify
from safebox_engine import SafeBoxEngine

app = Flask(__name__)
engine = SafeBoxEngine()

"""
- @app.route("/"): Define que quando alguém acessar o endereço principal do site (a "raiz").
- def index():: Executa esta função.
- return render_template("index.html"): Procura e exibe o arquivo visual index.html (o formulário onde o usuário digita os dados).
"""
@app.route("/")
def index():
    return render_template("index.html")

"""
- @app.route("/api/analisar-produto", methods=["POST"]): Cria um endereço de API. Ele só aceita o método POST (usado para enviar dados, não apenas visualizar).
"""
@app.route("/api/analisar-produto", methods=["POST"])

def analisar():

    """
    - Dentro da função def analisar():

        data = request.get_json(): Pega os dados brutos enviados pelo frontend (Javascript) e os converte para um dicionário Python.
        try: Inicia um bloco de tentativa. Se der qualquer erro aqui dentro, o código pula para os blocos except lá embaixo.

    - Extração e tratamento de dados:

        produto_id = data.get('produto_id'): Pega o ID do produto.
        preco_concorrente = float(data.get('preco_concorrente')): Pega o preço e força a conversão para número decimal (float). Se vier texto, dará erro.
        custo = float(data.get('custo')): Mesma coisa para o custo.

    - Configuração das Taxas:

        config_taxas = { ... }: Cria um dicionário para agrupar as taxas.

            "imposto": Pega o imposto, converte para float. O , 0 significa: "se não vier nada, use 0".
            "taxa_plat": Atenção aqui: Ele soma a taxa_plat (taxa da plataforma) com o valor de financeiro. Ambos têm valor padrão 0 se não forem enviados.
            "margem": Pega a margem de lucro desejada.

    - Validação e Execução:

        if not produto_id: Verifica se o ID veio vazio.

            return jsonify({"status": "erro", ...}): Se estiver vazio, encerra a função retornando uma mensagem de erro JSON.

        analise = engine.analisar_risco(...): Esta é a linha mais importante. Chama o método analisar_risco daquele motor que importamos no início, passando todos os dados tratados (produto_id, preço, custo e o dicionário de taxas).

        return jsonify(analise): Se tudo deu certo, transforma o resultado da análise em JSON e devolve para quem chamou (o frontend).
    
    - Tratamento de Erros: 
        Isso serve para o site não "quebrar" se o usuário digitar algo errado.

        except ValueError: Esse erro acontece especificamente se o Python tentar converter uma letra para número (no float()).
            Retorna JSON avisando: "Verifique se todos os números foram preenchidos corretamente."

        except Exception as e: Captura qualquer outro erro genérico que não foi previsto.
            Retorna JSON com a mensagem técnica do erro (str(e)), útil para debugging.

    """

    data = request.get_json()
    
    try:
        produto_id = data.get('produto_id')
        # Novo campo recebido do front
        preco_concorrente = float(data.get('preco_concorrente')) 
        custo = float(data.get('custo'))
        
        config_taxas = {
            "imposto": float(data.get('imposto', 0)),
            "taxa_plat": float(data.get('taxa_plat', 0)) + float(data.get('financeiro', 0)), 
            "margem": float(data.get('margem', 0))
        }

        if not produto_id:
            return jsonify({"status": "erro", "msg": "ID do produto é obrigatório."})

        # Passamos o preço manual para a engine
        analise = engine.analisar_risco(produto_id, preco_concorrente, custo, config_taxas)
        
        return jsonify(analise)
    
    except ValueError:
        return jsonify({"status": "erro", "msg": "Verifique se todos os números foram preenchidos corretamente."})
    except Exception as e:
        return jsonify({"status": "erro", "msg": str(e)})

if __name__ == "__main__":
    app.run(debug=True)