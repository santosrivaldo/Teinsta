# Sistema de Gestão ISO 27001

Sistema básico visual para gestão e certificação ISO 27001 (Segurança da Informação).

## Funcionalidades

- **Dashboard**: Visão geral com estatísticas e métricas
- **Gestão de Controles**: Cadastro e acompanhamento de controles de segurança
- **Gestão de Políticas**: Documentação e versionamento de políticas
- **Não Conformidades**: Rastreamento de não conformidades e ações corretivas
- **Auditorias**: Registro e acompanhamento de auditorias

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute a aplicação:
```bash
python app.py
```

3. Acesse no navegador:
```
http://localhost:6000
```

**Nota:** A senha padrão é `admin123`. Configure a variável de ambiente `DASHBOARD_PASSWORD` para alterar.

## Estrutura

```
.
├── app.py                  # Aplicação Flask principal
├── requirements.txt        # Dependências Python
├── iso27001.db            # Banco de dados SQLite (criado automaticamente)
├── templates/             # Templates HTML
│   ├── base.html
│   ├── dashboard.html
│   ├── controles.html
│   ├── politicas.html
│   └── ...
└── static/                # Arquivos estáticos
    ├── style.css
    └── script.js
```

## Uso

1. **Dashboard**: Visualize métricas e status geral do sistema
2. **Controles**: Adicione e gerencie os controles de segurança da ISO 27001
3. **Políticas**: Documente e gerencie políticas de segurança
4. **Não Conformidades**: Registre e acompanhe não conformidades
5. **Auditorias**: Registre auditorias e seus resultados

## Notas

- O banco de dados SQLite é criado automaticamente na primeira execução
- Alguns controles padrão da ISO 27001 são inseridos automaticamente
- Os dados são armazenados localmente no arquivo `iso27001.db`

## 🚀 Deploy para Produção

### Opção Rápida (Recomendada):
```bash
# Linux/Mac
chmod +x deploy.sh && ./deploy.sh

# Windows
deploy.bat
```

### Opção Manual:
```bash
# 1. Configurar .env
cp .env.example .env
nano .env  # Edite com suas configurações

# 2. Deploy
docker-compose up -d --build

# 3. Abrir firewall (se necessário)
sudo ufw allow 6000/tcp
```

**Acesse:** `http://localhost:6000` ou `http://SEU_IP:6000`

📖 **Guias detalhados:**
- [Guia Rápido](README_DEPLOY.md) - Deploy simplificado
- [Deploy Completo](DEPLOY.md) - Todas as opções (Docker, Cloud, VPS, etc.)

## Desenvolvimento

Este é um sistema básico criado para facilitar a gestão inicial da ISO 27001. Para uso em produção, considere:
- Implementar autenticação de usuários
- Adicionar backups automáticos
- Melhorar validações e segurança
- Adicionar relatórios em PDF
- Implementar notificações e alertas
