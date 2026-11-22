// Model-View-Presenter: testable UI logic without a UI framework.
// The View is an interface the GUI implements; the Presenter talks only to
// that interface, so a fake view can drive it in tests.
import test from 'node:test';
import assert from 'node:assert/strict';

class UserRepository {
  constructor(users) {
    this.users = new Map(users.map((u) => [u.id, u]));
  }

  findById(userId) {
    return this.users.get(userId);
  }
}

// In JS the "interface" is a contract: the view must implement these methods.
// A real screen implements them; tests use a fake that records calls.
class UserDetailPresenter {
  constructor(view, repository) {
    this.view = view;
    this.repository = repository;
  }

  onLoadClicked(userId) {
    if (!Number.isInteger(userId) || userId <= 0) {
      this.view.showError('Enter a valid user id');
      return;
    }
    this.view.showLoading();
    try {
      const user = this.repository.findById(userId);
      if (!user) {
        this.view.showError('User not found');
      } else {
        this.view.showUser(user.name, user.email);
      }
    } finally {
      this.view.hideLoading();
    }
  }
}

class FakeView {
  constructor() {
    this.calls = [];
  }

  showLoading() {
    this.calls.push('showLoading');
  }

  hideLoading() {
    this.calls.push('hideLoading');
  }

  showUser(name, email) {
    this.calls.push(`showUser:${name}:${email}`);
  }

  showError(message) {
    this.calls.push(`showError:${message}`);
  }
}

function makePresenter() {
  const repo = new UserRepository([{ id: 1, name: 'Ada', email: 'ada@example.com' }]);
  const view = new FakeView();
  return { presenter: new UserDetailPresenter(view, repo), view };
}

test('loads and shows the user', () => {
  const { presenter, view } = makePresenter();
  presenter.onLoadClicked(1);
  assert.ok(view.calls.includes('showUser:Ada:ada@example.com'));
});

test('shows an error for a missing user', () => {
  const { presenter, view } = makePresenter();
  presenter.onLoadClicked(99);
  assert.ok(view.calls.includes('showError:User not found'));
});

test('validates input without touching the repository', () => {
  const { presenter, view } = makePresenter();
  presenter.onLoadClicked(0);
  assert.ok(view.calls.includes('showError:Enter a valid user id'));
  assert.ok(!view.calls.includes('showLoading'));
});

test('loading indicators wrap the lookup', () => {
  const { presenter, view } = makePresenter();
  presenter.onLoadClicked(1);
  assert.deepEqual(view.calls, [
    'showLoading',
    'showUser:Ada:ada@example.com',
    'hideLoading',
  ]);
});

test('loading is hidden on error', () => {
  const { presenter, view } = makePresenter();
  presenter.onLoadClicked(99);
  assert.equal(view.calls.at(-1), 'hideLoading');
});
