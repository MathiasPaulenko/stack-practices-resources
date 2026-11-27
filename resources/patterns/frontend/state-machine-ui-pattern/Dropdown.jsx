// Dropdown.jsx — dropdown with proper state management
import { createMachine, assign } from 'xstate';
import { useMachine } from '@xstate/react';

const dropdownMachine = createMachine({
  id: 'dropdown',
  initial: 'closed',
  context: { selectedIndex: 0 },
  states: {
    closed: {
      on: {
        OPEN: 'open',
        TOGGLE: 'open',
      },
    },
    open: {
      on: {
        CLOSE: 'closed',
        TOGGLE: 'closed',
        SELECT: {
          target: 'closed',
          actions: assign({
            selectedIndex: (_, event) => event.index,
          }),
        },
        CLICK_OUTSIDE: 'closed',
        ESCAPE: 'closed',
      },
    },
  },
});

function Dropdown({ items }) {
  const [state, send] = useMachine(dropdownMachine);
  const selectedItem = items[state.context.selectedIndex];

  return (
    <div className="dropdown" tabIndex={0}>
      <button
        onClick={() => send('TOGGLE')}
        onKeyDown={(e) => e.key === 'Escape' && send('ESCAPE')}
      >
        {selectedItem.label} {state.matches('open') ? '▲' : '▼'}
      </button>

      {state.matches('open') && (
        <ul className="dropdown-menu">
          {items.map((item, index) => (
            <li
              key={item.id}
              onClick={() => send({ type: 'SELECT', index })}
            >
              {item.label}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
