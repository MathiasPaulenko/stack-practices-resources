import "server-only";

// In-memory stand-in for a database client — imagine Prisma here.
// Every method is async to mimic real I/O latency, so Server Components can
// await data during render exactly like they would against Postgres.
// The call signatures deliberately mirror Prisma's ({ where }, { data }, ...)
// so swapping the bodies for a real client is a mechanical change.

export type Product = {
  id: string;
  name: string;
  description: string;
  price: number;
  image: string;
  published: boolean;
  likeCount: number;
  createdAt: Date;
};

export type NewProduct = {
  name: string;
  price: number;
  description: string;
  image: string;
};

export type Review = {
  id: string;
  productId: string;
  authorName: string;
  rating: number;
  text: string;
  createdAt: Date;
};

export type Like = {
  id: string;
  productId: string;
  userId: string;
};

export type CatalogStats = {
  totalProducts: number;
  totalReviews: number;
  totalLikes: number;
};

const latency = (ms = 60) =>
  new Promise((resolve) => setTimeout(resolve, ms));

const products: Product[] = [
  {
    id: "prod-1",
    name: "Aurora Mechanical Keyboard",
    description:
      "Hot-swappable 75% board with tactile switches and PBT keycaps.",
    price: 129.99,
    image: "https://picsum.photos/seed/aurora-kb/600/400",
    published: true,
    likeCount: 24,
    createdAt: new Date("2026-01-15"),
  },
  {
    id: "prod-2",
    name: "Nimbus Headphones",
    description:
      "Over-ear ANC headphones with 40h battery and multipoint Bluetooth.",
    price: 249,
    image: "https://picsum.photos/seed/nimbus-hp/600/400",
    published: true,
    likeCount: 58,
    createdAt: new Date("2026-01-22"),
  },
  {
    id: "prod-3",
    name: "Drift Ergonomic Chair",
    description:
      "Mesh-back task chair with adjustable lumbar support and 4D armrests.",
    price: 449.5,
    image: "https://picsum.photos/seed/drift-chair/600/400",
    published: true,
    likeCount: 41,
    createdAt: new Date("2026-02-01"),
  },
  {
    id: "prod-4",
    name: "Lumen Desk Lamp",
    description: "Dimmable LED lamp with a wireless charging base.",
    price: 59.99,
    image: "https://picsum.photos/seed/lumen-lamp/600/400",
    published: true,
    likeCount: 12,
    createdAt: new Date("2026-02-08"),
  },
  {
    id: "prod-5",
    name: "Vertex USB-C Hub",
    description: "7-in-1 hub: HDMI, SD, Ethernet, and 100W passthrough.",
    price: 79,
    image: "https://picsum.photos/seed/vertex-hub/600/400",
    published: true,
    likeCount: 33,
    createdAt: new Date("2026-02-14"),
  },
  {
    id: "prod-6",
    name: "Pulse Smart Bottle",
    description:
      "Insulated bottle that tracks hydration and glows when it's time to drink.",
    price: 34.95,
    image: "https://picsum.photos/seed/pulse-bottle/600/400",
    published: true,
    likeCount: 9,
    createdAt: new Date("2026-02-20"),
  },
  {
    id: "prod-7",
    name: "Atlas Monitor Stand",
    description:
      "Gas-spring stand for ultrawide monitors — still a draft, not published.",
    price: 89,
    image: "https://picsum.photos/seed/atlas-stand/600/400",
    published: false,
    likeCount: 0,
    createdAt: new Date("2026-03-01"),
  },
];

const reviews: Review[] = [
  {
    id: "rev-1",
    productId: "prod-1",
    authorName: "Priya N.",
    rating: 5,
    text: "Switches feel crisp and the build quality is excellent.",
    createdAt: new Date("2026-02-01"),
  },
  {
    id: "rev-2",
    productId: "prod-1",
    authorName: "Tom W.",
    rating: 4,
    text: "Great keyboard, slightly heavy for travel.",
    createdAt: new Date("2026-02-10"),
  },
  {
    id: "rev-3",
    productId: "prod-2",
    authorName: "Ana G.",
    rating: 5,
    text: "Noise cancelling is legit — I focused through a whole flight.",
    createdAt: new Date("2026-01-28"),
  },
  {
    id: "rev-4",
    productId: "prod-3",
    authorName: "Marco S.",
    rating: 4,
    text: "Lumbar support is the best I've tried in this price range.",
    createdAt: new Date("2026-02-05"),
  },
  {
    id: "rev-5",
    productId: "prod-3",
    authorName: "Lena K.",
    rating: 3,
    text: "Assembly took a while but the result is solid.",
    createdAt: new Date("2026-02-12"),
  },
];

// Per-user like records. product.likeCount stays the denormalized total.
const likes: Like[] = [];
let likeSequence = 0;
let productSequence = products.length;

export const db = {
  product: {
    async findMany(args?: {
      where?: { published?: boolean };
      orderBy?: { createdAt?: "asc" | "desc" };
      take?: number;
    }): Promise<Product[]> {
      await latency();
      let result = [...products];
      const published = args?.where?.published;
      if (published !== undefined) {
        result = result.filter((p) => p.published === published);
      }
      const direction = args?.orderBy?.createdAt === "asc" ? 1 : -1;
      result.sort(
        (a, b) => direction * (a.createdAt.getTime() - b.createdAt.getTime())
      );
      if (args?.take) result = result.slice(0, args.take);
      return result;
    },

    async findUnique(args: {
      where: { id: string };
    }): Promise<Product | null> {
      await latency(40);
      return products.find((p) => p.id === args.where.id) ?? null;
    },

    async create(args: { data: NewProduct }): Promise<Product> {
      await latency(120);
      const product: Product = {
        id: `prod-${++productSequence}`,
        ...args.data,
        published: true,
        likeCount: 0,
        createdAt: new Date(),
      };
      products.unshift(product);
      return product;
    },

    async update(args: {
      where: { id: string };
      data: { likeCount?: number | { increment: number } };
    }): Promise<Product> {
      await latency(40);
      const product = products.find((p) => p.id === args.where.id);
      if (!product) throw new Error(`Product ${args.where.id} not found`);
      const likeCount = args.data.likeCount;
      if (typeof likeCount === "number") {
        product.likeCount = likeCount;
      } else if (likeCount) {
        product.likeCount += likeCount.increment;
      }
      return product;
    },

    async delete(args: { where: { id: string } }): Promise<Product> {
      await latency(80);
      const index = products.findIndex((p) => p.id === args.where.id);
      if (index === -1) {
        throw new Error(`Product ${args.where.id} not found`);
      }
      const [removed] = products.splice(index, 1);
      return removed;
    },
  },

  review: {
    async findMany(args: {
      where: { productId: string };
      orderBy?: { createdAt?: "asc" | "desc" };
      take?: number;
    }): Promise<Review[]> {
      await latency(90);
      let result = reviews.filter((r) => r.productId === args.where.productId);
      const direction = args?.orderBy?.createdAt === "asc" ? 1 : -1;
      result.sort(
        (a, b) => direction * (a.createdAt.getTime() - b.createdAt.getTime())
      );
      if (args?.take) result = result.slice(0, args.take);
      return result;
    },
  },

  like: {
    async findFirst(args: {
      where: { productId: string; userId: string };
    }): Promise<Like | null> {
      await latency(30);
      return (
        likes.find(
          (l) =>
            l.productId === args.where.productId &&
            l.userId === args.where.userId
        ) ?? null
      );
    },

    async create(args: {
      data: { productId: string; userId: string };
    }): Promise<Like> {
      await latency(60);
      const like: Like = {
        id: `like-${++likeSequence}`,
        ...args.data,
      };
      likes.push(like);
      return like;
    },

    async delete(args: { where: { id: string } }): Promise<Like> {
      await latency(60);
      const index = likes.findIndex((l) => l.id === args.where.id);
      if (index === -1) throw new Error(`Like ${args.where.id} not found`);
      const [removed] = likes.splice(index, 1);
      return removed;
    },
  },

  stats: {
    async findFirst(): Promise<CatalogStats> {
      // Slowest query on purpose — makes the per-section Suspense streaming
      // visible when you run the dev server.
      await latency(160);
      return {
        totalProducts: products.filter((p) => p.published).length,
        totalReviews: reviews.length,
        totalLikes: products.reduce((sum, p) => sum + p.likeCount, 0),
      };
    },
  },
};
