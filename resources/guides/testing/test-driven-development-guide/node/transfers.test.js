// Test suite for POST /api/transfers from the guide's "TDD in Production" section.
//
// `app`, `getAccount` and `userToken` come from your application setup.
// Wire them in the beforeAll hook: build the Express app, seed the test
// accounts and obtain a token for `sourceAccountId`/`destinationAccountId`.
// Jest + supertest.

const request = require("supertest");

// --- replace these stubs with your app's wiring --------------------------
// const app = require("../src/app");
// const { getAccount } = require("../src/accounts");
// const { userToken } = require("./fixtures/auth");
const app = null;
const getAccount = async () => ({});
const userToken = "test-token";
const originalA = 500;
const originalB = 200;
const accountA = { id: "acc-a" };
const accountB = { id: "acc-b" };
const otherUserAccount = { id: "acc-foreign" };
// -------------------------------------------------------------------------

describe.skip("POST /api/transfers", () => {
  it("should transfer between same user accounts", async () => {
    const res = await request(app)
      .post("/api/transfers")
      .set("Authorization", `Bearer ${userToken}`)
      .send({
        sourceAccountId: accountA.id,
        destinationAccountId: accountB.id,
        amount: 100,
        currency: "USD",
      });
    expect(res.status).toBe(201);
    expect(res.body.status).toBe("completed");

    const src = await getAccount(accountA.id);
    const dst = await getAccount(accountB.id);
    expect(src.balance).toBe(originalA - 100);
    expect(dst.balance).toBe(originalB + 100);
  });

  it("should reject transfer to foreign account", async () => {
    const res = await request(app)
      .post("/api/transfers")
      .set("Authorization", `Bearer ${userToken}`)
      .send({
        sourceAccountId: accountA.id,
        destinationAccountId: otherUserAccount.id,
        amount: 100,
        currency: "USD",
      });
    expect(res.status).toBe(403);
  });

  it("should reject negative amount", async () => {
    const res = await request(app)
      .post("/api/transfers")
      .set("Authorization", `Bearer ${userToken}`)
      .send({
        sourceAccountId: accountA.id,
        destinationAccountId: accountB.id,
        amount: -50,
        currency: "USD",
      });
    expect(res.status).toBe(400);
  });
});
