import {
  Kind,
  parseValue,
  type IntValueNode,
  type ObjectValueNode,
} from 'graphql';
import { DateScalar } from './scalars/Date.js';
import { EmailScalar } from './scalars/Email.js';
import { JSONScalar } from './scalars/JSON.js';
import { URLScalar } from './scalars/URL.js';
import { PositiveIntScalar } from './scalars/PositiveInt.js';

function check(label: string, fn: () => unknown) {
  try {
    console.log(`OK   ${label} ->`, fn());
  } catch (err) {
    console.log(`FAIL ${label} ->`, (err as Error).message);
  }
}

console.log('--- serialize (server -> client) ---');
check('DateScalar.serialize(new Date("2026-01-15T10:30:00Z"))', () =>
  DateScalar.serialize(new Date('2026-01-15T10:30:00Z'))
);
check('EmailScalar.serialize("USER@EXAMPLE.COM")', () =>
  EmailScalar.serialize('USER@EXAMPLE.COM')
);
check('EmailScalar.serialize(12345)', () => EmailScalar.serialize(12345));

console.log('--- parseValue (client variable -> server) ---');
check('DateScalar.parseValue("2026-01-15")', () => DateScalar.parseValue('2026-01-15'));
check('DateScalar.parseValue("not a date")', () => DateScalar.parseValue('not a date'));
check('EmailScalar.parseValue("User@Example.COM")', () =>
  EmailScalar.parseValue('User@Example.COM')
);
check('URLScalar.parseValue("ftp://files.example.com")', () =>
  URLScalar.parseValue('ftp://files.example.com')
);
check('URLScalar.parseValue("https://stackpractices.com")', () =>
  URLScalar.parseValue('https://stackpractices.com')
);
check('PositiveIntScalar.parseValue(0)', () => PositiveIntScalar.parseValue(0));
check('PositiveIntScalar.parseValue(42)', () => PositiveIntScalar.parseValue(42));

console.log('--- parseLiteral (inline AST -> server) ---');
check('JSONScalar.parseLiteral(object literal)', () =>
  JSONScalar.parseLiteral!(
    parseValue('{ tags: ["a", "b"], count: 2, active: true }') as ObjectValueNode,
    {}
  )
);
check('DateScalar.parseLiteral(Int node)', () =>
  DateScalar.parseLiteral!({ kind: Kind.INT, value: '42' } as IntValueNode, {})
);
