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

## Deploy para Produção

Para fazer deploy em produção, consulte o guia completo em **[DEPLOY.md](DEPLOY.md)**.

O guia inclui instruções para:
- 🐳 Docker e Docker Compose
- ☁️ Plataformas cloud (Render, Railway, Heroku, PythonAnywhere)
- 🖥️ Servidor VPS próprio
- 🔒 Configurações de segurança
- 💾 Backup e monitoramento

**Importante:** Antes de fazer deploy, configure:
- Variável de ambiente `SECRET_KEY` (obrigatório)
- Variável de ambiente `DASHBOARD_PASSWORD` (obrigatório)
- Veja `.env.example` para referência

## Desenvolvimento

Este é um sistema básico criado para facilitar a gestão inicial da ISO 27001. Para uso em produção, considere:
- Implementar autenticação de usuários
- Adicionar backups automáticos
- Melhorar validações e segurança
- Adicionar relatórios em PDF
- Implementar notificações e alertas
