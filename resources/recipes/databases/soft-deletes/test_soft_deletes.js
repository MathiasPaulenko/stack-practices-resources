// Tests for soft deletes with Sequelize.
// Run: npx jest test_soft_deletes.js
const { Sequelize, DataTypes, Model, Op } = require("sequelize");

let sequelize;
let User;
let Post;

beforeAll(async () => {
  sequelize = new Sequelize({ dialect: "sqlite", storage: ":memory:" });
  User = require("./javascript_soft_deletes").User;
  Post = require("./javascript_soft_deletes").Post;
  // Re-init with test database
  User.init(
    {
      email: { type: DataTypes.STRING, allowNull: false },
      name: { type: DataTypes.STRING, allowNull: true },
      deletedAt: { type: DataTypes.DATE, allowNull: true },
      deletedBy: { type: DataTypes.STRING, allowNull: true },
    },
    { sequelize, modelName: "User", paranoid: true, deletedAt: "deletedAt" }
  );
  await sequelize.sync({ force: true });
});

afterAll(async () => {
  await sequelize.close();
});

test("soft-deleted user excluded from findAll", async () => {
  const user = await User.create({ email: "test@example.com", name: "Test" });
  await user.destroy();

  const visible = await User.findAll();
  expect(visible).toHaveLength(0);
});

test("restore soft-deleted user", async () => {
  const user = await User.create({ email: "restore@example.com" });
  await user.destroy();

  await user.restore();
  const found = await User.findByPk(user.id);
  expect(found).not.toBeNull();
  expect(found.deletedAt).toBeNull();
});

test("purge only old records", async () => {
  const user = await User.create({ email: "purge@example.com" });
  await user.destroy();

  // Set old deletedAt
  await User.update(
    { deletedAt: new Date(Date.now() - 31 * 24 * 60 * 60 * 1000) },
    { where: { id: user.id }, paranoid: false }
  );

  const purged = await User.destroy({
    where: { deletedAt: { [Op.ne]: null, [Op.lt]: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000) } },
    force: true,
    paranoid: false,
  });

  expect(purged).toBe(1);
  const stillThere = await User.findByPk(user.id, { paranoid: false });
  expect(stillThere).toBeNull();
});
