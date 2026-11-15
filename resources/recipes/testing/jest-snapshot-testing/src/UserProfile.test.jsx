import { render, screen } from '@testing-library/react';
import UserProfile from './UserProfile';

describe('UserProfile', () => {
  it('matches snapshot for active user', () => {
    const user = {
      name: 'Alice Johnson',
      email: 'alice@example.com',
      role: 'admin',
      avatar: '/avatars/alice.jpg',
    };

    const { asFragment } = render(<UserProfile user={user} />);
    expect(asFragment()).toMatchSnapshot();
  });

  it('matches snapshot for loading state', () => {
    const { asFragment } = render(<UserProfile loading />);
    expect(asFragment()).toMatchSnapshot();
  });
});
