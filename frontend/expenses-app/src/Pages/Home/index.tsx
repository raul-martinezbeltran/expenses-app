import { useEffect, useState } from "react";
import { useNavigate } from "react-router";
import { isAuthenticated } from "../../utils/auth";
import Navbar from "../../Components/Navbar";

export default function Home() {
  const navigate = useNavigate();
  const [checkedAuth, setCheckedAuth] = useState(false);

  useEffect(() => {
    if (!isAuthenticated()) {
      navigate("/login", { replace: true });
      return;
    }

    setCheckedAuth(true);
  }, [navigate]);

  if (!checkedAuth) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      Home Page
    </div>
  );
}
