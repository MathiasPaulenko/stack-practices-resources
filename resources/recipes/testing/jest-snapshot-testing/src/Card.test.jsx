import { render } from '@testing-library/react';
import Card from './Card';

describe('Card', () => {
  const baseProps = {
    title: 'Test Card',
    description: 'A sample card for testing',
    imageUrl: '/test.jpg',
  };

  it('renders with all props', () => {
    const { container } = render(<Card {...baseProps} />);
    expect(container).toMatchSnapshot();
  });

  it('renders without image', () => {
    const { container } = render(
      <Card title={baseProps.title} description={baseProps.description} />
    );
    expect(container).toMatchSnapshot();
  });

  it('renders loading state', () => {
    const { container } = render(<Card loading title="Loading" />);
    expect(container).toMatchSnapshot();
  });
});
