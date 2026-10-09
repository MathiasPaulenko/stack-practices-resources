// Generate URL-friendly slugs from arbitrary strings.
// Zero dependencies: String.normalize('NFKD') + regex.

function generateSlug(text) {
    return text
        .normalize('NFKD')
        .replace(/[\u0300-\u036f]/g, '')  // Remove diacritics
        .toLowerCase()
        .trim()
        .replace(/[^\w\s-]/g, '')
        .replace(/[-\s]+/g, '-')
        .replace(/^-+|-+$/g, '');         // Trim edge hyphens
}

console.log(generateSlug('Hello, World! 2024'));    // hello-world-2024
console.log(generateSlug('Café & Crème Brûlée'));   // cafe-creme-brulee

// Variant with configurable options
function generateSlugWithOptions(text, options = {}) {
    const {
        replacement = '-',
        remove = /[^\w\s-]/g,
        lower = true,
        strict = true,
    } = options;

    let result = text
        .normalize('NFKD')
        .replace(/[\u0300-\u036f]/g, '')
        .replace(remove, '')
        .trim()
        .replace(/[-\s]+/g, replacement);

    if (lower) result = result.toLowerCase();
    if (strict) result = result.replace(/[^a-z0-9-]/g, '');

    return result;
}

console.log(generateSlugWithOptions('My Post: Part 2!'));  // my-post-part-2
