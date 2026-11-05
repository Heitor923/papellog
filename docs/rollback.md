# PapelLog — Teste de Rollback (A2)

**Data:** 05/11/2026  
**Ambiente:** Docker Compose local, na porta 8001.

## O que foi feito

Utilizei duas versões do PapelLog publicadas no GHCR: `v1.0.0` e `v1.0.1`.

Primeiro, executei a versão `v1.0.1` e simulei uma falha na inicialização. O contêiner foi encerrado com o status `Exited (1)`.

Depois, fiz o rollback para a versão anterior usando:

```powershell
$env:ROLLBACK_VERSION="v1.0.0"
docker compose -p papellog-rollback -f docker-compose.rollback.yml up -d --force-recreate web
```

Para confirmar a versão restaurada, executei:

```powershell
docker inspect --format "{{.Config.Image}}" papellog-rollback-web-1
```

**Resultado:** `ghcr.io/heitor923/papellog:v1.0.0`

## Conclusão

O rollback funcionou. A versão `v1.0.0` foi restaurada e a página de login voltou a abrir normalmente na porta 8001.

A falha foi simulada e a recuperação foi feita manualmente, sem alterar o banco de dados.