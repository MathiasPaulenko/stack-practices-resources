export function greet(name = "pipeline") {
  return `hello, ${name}`;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  console.log(greet("gitlab-ci"));
}
