// scalars.ts — Custom GraphQL scalar for email validation.
// Requires: graphql (for GraphQLScalarType in production)
// This file exports a dependency-free email validator for testing.

export function isValidEmail(value: string): boolean {
  return typeof value === "string" && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

export function normalizeEmail(value: string): string {
  return value.toLowerCase().trim();
}

// In production with the graphql package installed, use:
//
// import { GraphQLScalarType, GraphQLError } from "graphql";
//
// export const EmailScalar = new GraphQLScalarType({
//   name: "Email",
//   description: "A validated email address",
//   parseValue: (value: string) => {
//     if (!isValidEmail(value)) {
//       throw new GraphQLError("Invalid email format", {
//         extensions: { code: "INVALID_EMAIL", field: "email" },
//       });
//     }
//     return normalizeEmail(value);
//   },
//   parseLiteral: (ast: any) => {
//     if (ast.kind !== "StringValue") {
//       throw new GraphQLError("Email must be a string", {
//         extensions: { code: "INVALID_TYPE" },
//       });
//     }
//     if (!isValidEmail(ast.value)) {
//       throw new GraphQLError("Invalid email format", {
//         extensions: { code: "INVALID_EMAIL" },
//       });
//     }
//     return normalizeEmail(ast.value);
//   },
//   serialize: (value: string) => value,
// });
