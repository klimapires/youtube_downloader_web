# Usar a imagem oficial do Python
FROM python:3.11

# Definir diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos do projeto para o container
COPY . .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta 5000 para comunicação
EXPOSE 5000

# Definir o comando para rodar o Flask com Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
