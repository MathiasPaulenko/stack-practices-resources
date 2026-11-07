// Envelope encryption with AWS KMS — field-level encryption for PII columns.
// The DEK encrypts data; the KMS-held KEK encrypts the DEK. The KEK never
// leaves the KMS, so a database dump alone reveals nothing.
//
// Run: npm install @aws-sdk/client-kms && node envelope-kms.js
// (requires AWS credentials with kms:Encrypt / kms:Decrypt on the key)

const { KMSClient, EncryptCommand, DecryptCommand } = require("@aws-sdk/client-kms");
const crypto = require("crypto");

async function encryptField(plaintext, kmsKeyId, region = "us-east-1") {
  const dek = crypto.randomBytes(32);      // random 256-bit DEK per record
  const iv = crypto.randomBytes(12);       // unique 96-bit nonce per DEK

  const cipher = crypto.createCipheriv("aes-256-gcm", dek, iv);
  const ciphertext = Buffer.concat([cipher.update(plaintext, "utf8"), cipher.final()]);
  const authTag = cipher.getAuthTag();

  const kms = new KMSClient({ region });
  const { CiphertextBlob } = await kms.send(new EncryptCommand({
    KeyId: kmsKeyId,
    Plaintext: dek,
  }));

  return {
    encryptedDek: Buffer.from(CiphertextBlob).toString("base64"),
    iv: iv.toString("base64"),
    authTag: authTag.toString("base64"),
    ciphertext: ciphertext.toString("base64"),
  };
}

async function decryptField(encrypted, region = "us-east-1") {
  const kms = new KMSClient({ region });
  const { Plaintext: dek } = await kms.send(new DecryptCommand({
    CiphertextBlob: Buffer.from(encrypted.encryptedDek, "base64"),
  }));

  const decipher = crypto.createDecipheriv(
    "aes-256-gcm", Buffer.from(dek), Buffer.from(encrypted.iv, "base64")
  );
  decipher.setAuthTag(Buffer.from(encrypted.authTag, "base64"));
  return Buffer.concat([
    decipher.update(Buffer.from(encrypted.ciphertext, "base64")),
    decipher.final(),
  ]).toString("utf8");
}

// Local-only demo without KMS: wrap the DEK with a local "KEK" so the flow
// is runnable end-to-end. Production uses KMS exactly as above.
function demo() {
  const kek = crypto.randomBytes(32);
  const wrap = (dek) => {
    const iv = crypto.randomBytes(12);
    const c = crypto.createCipheriv("aes-256-gcm", kek, iv);
    return Buffer.concat([iv, c.update(dek), c.final(), c.getAuthTag()]);
  };
  const unwrap = (blob) => {
    const d = crypto.createDecipheriv("aes-256-gcm", kek, blob.subarray(0, 12));
    d.setAuthTag(blob.subarray(-16));
    return Buffer.concat([d.update(blob.subarray(12, -16)), d.final()]);
  };

  const dek = crypto.randomBytes(32);
  const wrapped = wrap(dek);
  console.log("wrapped DEK:", wrapped.toString("base64").slice(0, 40), "...");
  console.log("unwrapped matches:", unwrap(wrapped).equals(dek));
}

demo();
