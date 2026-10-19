// Unit test with @open-wc/testing — runs in a real browser via Web Test Runner.
//   npm i -D @web/test-runner @open-wc/testing
//   npx web-test-runner test/ --node-resolve
import { fixture, expect } from '@open-wc/testing';
import '../src/user-card.js';

describe('user-card', () => {
  it('renders the name attribute inside the shadow root', async () => {
    const el = await fixture('<user-card name="Ada"></user-card>');
    expect(el.shadowRoot.querySelector('.name').textContent).to.equal('Ada');
  });

  it('re-renders when an observed attribute changes', async () => {
    const el = await fixture('<user-card name="Ada"></user-card>');
    el.setAttribute('name', 'Grace');
    expect(el.shadowRoot.querySelector('.name').textContent).to.equal('Grace');
  });

  it('dispatches a composed user-selected event', async () => {
    const el = await fixture('<user-card name="Ada" user-id="u-7"></user-card>');
    let received = null;
    document.addEventListener('user-selected', (e) => (received = e.detail), {
      once: true,
    });
    el.shadowRoot.querySelector('button').click();
    expect(received.userId).to.equal('u-7');
  });
});
