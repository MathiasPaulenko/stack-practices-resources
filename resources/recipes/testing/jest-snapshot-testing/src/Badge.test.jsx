import { render } from "@testing-library/react";
import Badge from "./Badge";

describe("Badge", () => {
  it("renders status badge", () => {
    const { container } = render(<Badge status="active">Online</Badge>);
    expect(container.firstChild).toMatchInlineSnapshot(`
      <span
        class="badge badge--active"
      >
        Online
      </span>
    `);
  });
});
