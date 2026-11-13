// review.mjs — automated subset of the GraphQL schema review checklist.
// Parses SDL directly (graphql-js `parse`) so deprecation reasons and
// argument lists are checked against what the author actually wrote.
//
// Usage: node review.mjs <schema-file.graphqls>

import { readFileSync } from 'node:fs';
import { parse } from 'graphql';

const PASCAL = /^[A-Z][a-zA-Z0-9]*$/;
const CAMEL = /^[a-z][a-zA-Z0-9]*$/;
const UPPER_SNAKE = /^[A-Z][A-Z0-9_]*$/;
const MUTATION_VERBS = ['create', 'update', 'delete', 'archive', 'restore', 'add', 'remove'];
const PAGINATION_ARGS = new Set(['first', 'after', 'last', 'before']);

const unwrap = (t) => (t.kind === 'NamedType' ? t.name.value : unwrap(t.type));
const isList = (t) => t.kind === 'ListType' || (t.kind === 'NonNullType' && isList(t.type));
const typeName = (t) => unwrap(t);

export function reviewSchema(sdl) {
  const doc = parse(sdl);
  const failures = [];

  const types = new Map();
  for (const def of doc.definitions) {
    if (def.name) types.set(def.name.value, def);
  }
  const payloadNames = new Set(
    [...types.values()]
      .filter((d) => d.kind === 'ObjectTypeDefinition' && d.name.value.endsWith('Payload'))
      .map((d) => d.name.value)
  );

  const fail = (check, where, msg) => failures.push({ check, where, msg });

  for (const def of doc.definitions) {
    const kind = def.kind;
    if (!['ObjectTypeDefinition', 'InterfaceTypeDefinition', 'InputObjectTypeDefinition', 'EnumTypeDefinition'].includes(kind)) continue;
    const name = def.name.value;
    if (name.startsWith('__') || ['Query', 'Mutation', 'Subscription'].includes(name)) {
      // Root types are exempt from naming rules but still get field checks.
    } else if (!PASCAL.test(name)) {
      fail('type-names-pascal', name, `type name "${name}" is not PascalCase`);
    }

    if (kind === 'EnumTypeDefinition') {
      for (const v of def.values ?? []) {
        if (!UPPER_SNAKE.test(v.name.value)) {
          fail('enum-upper-snake', `${name}.${v.name.value}`, `enum value "${v.name.value}" is not UPPER_SNAKE_CASE`);
        }
      }
      continue;
    }

    for (const field of def.fields ?? []) {
      const fname = field.name.value;
      const where = `${name}.${fname}`;

      if (!CAMEL.test(fname)) {
        fail('field-names-camel', where, `field name "${fname}" is not camelCase`);
      }
      const tname = typeName(field.type);
      if (tname === 'Boolean' && !/^(is|has|can)/.test(fname)) {
        fail('boolean-verb-prefix', where, `Boolean field "${fname}" should start with is/has/can`);
      }
      if (fname === 'id' && tname !== 'ID') {
        fail('id-uses-id-type', where, `field "id" typed ${tname}, expected ID`);
      }

      const deprecated = (field.directives ?? []).find((d) => d.name.value === 'deprecated');
      if (deprecated) {
        const reason = deprecated.arguments?.find((a) => a.name.value === 'reason');
        if (!reason) {
          fail('deprecated-needs-reason', where, '@deprecated without a reason argument');
        }
      }

      if (name === 'Query' && isList(field.type)) {
        const argNames = new Set((field.arguments ?? []).map((a) => a.name.value));
        const hasPagination = [...argNames].some((a) => PAGINATION_ARGS.has(a));
        if (!hasPagination) {
          fail('list-needs-pagination', where, 'list field on Query has no cursor pagination args (first/after/last/before)');
        }
        if (argNames.has('offset')) {
          fail('no-offset-pagination', where, 'offset pagination on a Query list field');
        }
      }

      if (name === 'Mutation') {
        const verbOk = MUTATION_VERBS.some((v) => fname.startsWith(v));
        if (!verbOk) {
          fail('mutation-verb', where, `mutation "${fname}" does not start with a known verb`);
        }
        const args = field.arguments ?? [];
        const singleInput = args.length === 1 && args[0].name.value === 'input';
        if (!singleInput) {
          fail('mutation-single-input', where, 'mutation should take a single "input" argument');
        }
        if (!payloadNames.has(tname)) {
          fail('mutation-returns-payload', where, `mutation returns ${tname}, expected a *Payload type`);
        }
      }
    }
  }

  // Payload types must expose userErrors
  for (const def of doc.definitions) {
    if (def.kind !== 'ObjectTypeDefinition' || !def.name.value.endsWith('Payload')) continue;
    const hasErrors = (def.fields ?? []).some((f) => f.name.value === 'userErrors');
    if (!hasErrors) {
      fail('payload-user-errors', def.name.value, 'payload type lacks a userErrors field');
    }
  }

  return failures;
}

export function formatReport(failures) {
  if (failures.length === 0) return 'PASS: all automated checks passed';
  return failures.map((f) => `FAIL [${f.check}] ${f.where}: ${f.msg}`).join('\n');
}

// Run as CLI
if (process.argv[1] && process.argv[1].endsWith('review.mjs')) {
  const file = process.argv[2];
  if (!file) {
    console.error('Usage: node review.mjs <schema.graphqls>');
    process.exit(2);
  }
  const sdl = readFileSync(file, 'utf-8');
  const failures = reviewSchema(sdl);
  console.log(formatReport(failures));
  process.exit(failures.length ? 1 : 0);
}
