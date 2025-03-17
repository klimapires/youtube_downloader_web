# YouTube Downloader Web

Uma aplicação web em Python (Flask) para baixar vídeos do YouTube na qualidade máxima. A aplicação permite escolher a qualidade do vídeo, selecionar a pasta de destino e exibe uma barra de progresso durante o download.

---

## Funcionalidades

- **Download de vídeos**: Baixe vídeos do YouTube em formatos `.mp4` ou `.avi`.
- **Seleção de qualidade**: Escolha entre 144p, 240p, 360p e 720p.
- **Barra de progresso**: Acompanhe o progresso do download em tempo real.
- **Lembrar diretório**: A aplicação lembra o último diretório escolhido para salvar os arquivos.

---

## Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.9** ou superior.
- **Docker** (opcional, para rodar em container).
- **Git** (opcional, para clonar o repositório).

---

## Como Rodar Localmente

### 1. Clone o Repositório

```bash
git clone https://github.com/klimapires/youtube_downloader_web.git
cd youtube_downloader_web
```

### 2. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 3. Execute a Aplicação

```bash
python run.py
```
A aplicação estará disponível em:
👉 http://localhost:5000

***

## Como Rodar com Docker

### 1. Construa a Imagem Docker

```bash
docker-compose build
```

### 2. Inicie o Container

```bash
docker-compose up
```
A aplicação estará disponível em:
👉 http://localhost:5000

