// The server-only package ships no TypeScript declarations; this ambient
// module keeps `tsc --noEmit` happy. The runtime guard still works: importing
// these modules from a Client Component fails the build.
declare module "server-only";
