import Link from "next/link";

export default function NotFound() {
  return (
    <div className="mx-auto max-w-2xl space-y-4 p-6">
      <h1 className="text-2xl font-bold">Page not found</h1>
      <p className="text-zinc-600">
        The page you are looking for does not exist or was moved.
      </p>
      <Link href="/" className="text-blue-600 hover:underline">
        Back to home
      </Link>
    </div>
  );
}
