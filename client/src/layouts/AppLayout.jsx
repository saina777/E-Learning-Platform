import { Outlet, Link } from "react-router-dom";

export default function AppLayout() {
  return (
    <div className="min-h-screen">
      <header className="border-b">
        <nav className="mx-auto max-w-6xl px-4 py-3 flex gap-4">
          <Link to="/" className="font-semibold">LearnFlow</Link>
          <Link to="/catalog">Catalog</Link>
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/studio">Studio</Link>
          <Link to="/settings">Settings</Link>
        </nav>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-6">
        <Outlet />
      </main>
    </div>
  );
}
