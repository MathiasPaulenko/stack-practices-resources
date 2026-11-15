import { render } from '@testing-library/react';
import LastLogin from './LastLogin';

describe('LastLogin', () => {
  beforeEach(() => {
    jest.useFakeTimers().setSystemTime(new Date('2026-01-15T09:30:00Z'));
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  it('renders a stable timestamp', () => {
    const { container } = render(<LastLogin userId={7} />);
    expect(container.firstChild).toMatchSnapshot();
  });
});
