// flyweight_javascript.js — Flyweight pattern implementation in JavaScript.
// Run: node flyweight_javascript.js

class TreeType {
  static cache = new Map();

  constructor(species, color, texture) {
    this.species = species;
    this.color = color;
    this.texture = texture;
  }

  static get(species, color, texture) {
    const key = `${species}|${color}|${texture}`;
    if (!TreeType.cache.has(key)) {
      TreeType.cache.set(key, new TreeType(species, color, texture));
    }
    return TreeType.cache.get(key);
  }

  static get cacheSize() {
    return TreeType.cache.size;
  }

  render(x, y) {
    return `Rendering ${this.species} at (${x}, ${y}) color=${this.color}`;
  }
}

class Tree {
  constructor(x, y, treeType) {
    this.x = x;
    this.y = y;
    this.treeType = treeType;
  }

  render() {
    return this.treeType.render(this.x, this.y);
  }
}

function buildForest(n = 1000) {
  const treeType = TreeType.get("Oak", "green", "bark.png");
  return Array.from({ length: n }, (_, i) => new Tree(i, i, treeType));
}

function buildMixedForest(n = 3000) {
  const types = [
    TreeType.get("Oak", "green", "bark.png"),
    TreeType.get("Pine", "dark", "pine.png"),
    TreeType.get("Birch", "light", "birch.png"),
  ];
  return Array.from({ length: n }, (_, i) => new Tree(i, i, types[i % types.length]));
}

if (require.main === module) {
  const forest = buildForest(1000);
  console.log(forest[0].render());
  console.log(forest[999].render());
  console.log(`Unique tree types: ${TreeType.cacheSize}`);

  const mixed = buildMixedForest(3000);
  console.log(`\nMixed forest: ${mixed.length} trees, ${TreeType.cacheSize} unique types`);
}

module.exports = { TreeType, Tree, buildForest, buildMixedForest };
