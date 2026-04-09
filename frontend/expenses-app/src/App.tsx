import { Routes, Route } from "react-router";
import Home from "./Pages/Home";
import SignUp from "./Pages/SignUp";
import "./App.css";
import Login from "./Pages/Login";
import CreateExpense from "./Pages/CreateExpense";

function App() {
  return (
    <div>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/login" element={<Login />} />
        <Route path="/home" element={<Home />} />
        <Route path="/create_expense" element={<CreateExpense />} />
      </Routes>
    </div>
  );
}

export default App;
