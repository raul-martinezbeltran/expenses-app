import { Link, useNavigate } from "react-router";
import { useEffect, useState } from "react";
import { clearAuthTokens } from "../../utils/auth";

const navItemStyle =
  "inline-flex w-full items-center rounded-xl px-4 py-3 text-sm font-medium text-gray-700 transition-colors duration-200 hover:bg-gray-100 hover:text-gray-900";

const logoutButtonStyle =
  "inline-flex w-full items-center rounded-xl border border-gray-200 px-4 py-3 text-sm font-medium text-gray-700 transition-colors duration-200 hover:bg-gray-100 hover:text-gray-900";

export default function Navbar() {
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);

  useEffect(() => {
    document.body.style.overflow = open ? "hidden" : "";
    return () => {
      document.body.style.overflow = "";
    };
  }, [open]);

  const handleLogout = () => {
    clearAuthTokens();
    setOpen(false);
    navigate("/login", { replace: true });
  };

  const handleCloseMenu = () => {
    setOpen(false);
  };

  return (
    <>
      <nav className="hidden md:fixed md:left-0 md:top-0 md:z-40 md:flex md:h-screen md:w-64 md:flex-col md:border-r md:border-gray-200 md:bg-white md:px-4 md:py-6">
        <div>
          <p className="px-4 text-xs font-semibold uppercase tracking-[0.2em] text-gray-500">
            PlaceHolder
          </p>

          <div className="mt-6 flex flex-col gap-2">
            <Link to="/" className={navItemStyle}>
              Home
            </Link>
            <Link to="/expenses" className={navItemStyle}>
              Expenses
            </Link>
            <Link to="/create_expense" className={navItemStyle}>
              Create Expense
            </Link>
          </div>
        </div>

        <div className="mt-auto pt-6">
          <button
            type="button"
            onClick={handleLogout}
            className={logoutButtonStyle}
          >
            Logout
          </button>
        </div>
      </nav>

      {!open && (
        <div className="sticky top-0 z-50 flex items-center justify-end border-b border-gray-200 bg-white px-4 py-4 md:hidden">
          <button
            type="button"
            onClick={() => setOpen(true)}
            className="inline-flex items-center rounded-xl border border-gray-200 px-3 py-2 text-sm font-medium text-gray-700 transition-colors duration-200 hover:bg-gray-100 hover:text-gray-900"
            aria-label="Toggle navigation menu"
            aria-expanded={open}
          >
            <span className="relative flex h-5 w-5 items-center justify-center">
              <span className="absolute block h-0.5 w-5 -translate-y-1.5 rounded-full bg-gray-700 transition-all duration-300 ease-out" />
              <span className="absolute block h-0.5 w-5 rounded-full bg-gray-700 transition-all duration-200 ease-out" />
              <span className="absolute block h-0.5 w-5 translate-y-1.5 rounded-full bg-gray-700 transition-all duration-300 ease-out" />
            </span>
          </button>
        </div>
      )}

      <div
        className={`fixed inset-0 z-[60] md:hidden transition-opacity duration-300 ease-out ${
          open
            ? "pointer-events-auto bg-black/30 opacity-100"
            : "pointer-events-none bg-black/0 opacity-0"
        }`}
        onClick={handleCloseMenu}
      >
        <div
          className={`absolute left-0 top-0 flex h-screen w-72 flex-col border-r border-gray-200 bg-white px-4 py-6 shadow-lg transition-transform duration-300 ease-out ${
            open ? "translate-x-0" : "-translate-x-full"
          }`}
          onClick={(e) => e.stopPropagation()}
        >
          <div className="flex items-center justify-end">
            <button
              type="button"
              onClick={handleCloseMenu}
              className="inline-flex items-center rounded-xl border border-gray-200 px-3 py-2 text-sm font-medium text-gray-700 transition-colors duration-200 hover:bg-gray-100 hover:text-gray-900"
              aria-label="Close navigation menu"
            >
              ✕
            </button>
          </div>

          <div className="mt-6 flex flex-col gap-2">
            <Link to="/" className={navItemStyle} onClick={handleCloseMenu}>
              Home
            </Link>
            <Link
              to="/expenses"
              className={navItemStyle}
              onClick={handleCloseMenu}
            >
              Expenses
            </Link>
            <Link
              to="/create_expense"
              className={navItemStyle}
              onClick={handleCloseMenu}
            >
              Create Expense
            </Link>
          </div>

          <div className="mt-auto pt-6">
            <button
              type="button"
              onClick={handleLogout}
              className={logoutButtonStyle}
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
