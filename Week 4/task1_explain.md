Trace lines (from OFMC) and mapping:

1. (x20,1) -> i: {NA(1), x20}\_inv(pk(x20))

   - Protocol mapping: A -> S : {NA, A}\_inv(pk(A)) was sent, but intruder `i` intercepted it.
   - Meaning: A broadcast/signed message was readable by the intruder (signature does not hide NA).

2. i -> (x25,1): {NA(1), i}\_inv(pk(i))

   - Intruder action: intruder creates its own signed message using the learned NA, claiming to be agent `i` ({NA, i} signed with intruder private key) and sends it to S.
   - Why intruder can: It read `NA` in step 1, it has its own private key so can sign `{NA, i}`.

3. (x25,1) -> i: {|NA(1)|}_Ktemp(2), {tag, {tag, Ktemp(2)}\_inv(pk(x25))}_(pk(i))

   - Protocol mapping: S -> recipient (now the intruder `i`) produces the normal reply: `|NA|_Ktemp` and the signed `{tag,Ktemp}` encrypted to the recipient's public key (here `pk(i)`).
   - S is acting legally given the signed message it received (it believes it is talking to `i`).

4. i -> (x20,1): {|NA(1)|}_Ktemp(2), {tag, {tag, Ktemp(2)}\_inv(pk(x25))}_(pk(x20))
   - Intruder action: intruder forwards the `|NA|_Ktemp` unchanged and **re-encrypts** the signed `{tag,Ktemp}` blob so it is delivered to A (encrypt outer layer to `pk(A)`), or simply forwards/rewraps into the form S’s reply would take to A.
   - Why intruder can: The signed blob `{tag, {tag, Ktemp}}` is valid (signed by S); encryption to a different public key does not change the validity of the inner signature. The intruder obtained the signed Ktemp from S in step 3 and so can repackage it to A.

**Result:** Intruder now knows `Ktemp` (it was delivered to `i` in step 3) and A accepts `Ktemp` as valid (it sees a valid S signature after decrypting), so secrecy is lost.

**Important detail:** Each reply from honest parties corresponds to a legal protocol step:

- S replied to what it believed to be a valid signed request (from `i`), so its reply is legal.
- A received a reply that looks like a legal S reply, so it acts legally.

Thus the whole attack is _executable_ under protocol rules — OFMC just explores these interleavings and proves the secrecy goal fails.

---

## 4) Where did it go wrong? What the designer likely missed? How to fix?

### Where it went wrong (plain)

- **A’s first message is readable by the adversary** (it is only _signed_, not encrypted). That reveals `NA` to the intruder.
- S is willing to deliver `Ktemp` to whoever asks and only binds `Ktemp` to the recipient by outer encryption to the recipient’s public key. If the intruder can get S to encrypt/signed `Ktemp` to the intruder’s public key (by pretending to be the requester), the intruder obtains `Ktemp`.
- The protocol does not ensure that S’s reply containing `Ktemp` is only ever produced for the _actual_ A who originally requested the key — S has insufficient evidence that the requester was really A (it only saw a signed but readable nonce).

### Designer’s likely intention vs reality

- Likely intention: signature on `{NA,A}` proves message authenticity, and the blob encrypted to `pk(A)` ensures only A learns `Ktemp`. But because the signed message is readable, attacker can replay `NA` to S with its own identity and make S produce `Ktemp` for the attacker.
- The designer probably assumed signatures alone are enough or didn’t consider that the intruder could reuse `NA` in a different session.

### Minimal, effective fixes (choose one)

**Fix 1 (recommended): hide the nonce so intruder cannot read it — sign then encrypt to S.**  
Change the first message to **sign then encrypt**:

```text
A -> S : { { NA, A } inv(pk(A)) } pk(S)
```
