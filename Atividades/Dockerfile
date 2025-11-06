# Usa uma imagem base Python
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de dependência e os instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY app.py .

# Expõe a porta que a aplicação vai rodar
EXPOSE 5001

# Comando para rodar a aplicação quando o container iniciar
CMD ["python", "app.py"]