// Firestore write from the GCP Basics guide.
// Uses the modular Firebase web SDK — works in browsers and Node 18+.
// npm install firebase

import { getFirestore, doc, setDoc } from 'firebase/firestore';

const db = getFirestore();
await setDoc(doc(db, 'users', 'user-1'), {
  name: 'Alice',
  email: 'alice@example.com',
});
