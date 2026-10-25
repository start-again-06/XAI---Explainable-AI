# API Contract and Typed Client

This project now supports an explicit OpenAPI contract and generated frontend types.

## Generate OpenAPI Schema

From `frontend/`:

```bash
npm run gen:api-schema
```

This exports `backend/openapi.json` from the running FastAPI app definition.

## Generate Frontend API Types

From `frontend/`:

```bash
npm run gen:api-types
```

This writes:

- `frontend/src/types/api.generated.d.ts`

The file is generated from `backend/openapi.json` and should not be edited manually.

## Recommended Workflow

1. Change backend routes/models.
2. Run `npm run gen:api-types`.
3. Update frontend usage as needed.
4. Commit backend + generated type changes together.
