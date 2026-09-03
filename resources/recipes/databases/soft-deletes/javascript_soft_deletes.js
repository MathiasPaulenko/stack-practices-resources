// Soft deletes implementation with Sequelize (paranoid mode).
// Run: node javascript_soft_deletes.js
const { Sequelize, DataTypes, Model, Op } = require("sequelize");

const sequelize = new Sequelize({ dialect: "sqlite", storage: "soft_deletes.db" });

class User extends Model {}
class Post extends Model {}

User.init(
  {
    email: { type: DataTypes.STRING, allowNull: false },
    name: { type: DataTypes.STRING, allowNull: true },
    deletedAt: { type: DataTypes.DATE, allowNull: true },
    deletedBy: { type: DataTypes.STRING, allowNull: true },
  },
  { sequelize, modelName: "User", paranoid: true, deletedAt: "deletedAt" }
);

Post.init(
  {
    userId: { type: DataTypes.INTEGER, allowNull: false },
    title: { type: DataTypes.STRING, allowNull: false },
    body: { type: DataTypes.TEXT, allowNull: true },
    deletedAt: { type: DataTypes.DATE, allowNull: true },
    deletedBy: { type: DataTypes.STRING, allowNull: true },
  },
  { sequelize, modelName: "Post", paranoid: true, deletedAt: "deletedAt" }
);

Post.belongsTo(User, { foreignKey: "userId" });
User.hasMany(Post, { foreignKey: "userId" });

async function restoreUser(userId) {
  const user = await User.findByPk(userId, { paranoid: false });
  if (user && user.deletedAt !== null) {
    await user.restore();
    await Post.update(
      { deletedAt: null, deletedBy: null },
      { where: { userId }, paranoid: false }
    );
  }
  return user;
}

async function purgeOldSoftDeletes(days = 30) {
  const cutoff = new Date(Date.now() - days * 24 * 60 * 60 * 1000);
  const users = await User.destroy({
    where: { deletedAt: { [Op.ne]: null, [Op.lt]: cutoff } },
    force: true,
    paranoid: false,
  });
  await Post.destroy({
    where: { deletedAt: { [Op.ne]: null, [Op.lt]: cutoff } },
    force: true,
    paranoid: false,
  });
  return users;
}

async function main() {
  await sequelize.sync({ force: true });

  const user = await User.create({ email: "alice@example.com", name: "Alice" });
  console.log(`Created user: ${user.email}`);

  await user.destroy();
  console.log(`Soft-deleted user: ${user.email}`);

  const visible = await User.findAll();
  console.log(`Visible users: ${visible.length}`);

  await restoreUser(user.id);
  const restored = await User.findByPk(user.id);
  console.log(`Restored: ${restored ? restored.email : "not found"}`);

  const visibleAfter = await User.findAll();
  console.log(`Visible users after restore: ${visibleAfter.length}`);

  await user.destroy();
  // Set old deletedAt for purge test
  await User.update(
    { deletedAt: new Date(Date.now() - 31 * 24 * 60 * 60 * 1000) },
    { where: { id: user.id }, paranoid: false }
  );

  const purged = await purgeOldSoftDeletes(30);
  console.log(`Purged ${purged} old records`);

  await sequelize.close();
}

main().catch(console.error);
