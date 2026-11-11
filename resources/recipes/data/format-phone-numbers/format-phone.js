// Phone number parsing, validation and formatting with libphonenumber-js.
// Install: npm install libphonenumber-js
// Run:     node format-phone.js

import { parsePhoneNumberFromString, AsYouType } from "libphonenumber-js";

function parseAndFormat(raw, region = "US") {
  const phone = parsePhoneNumberFromString(raw, region);
  if (!phone) return { raw, error: "unparseable input" };

  return {
    raw,
    possible: phone.isPossible(),
    valid: phone.isValid(),
    e164: phone.number,
    international: phone.formatInternational(),
    national: phone.formatNational(),
    uri: phone.getURI(),
    extension: phone.ext || null,
    type: phone.getType(),
  };
}

const samples = [
  ["(415) 555-2671", "US"],
  ["020 7946 0958", "GB"],
  ["+52 55 1234 5678", "MX"],
  ["+1 555-1234 ext. 42", "US"],
  ["not a number", "US"],
];

for (const [raw, region] of samples) {
  console.log(`'${raw}' [${region}] ->`);
  const result = parseAndFormat(raw, region);
  for (const [key, value] of Object.entries(result)) {
    if (key !== "raw") console.log(`    ${key}: ${value}`);
  }
  console.log();
}

// As-you-type formatting for live inputs.
const formatter = new AsYouType("US");
let formatted = "";
for (const ch of "4155552671") formatted = formatter.input(ch);
console.log(`As-you-type: 4155552671 -> ${formatted}`);
