# Copilot Instructions - Cybersecurity Fundamentals Exercises

This workspace contains DTU course exercises (02270) covering cryptography and security protocol analysis.

## Project Structure

- **Week 2**: Cryptographic implementations (RSA decryption, Caesar cipher)
- **Week 4**: Protocol analysis using AnB notation and OFMC model checker

## Key Technologies

### AnB Protocol Notation

Formal language for specifying authentication and key exchange protocols. Core structure:

- **Types**: Agent roles and values (e.g., `Agent A,B,s` for three parties)
- **Knowledge**: What each agent knows initially (secrets, keys, public values)
- **Actions**: Message sequences with encryption `{}` and signing `_inv(pk(X))`
- **Goals**: Security properties to verify (secrecy, authentication)

Example syntax:

```anb
Protocol: NSPK
Types: Agent A,B; Number NA,NB; Function pk
Actions:
  A->B: {NA,A}(pk(B))      # Encrypt with B's public key
  B->A: {NA,NB}(pk(A))     # Symmetric key crypto: {|msg|}_K
  A->B: {NB}(pk(B))
Goals:
  B authenticates A on NA   # B can verify NA came from A
  NA secret between A,B     # Only A and B know NA
```

### OFMC Model Checker

Tool in `Week 4/ofmc2024.2/executables/mac/ofmc`. Performs formal verification of protocols.

**Workflow**:

1. Write `.AnB` protocol file
2. Run: `./ofmc <file.AnB>` or `./ofmc <file.AnB> --numSess 3` for multiple sessions
3. Output shows: "SAFE" (goals verified) or attack trace showing vulnerable interleaving

**Understanding attack traces**:

- Numbered steps show message interceptions/forwarding by the intruder
- Step format: `(Agent,session) -> recipient: message`
- Cross-reference with task explanation markdown (e.g., `task1_explain.md`) to understand why goals fail

## Developer Patterns

### AnB Protocol Development

1. **Review existing examples** in `Week 4/ofmc2024.2/examples/` for similar patterns (symmetric key, public key, TTP-based)
2. **Define security goals explicitly** - be precise about authentication and secrecy boundaries
3. **Watch for common vulnerabilities**:
   - Readable (signed but unencrypted) nonces that intruders can replay with different identities
   - Insufficient binding between keys and intended recipients
   - Missing freshness checks or identity confirmation
4. **Fix strategy** (from `task1_explain.md`):
   - Hide sensitive values: use encryption in addition to signatures
   - Bind values to specific agents: include recipient identity in encrypted/signed messages
   - Avoid protocol rules that allow redirection to unintended parties

### Python Cryptography (Week 2)

Uses `sympy` and `pycryptodome`:

```python
from sympy import factorint
from Crypto.Util.number import inverse, long_to_bytes

# RSA decryption pattern
d = inverse(e, phi_n)
plaintext = pow(c, d, n)
flag = long_to_bytes(plaintext)
```

Setup: `pip install sympy` (virtualenv in `.venv`)

## Critical Workflows

**Verify a protocol**:

```bash
cd Week 4
./ofmc nspk.AnB  # Check for attacks
./ofmc nspk.AnB --numSess 3  # Multi-session analysis (stronger)
```

**Read attack traces**:

- `task1_explain.md` and `task2_explain.md` contain line-by-line mapping of OFMC output
- Key pattern: intruder intercepts readable message → forges identity → tricks server into producing secrets → forwards to original party
- The protocol looks "legal" to honest agents but violates secrecy/authentication at system level

**Create new protocol**:

1. Start from similar `.AnB` example (e.g., `KeyEx.AnB` for TTP, `nspk.AnB` for public key)
2. Specify types, initial knowledge, and actions
3. Declare goals (authentication, secrecy)
4. Run OFMC; if attack found, review trace and add constraints (encryption, identity checks, server binding)

## External Dependencies

- **OFMC 2024.2**: Included in `Week 4/ofmc2024.2/`. Uses pre-built macOS binary in `executables/mac/`
- **Syntax highlighting**: AnB language support in `ofmc2024.2/AnB-syntax-highlighting/` (Sublime, Emacs)

## Notes for AI Assistants

- When analyzing failing protocols, always read the corresponding `_explain.md` file to understand the attack rationale
- Protocol vulnerabilities often stem from insufficient binding (e.g., server producing a key without confirming the original requester)
- The intruder model is Dolev-Yao (can intercept, decrypt with known keys, recompose messages) – not a cryptographic break
- Use `--numSess N` flag for stronger verification (detects multi-session attacks)
