// Composite Pattern for UI trees: a discriminated-union node tree
// rendered by one recursive component.
// The tree is plain data — serialize it, POST it, version it.

export type UINode =
  | { type: 'field'; id: string; label: string; inputType: string }
  | { type: 'section'; id: string; title: string; children: UINode[] };

export function Node({ node }: { node: UINode }) {
  if (node.type === 'field') {
    return (
      <div className="field" key={node.id}>
        <label>{node.label}</label>
        <input type={node.inputType} />
      </div>
    );
  }
  return (
    <fieldset className="section" key={node.id}>
      <legend>{node.title}</legend>
      {node.children.map((child) => (
        <Node key={child.id} node={child} />
      ))}
    </fieldset>
  );
}

export function FormBuilder({ tree }: { tree: UINode }) {
  return (
    <form>
      <Node node={tree} />
    </form>
  );
}
