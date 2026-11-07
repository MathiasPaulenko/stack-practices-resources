// Second domain: a nested navigation menu as a data tree.
// Same UINode idea — leaves are links, composites are groups.

type NavNode =
  | { type: 'link'; id: string; label: string; href: string }
  | { type: 'group'; id: string; label: string; children: NavNode[] };

export function NavItem({ node }: { node: NavNode }) {
  if (node.type === 'link') {
    return (
      <li key={node.id}>
        <a href={node.href}>{node.label}</a>
      </li>
    );
  }
  return (
    <li key={node.id} className="nav-group">
      <span>{node.label}</span>
      <ul>
        {node.children.map((child) => (
          <NavItem key={child.id} node={child} />
        ))}
      </ul>
    </li>
  );
}

export const navTree: NavNode = {
  type: 'group',
  id: 'root',
  label: 'Docs',
  children: [
    { type: 'link', id: 'intro', label: 'Introduction', href: '/docs/intro' },
    {
      type: 'group',
      id: 'patterns',
      label: 'Patterns',
      children: [
        { type: 'link', id: 'composite', label: 'Composite', href: '/patterns/composite' },
        { type: 'link', id: 'decorator', label: 'Decorator', href: '/patterns/decorator' },
      ],
    },
    { type: 'link', id: 'api', label: 'API Reference', href: '/api' },
  ],
};

export function Sidebar() {
  return (
    <nav>
      <ul>
        <NavItem node={navTree} />
      </ul>
    </nav>
  );
}
