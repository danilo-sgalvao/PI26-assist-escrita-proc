# Frontend

Base React + TypeScript da tarefa T06 (#10).

## Desenvolvimento

Requer Node.js 22.22.2 ou superior. Em `frontend/`:

```sh
npm ci
npm run dev
```

O Vite encaminha `/api` para `http://localhost:8080`. A página inicial apresenta o termo de ciência e consulta `GET /api/health`. O aceite será ligado à autenticação e ao registro de consentimento na tarefa T14; esta página informativa ainda não libera o uso da plataforma.

Para verificar localmente: `npm run lint`, `npm test` e `npm run build`.
