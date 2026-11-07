// tests/components/Card.snapshot.test.tsx — Snapshot testing
import { describe, it, expect } from "vitest";
import { render } from "@testing-library/react";
import { Card } from "@/components/Card";

describe("Card snapshots", () => {
  it("matches snapshot with content", () => {
    const { container } = render(
      <Card title="Test Title" description="Test Description" />
    );
    expect(container.firstChild).toMatchSnapshot();
  });

  it("matches snapshot with image", () => {
    const { container } = render(
      <Card title="With Image" image="/test.jpg" />
    );
    expect(container.firstChild).toMatchSnapshot();
  });

  it("matches inline snapshot", () => {
    const { container } = render(<Card title="Inline" />);
    expect(container.firstChild).toMatchInlineSnapshot(`
      <div
        class="card"
      >
        <h3>
          Inline
        </h3>
      </div>
    `);
  });
});
