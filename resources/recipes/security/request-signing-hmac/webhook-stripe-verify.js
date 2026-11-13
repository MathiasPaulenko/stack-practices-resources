// Stripe-style webhook verification — the signature header carries the
// timestamp inside it ("t=...,v1=...") and may hold several v1 values
// while the provider rotates secrets.
const crypto = require('crypto');

function verifyWebhook(rawBody, signatureHeader, secret) {
    const parts = signatureHeader.split(',');
    const timestamp = parts.find(p => p.startsWith('t='))?.split('=')[1];
    const signatures = parts
        .filter(p => p.startsWith('v1='))
        .map(p => p.split('=')[1]);

    if (!timestamp || signatures.length === 0) return false;

    // Reject stale timestamps (5 minute window)
    const age = Math.floor(Date.now() / 1000) - parseInt(timestamp, 10);
    if (age > 300 || age < -300) return false;

    // Stripe signs: timestamp + "." + raw body
    const expected = crypto
        .createHmac('sha256', secret)
        .update(`${timestamp}.${rawBody}`, 'utf8')
        .digest('hex');

    // timingSafeEqual throws on length mismatch — compare hex lengths first
    return signatures.some(sig =>
        sig.length === expected.length &&
        crypto.timingSafeEqual(Buffer.from(sig, 'hex'), Buffer.from(expected, 'hex'))
    );
}

module.exports = { verifyWebhook };

// Demo: sign a payload in Stripe's format, then verify it
if (require.main === module) {
    const secret = 'whsec_test_secret';
    const body = '{"type":"payment_intent.succeeded"}';
    const t = Math.floor(Date.now() / 1000);
    const sig = crypto
        .createHmac('sha256', secret)
        .update(`${t}.${body}`, 'utf8')
        .digest('hex');
    const header = `t=${t},v1=${sig}`;
    console.log('header:', header);
    console.log('verify:', verifyWebhook(body, header, secret));          // true
    console.log('verify:', verifyWebhook(body, header, 'wrong-secret')); // false
}
