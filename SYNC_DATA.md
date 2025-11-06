# 🔄 Sincronização de Dados entre Dev e Produção

Este guia explica como sincronizar dados (banco de dados e uploads) entre o ambiente de desenvolvimento e produção.

## 🚀 Método Rápido (Recomendado)

**Para copiar EXATAMENTE o banco de desenvolvimento para produção:**

### Windows:
```bash
deploy_db.bat usuario@servidor /caminho/do/projeto
```

### Linux/Mac:
```bash
chmod +x deploy_db.sh
./deploy_db.sh usuario@servidor /caminho/do/projeto
```

**Exemplo:**
```bash
./deploy_db.sh root@192.168.1.100 /root/Teinsta
```

Este script:
1. ✅ Encontra o banco local automaticamente
2. ✅ Mostra estatísticas (controles, módulos, etc.)
3. ✅ Cria backup automático no servidor
4. ✅ Copia o banco para produção
5. ✅ Reinicia o container
6. ✅ Verifica se está funcionando

---

## 📋 Métodos Detalhados

Este guia explica como sincronizar dados (banco de dados e uploads) entre o ambiente de desenvolvimento e produção.

## 📋 O que é sincronizado?

- ✅ Banco de dados SQLite (`iso27001.db`)
- ✅ Arquivos enviados (`uploads/`)

## 🚀 Métodos de Sincronização

### Método 1: Script Automático (Recomendado)

#### Windows:
```bash
# Exportar dados do desenvolvimento
sync_data.bat export

# Importar dados na produção
sync_data.bat import backup_completo.tar.gz
```

#### Linux/Mac:
```bash
# Dar permissão de execução (primeira vez)
chmod +x sync_data.sh

# Exportar dados do desenvolvimento
./sync_data.sh export

# Importar dados na produção
./sync_data.sh import backup_completo.tar.gz
```

### Método 2: Python Direto

#### Exportar dados:
```bash
# No ambiente de desenvolvimento
python sync_data.py export --output backup_completo.tar.gz
```

#### Importar dados:
```bash
# No ambiente de produção (Docker)
docker-compose exec web python sync_data.py import --input /tmp/backup_completo.tar.gz
docker-compose restart web

# Ou localmente
python sync_data.py import --input backup_completo.tar.gz
```

### Método 3: Sincronização via SSH (Automática)

```bash
# Sincronizar direto do dev para produção via SSH
python sync_data.py sync \
  --host usuario@servidor-producao \
  --path /caminho/do/projeto/Teinsta
```

**Nota:** Requer SSH configurado sem senha (chaves SSH) e `sync_data.py` no servidor.

## 📦 Passo a Passo Completo

### 1. No Ambiente de Desenvolvimento

```bash
# 1. Exportar todos os dados
./sync_data.sh export
# ou
python sync_data.py export --output backup_completo.tar.gz

# 2. Verificar que o arquivo foi criado
ls -lh backup_completo.tar.gz
```

### 2. Transferir para Produção

**Opção A - SCP (via SSH):**
```bash
scp backup_completo.tar.gz usuario@servidor-producao:/caminho/do/projeto/
```

**Opção B - SFTP:**
```bash
# Usar cliente SFTP como FileZilla, WinSCP, etc.
```

**Opção C - Sincronização Automática:**
```bash
python sync_data.py sync --host usuario@servidor --path /caminho/do/projeto
```

### 3. No Ambiente de Produção (Docker)

```bash
# 1. Entrar no diretório do projeto
cd /caminho/do/projeto

# 2. Importar dados
docker-compose exec web python sync_data.py import --input /tmp/backup_completo.tar.gz

# Ou usar o script
docker cp backup_completo.tar.gz $(docker-compose ps -q web):/tmp/
docker-compose exec web python sync_data.py import --input /tmp/backup_completo.tar.gz
docker-compose exec web rm /tmp/backup_completo.tar.gz

# 3. Reiniciar container para aplicar mudanças
docker-compose restart web
```

### 4. Verificar

```bash
# Ver logs do container
docker-compose logs -f web

# Acessar aplicação
curl http://localhost:5001/login
```

## 🔄 Sincronização Inversa (Produção → Dev)

Para trazer dados de produção para desenvolvimento:

```bash
# 1. No servidor de produção
ssh usuario@servidor-producao
cd /caminho/do/projeto
docker-compose exec web python sync_data.py export --output /tmp/backup_prod.tar.gz
docker cp $(docker-compose ps -q web):/tmp/backup_prod.tar.gz ./
exit

# 2. No desenvolvimento
scp usuario@servidor-producao:/caminho/do/projeto/backup_prod.tar.gz ./
python sync_data.py import --input backup_prod.tar.gz
```

## ⚠️ Importante

1. **Backup Automático:** O script de importação cria backup automático antes de sobrescrever dados
2. **Backups:** Os backups são salvos em `backups/` com timestamp
3. **Permissões:** Certifique-se de que o Docker tem permissão para acessar `data/` e `uploads/`
4. **Espaço em Disco:** Verifique espaço disponível antes de importar

## 🔧 Troubleshooting

### Erro: "Banco de dados não encontrado"
- Verifique se o banco está em `./iso27001.db` ou `./data/iso27001.db`
- No Docker, verifique se o volume está montado corretamente

### Erro: "Permission denied"
- Verifique permissões do diretório `data/` e `uploads/`
- No Docker: `docker-compose exec web chown -R www-data:www-data /app/data`

### Erro: "Container não encontrado"
- Verifique se o container está rodando: `docker-compose ps`
- Inicie se necessário: `docker-compose up -d`

### Arquivo muito grande
- Comprimir uploads antigos antes de exportar
- Ou exportar apenas banco de dados manualmente

## 📝 Exemplo Completo

```bash
# ===== DESENVOLVIMENTO =====
# 1. Exportar
./sync_data.sh export

# 2. Transferir
scp backup_completo.tar.gz user@prod:/home/user/Teinsta/

# ===== PRODUÇÃO =====
# 3. Importar
ssh user@prod
cd /home/user/Teinsta
docker cp backup_completo.tar.gz $(docker-compose ps -q web):/tmp/
docker-compose exec web python sync_data.py import --input /tmp/backup_completo.tar.gz
docker-compose restart web

# 4. Verificar
docker-compose logs -f web
```

## 🎯 Dicas

- **Agendar sincronização:** Use cron para sincronizar automaticamente
- **Versionamento:** Mantenha backups numerados (backup_001.tar.gz, backup_002.tar.gz)
- **Teste local:** Sempre teste importação em ambiente de teste antes de produção
- **Documentação:** Mantenha log de quando sincronizou e o que mudou

