# Deployment Plan: V3 "Hermetic Convergence" Release

## Phase 1: Stabilization (Current)
- [x] **Schema Hardening**: Apply `idempotent_migrate.py` to ensure V3 contract.
- [x] **Asset Mining**: Allow `mine_images.py` to complete its full corpus scan (Background Task).
- [ ] **Data Ingestion**: Execute `ingest_historiography.py` *after* image mining completes to avoid DB locks.

## Phase 2: Interface Construction (Next Sprint)
- [ ] **Build "Gallery" Page**: Create `dashboard/src/pages/ImageGallery.tsx` to display `alchemy_images`.
- [ ] **Connect Logic**: Add `/api/alchemy/images` endpoint to `backend.py` with filtering by `motif` and `period`.
- [ ] **Theming**: Implement the "Lumina/Grimoire" toggle in `index.css`.

## Phase 3: Final Production Build
- [ ] **Build Frontend**: `npm run build` in `dashboard/`.
- [ ] **Serve Static**: Verify `backend.py` serves the new build correctly.
- [ ] **Smoke Test**: Run `smoke_test_v3.py` to verify all end-to-end flows.

## Phase 4: Launch
- [ ] **Tag Release**: `git tag v3.0.0-hermetic`.
- [ ] **Deploy**: Update the production instance.
- [ ] **Celebrate**: Review the "Story of Learning" on the new DH page.

## Immediate Action Required
**User**: Please wait for the current `mine_images.py` process to finish in your terminal before running further ingestion scripts.
