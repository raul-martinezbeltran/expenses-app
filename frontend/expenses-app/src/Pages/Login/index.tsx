import React, { useState } from "react";
import { useNavigate } from "react-router";
import { loginUser } from "../../utils/api";

export default function Login() {
  const navigate = useNavigate();

  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");

  const [userNameValid, setUserNameValid] = useState(true);
  const [generalMessage, setGeneralMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validateUserName = (value: string) => {
    return value.length >= 1 && value.length < 255;
  };

  const handleUserNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setUserName(value);
    setUserNameValid(validateUserName(value));
    setGeneralMessage("");
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const isUserNameValid = validateUserName(userName);
    setUserNameValid(isUserNameValid);
    setGeneralMessage("");

    if (!isUserNameValid) {
      return;
    }

    setIsSubmitting(true);

    try {
      await loginUser(userName, password);
      navigate("/", { replace: true });
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Unable to connect to server";

      setGeneralMessage(message);
    } finally {
      setIsSubmitting(false);
    }
  };

  const inputBaseStyle =
    "mt-2 w-full rounded-xl border bg-white px-4 py-3 text-sm text-gray-900 outline-none transition placeholder:text-gray-400 focus:ring-2";
  const inputValidStyle =
    "border-gray-300 focus:border-gray-900 focus:ring-gray-200";
  const inputErrorStyle =
    "border-red-400 focus:border-red-500 focus:ring-red-100";

  return (
    <div className="min-h-screen bg-gray-50 px-6 py-12">
      <div className="mx-auto flex min-h-[80vh] max-w-6xl items-center justify-center">
        <div className="grid w-full max-w-5xl overflow-hidden rounded-3xl border border-gray-200 bg-white shadow-sm lg:grid-cols-2">
          <div className="hidden border-r border-gray-200 bg-gray-50 p-12 lg:flex lg:flex-col lg:justify-center">
            <div>
              <p className="text-sm font-medium uppercase tracking-[0.2em] text-gray-500">
                Welcome Back
              </p>
              <h1 className="mt-4 text-4xl font-semibold tracking-tight text-gray-900">
                Sign in to your account
              </h1>
              <p className="mt-4 max-w-md text-sm leading-7 text-gray-600">
                Access your account and continue with your personalized
                experience.
              </p>
            </div>
          </div>

          <div className="p-8 sm:p-10 lg:p-12">
            <div className="mx-auto max-w-md">
              <div className="lg:hidden">
                <p className="text-sm font-medium uppercase tracking-[0.2em] text-gray-500">
                  Welcome Back
                </p>
                <h1 className="mt-3 text-3xl font-semibold tracking-tight text-gray-900">
                  Sign in to your account
                </h1>
                <p className="mt-3 text-sm leading-6 text-gray-600">
                  Log in with your username and password.
                </p>
              </div>

              <form onSubmit={handleSubmit} className="mt-8 space-y-5">
                <div>
                  <label
                    htmlFor="username"
                    className="text-sm font-medium text-gray-700"
                  >
                    Username
                  </label>
                  <input
                    id="username"
                    type="text"
                    value={userName}
                    onChange={handleUserNameChange}
                    required
                    className={`${inputBaseStyle} ${
                      userNameValid ? inputValidStyle : inputErrorStyle
                    }`}
                    placeholder="Enter your username"
                  />
                  {!userNameValid && (
                    <p className="mt-2 text-sm text-red-600">
                      Invalid username
                    </p>
                  )}
                </div>

                <div>
                  <label
                    htmlFor="password"
                    className="text-sm font-medium text-gray-700"
                  >
                    Password
                  </label>
                  <input
                    id="password"
                    type="password"
                    value={password}
                    onChange={(e) => {
                      setPassword(e.target.value);
                      setGeneralMessage("");
                    }}
                    required
                    className={`${inputBaseStyle} ${inputValidStyle}`}
                    placeholder="Enter your password"
                  />
                </div>

                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full rounded-xl bg-gray-900 px-4 py-3 text-sm font-medium text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-70"
                >
                  {isSubmitting ? "Signing in..." : "Sign In"}
                </button>

                {generalMessage && (
                  <div className="rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-sm text-gray-700">
                    {generalMessage}
                  </div>
                )}
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
