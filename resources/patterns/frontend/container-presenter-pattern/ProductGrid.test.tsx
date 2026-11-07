// ProductGrid.test.tsx — presenter tested in isolation, no network mocking.
import { render, screen, fireEvent } from '@testing-library/react';
import { ProductGrid } from './ProductGrid';

const mockProducts = [
  { id: 1, name: 'Keyboard', image: '/kb.png', price: 79 },
  { id: 2, name: 'Mouse', image: '/ms.png', price: 39 },
];

const props = {
  products: mockProducts,
  loading: false,
  error: null,
  onAddToCart: jest.fn(),
};

describe('ProductGrid', () => {
  beforeEach(() => props.onAddToCart.mockClear());

  it('renders every product', () => {
    render(<ProductGrid {...props} />);
    expect(screen.getByText('Keyboard')).toBeInTheDocument();
    expect(screen.getByText('Mouse')).toBeInTheDocument();
  });

  it('shows loading state', () => {
    render(<ProductGrid {...props} loading={true} />);
    expect(screen.getByText('Loading products...')).toBeInTheDocument();
  });

  it('shows error message', () => {
    render(<ProductGrid {...props} error="Network error" />);
    expect(screen.getByText('Network error')).toBeInTheDocument();
  });

  it('forwards the product id to onAddToCart', () => {
    render(<ProductGrid {...props} />);
    fireEvent.click(screen.getAllByText('Add to Cart')[0]);
    expect(props.onAddToCart).toHaveBeenCalledWith(1);
  });
});
