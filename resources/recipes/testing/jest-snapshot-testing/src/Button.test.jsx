import { render } from '@testing-library/react';
import Button from './Button';

describe('Button', () => {
  it('renders correctly with default props', () => {
    const { container } = render(<Button>Click me</Button>);
    expect(container.firstChild).toMatchSnapshot();
  });

  it('renders correctly with variant prop', () => {
    const { container } = render(<Button variant="danger">Delete</Button>);
    expect(container.firstChild).toMatchSnapshot();
  });

  it('renders correctly when disabled', () => {
    const { container } = render(<Button disabled>Loading</Button>);
    expect(container.firstChild).toMatchSnapshot();
  });
});
