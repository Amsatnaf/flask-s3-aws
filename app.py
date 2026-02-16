import boto3
from flask import Flask, jsonify
import datetime
import os

app = Flask(__name__)

# Configurações
# Dica: No EKS, se o nó tem a Role, não precisa de chaves aqui!
BUCKET_NAME = "lab-eks-storage-diego-2026"
REGION = "us-east-1"

@app.route('/')
def index():
    return "<h1>API Flask do Diego: Online</h1><p>Use a rota <b>/upload</b> para testar o S3.</p>"

@app.route('/upload')
def upload_to_s3():
    try:
        s3 = boto3.client('s3', region_name=REGION)
        
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        nome_arquivo = f"sucesso_diego_{timestamp}.txt"
        conteudo = f"Analista Diego venceu a infra! Arquivo gerado em: {timestamp}"
        
        s3.put_object(Bucket=BUCKET_NAME, Key=nome_arquivo, Body=conteudo)
        
        return jsonify({"status": "sucesso", "arquivo": nome_arquivo, "bucket": BUCKET_NAME})
    except Exception as e:
        return jsonify({"status": "erro", "detalhes": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
