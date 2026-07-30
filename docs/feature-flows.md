# Cancion Feature Flows

This document describes the main frontend and backend feature flows for the Cancion application, with internal function and service mappings.

## 1. Contract Creation

**User flow:**
- User enters an intent like `renew Spotify for $15 monthly` on the Contracts page.
- The frontend posts the text to the backend.
- The backend parses the intent, creates a contract, saves it, and returns the contract data.

```mermaid
flowchart LR
  U[User enters intent text] --> F[ContractsPage.jsx]
  F -->|POST /contracts/| A[contracts router]
  A --> P[get_intent_parser()]
  A -->|parser.parse(text)| I[RegexIntentParser]
  I --> B[IntentBuilder]
  B --> C[ContractFactory.create(intent)]
  C --> S[ContractRepository.save(contract)]
  S --> R[ContractResponse]
  R --> F
```

**Key files:**
- `frontend/src/pages/ContractsPage.jsx`
- `src/cancion/api/routes/contracts.py`
- `src/cancion/api/dependencies.py`
- `src/cancion/intent/regex/parser.py`
- `src/cancion/domain/factory.py`
- `src/cancion/services/contract.py`
- `src/cancion/repositories/contract.py`

### Internal responsibilities
- `ContractsPage.jsx`: shows the create form, sends contract creation request, reloads active contracts.
- `contracts.py:create_contract()`: validates and parses intent, calls `ContractService.create()`.
- `RegexIntentParser.parse()`: turns free text into structured `Intent`.
- `ContractFactory.create()`: builds a `Contract` domain object.
- `ContractRepository.save()`: persists the contract via SQLAlchemy.

## 2. Active Contract Listing

**User flow:**
- The Contracts page loads active contracts on mount.
- The frontend calls the backend list endpoint.
- The backend returns a list of active contracts.

```mermaid
flowchart LR
  Page[ContractsPage.jsx mount] -->|GET /contracts/| Router[contracts router]
  Router --> Service[ContractService.list()]
  Service --> Repo[ContractRepository.list()]
  Repo --> Response[ContractResponse list]
  Response --> Page
```

**Key files:**
- `frontend/src/pages/ContractsPage.jsx`
- `src/cancion/api/routes/contracts.py`
- `src/cancion/services/contract.py`
- `src/cancion/repositories/contract.py`

### Internal responsibilities
- `ContractService.list()`: retrieves only active contracts.
- `ContractRepository.list()`: queries active contracts from the database.
- `ContractsPage.jsx`: renders active contract cards and contract metadata.

## 3. Contract Deactivation / Soft Delete

**User flow:**
- The user clicks the deactivate button on a contract card.
- Frontend sends `DELETE /contracts/{id}`.
- Backend marks the contract inactive instead of removing it.

```mermaid
flowchart LR
  Click[User clicks deactivate] --> F[ContractsPage.jsx]
  F -->|DELETE /contracts/{id}| A[contracts router]
  A --> Service[ContractService.delete(id)]
  Service --> Repo[ContractRepository.delete(id)]
  Repo --> DB[soft delete / inactive update]
  DB --> Service
  Service --> F
```

**Key files:**
- `frontend/src/pages/ContractsPage.jsx`
- `src/cancion/api/routes/contracts.py`
- `src/cancion/services/contract.py`
- `src/cancion/repositories/contract.py`

### Internal responsibilities
- `ContractRepository.delete()`: implements a soft delete / status update.
- `ContractsPage.jsx`: refreshes the active list after deactivation.

## 4. Inactive Contract History

**User flow:**
- The user opens the History tab.
- The frontend requests inactive contracts from `/contracts/history/inactive`.
- The backend returns inactive contracts.

```mermaid
flowchart LR
  Mount[HistoryPage.jsx mount] -->|GET /contracts/history/inactive| Router[contracts router]
  Router --> Service[ContractService.list_inactive()]
  Service --> Repo[ContractRepository.list_inactive()]
  Repo --> Response[ContractResponse list]
  Response --> Page
```

**Key files:**
- `frontend/src/pages/HistoryPage.jsx`
- `src/cancion/api/routes/contracts.py`
- `src/cancion/services/contract.py`
- `src/cancion/repositories/contract.py`

### Internal responsibilities
- `ContractService.list_inactive()`: returns contracts with inactive status.
- `HistoryPage.jsx`: renders the inactive contract history list.

## 5. Spend Evaluation

**User flow:**
- The user enters a contract UUID and requested amount on the Evaluate page.
- The page first fetches the contract details.
- Then it sends the spend evaluation request to `/governance/evaluate`.
- The backend loads the contract, evaluates policies, records a decision, and returns the outcome.

```mermaid
flowchart LR
  U[User enters UUID + amount] --> E[EvaluatePage.jsx]
  E -->|GET /contracts/{id}| ContractAPI
  ContractAPI --> C[ContractService.get(id)]
  C --> RepoGet[ContractRepository.get(id)]
  RepoGet --> ContractAPI
  ContractAPI --> E
  E -->|POST /governance/evaluate| GovAPI
  GovAPI --> ContractService.get(id)
  GovAPI --> SpendRequest[build SpendRequest]
  GovAPI --> GovernanceService.evaluate(contract, request)
  GovernanceService --> Engine[GovernanceEngine.evaluate(context)]
  Engine --> Rules[Vendor, Action, Amount, Status, Approval, Frequency]
  Rules --> Decision[Decision]
  Decision --> DecisionRepo.save()
  Decision --> SpendLedgerService.record_spend() [if approved]
  Decision --> GovAPI
  GovAPI --> E
```

**Key files:**
- `frontend/src/pages/EvaluatePage.jsx`
- `src/cancion/api/routes/governance.py`
- `src/cancion/api/mappers/spend_request.py`
- `src/cancion/services/governance.py`
- `src/cancion/governance/engine.py`
- `src/cancion/governance/policies/*.py`
- `src/cancion/repositories/decision.py`
- `src/cancion/services/spend_ledger.py`

### Internal responsibilities
- `EvaluatePage.jsx`: validates input, fetches the contract, posts the evaluation request, and renders the decision.
- `governance.py`: validates contract existence, maps request data, invokes the governance service.
- `GovernanceEngine.evaluate()`: runs the contract context through all configured rules.
- `VendorRule`, `ActionRule`, `AmountRule`, `StatusRule`, `ApprovalRule`, `FrequencyRule`: each checks one policy condition.
- `GovernanceService.evaluate()`: saves the decision and updates the ledger on approval.

## 6. Backend policy evaluation details

When the backend evaluates a spend request, the engine applies the following rule pipeline:

```mermaid
flowchart TB
  Context[EvaluationContext(contract, request)] --> VendorRule
  VendorRule --> ActionRule
  ActionRule --> AmountRule
  AmountRule --> StatusRule
  StatusRule --> ApprovalRule
  ApprovalRule --> FrequencyRule
  FrequencyRule --> Decision[Decision(APPROVE/DENY)]
```

### Policy rules
- `VendorRule`: checks that request vendor matches contract vendor.
- `ActionRule`: checks that request action matches contract action.
- `AmountRule`: checks that request amount does not exceed contract max amount.
- `StatusRule`: checks the contract is active.
- `ApprovalRule`: checks approval mode or auto approval rules.
- `FrequencyRule`: checks cumulative spend against contract limits.

## 7. Feature summary

| Feature | Frontend page | Backend endpoint | Core service | Purpose |
|---|---|---|---|---|
| Contract creation | `ContractsPage` | `POST /contracts/` | `ContractService.create()` | Create a contract from agent intent |
| Active contracts | `ContractsPage` | `GET /contracts/` | `ContractService.list()` | Show active contracts |
| Soft delete | `ContractsPage` | `DELETE /contracts/{id}` | `ContractService.delete()` | Deactivate a contract |
| Inactive history | `HistoryPage` | `GET /contracts/history/inactive` | `ContractService.list_inactive()` | Show inactive contracts |
| Spend evaluation | `EvaluatePage` | `POST /governance/evaluate` | `GovernanceService.evaluate()` | Approve or deny spend requests |

## 8. How to use these docs

- Start the backend with `uv run uvicorn cancion.api.app:app --reload --port 8015`
- Start the frontend in `frontend/` with `npm run dev`
- Use the Contracts page to create and deactivate contracts
- Use the History page to inspect inactive contracts
- Use the Evaluate page to test actual policy evaluation
