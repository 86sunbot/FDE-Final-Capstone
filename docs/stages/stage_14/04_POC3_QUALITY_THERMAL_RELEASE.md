# Stage 14 - POC3: Product, Quality and Thermal-Release Support

The Quality packet keeps MES, ERP, LIMS/QC, deviations, logistics/thermal and QMS evidence distinct. MES `RELEASED` and ERP `AVAILABLE` are displayed as conflicts when authorized QMS release is absent; they never release product.

OOS/OOT/pending QC without explicit disposition, open blocking deviations, ambiguous thermal evidence and missing controlled evidence block or make release unknown. Only a scoped `QUALITY_AUTHORITY` can create the evidence-bearing `ProductReleased` event, and configured requester/approver separation is enforced. Replays create no second release event.

The assistant may summarize the packet but cannot emit release, disposition, state or tool fields.
