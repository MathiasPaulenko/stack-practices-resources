import { render } from '@testing-library/react';
import Dashboard from './Dashboard';

jest.mock('./lib/Chart');

describe('Dashboard', () => {
  it('replaces the third-party chart with a stable stub', () => {
    const { container } = render(<Dashboard series={[4, 8, 15]} />);
    expect(container.firstChild).toMatchSnapshot();
  });
});
