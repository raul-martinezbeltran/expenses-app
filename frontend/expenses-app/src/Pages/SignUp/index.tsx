import React, { useState } from "react";
import { signupAndLogin } from "../../utils/api";

export default function SignUp() {
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [userNameValid, setUserNameValid] = useState(true);
  const [emailValid, setEmailValid] = useState(true);
  const [passwordMatch, setPasswordMatch] = useState(true);

  const [userNameErrorMessage, setUserNameErrorMessage] = useState("");
  const [emailErrorMessage, setEmailErrorMessage] = useState("");
  const [generalMessage, setGeneralMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validateUserName = (value: string) => {
    return value.length >= 1 && value.length < 255;
  };

  const validateEmail = (value: string) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(value);
  };

  const handleUserNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setUserName(value);
    setUserNameValid(validateUserName(value));
    setUserNameErrorMessage("");
    setGeneralMessage("");
  };

  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setEmail(value);
    setEmailValid(validateEmail(value));
    setEmailErrorMessage("");
    setGeneralMessage("");
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const isUserNameValid = validateUserName(userName);
    const isEmailValid = validateEmail(email);
    const isPasswordMatch = password === confirmPassword;

    setUserNameValid(isUserNameValid);
    setEmailValid(isEmailValid);
    setPasswordMatch(isPasswordMatch);
    setUserNameErrorMessage("");
    setEmailErrorMessage("");
    setGeneralMessage("");

    if (!isUserNameValid || !isEmailValid || !isPasswordMatch) {
      return;
    }

    setIsSubmitting(true);

    try {
      await signupAndLogin({
        username: userName,
        email,
        full_name: fullName,
        password,
      });

      setGeneralMessage("Signup and login successful");

      setUserName("");
      setPassword("");
      setConfirmPassword("");
      setFullName("");
      setEmail("");
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Unable to connect to server";

      if (message === "Username already registered") {
        setUserNameValid(false);
        setUserNameErrorMessage(message);
      } else if (message === "Email already registered") {
        setEmailValid(false);
        setEmailErrorMessage(message);
      } else {
        setGeneralMessage(message);
      }
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
                Welcome
              </p>
              <h1 className="mt-4 text-4xl font-semibold tracking-tight text-gray-900">
                Create your account
              </h1>
              <p className="mt-4 max-w-md text-sm leading-7 text-gray-600">
                Set up your account to start managing your profile and access
                your personalized experience.
              </p>
            </div>
          </div>

          <div className="p-8 sm:p-10 lg:p-12">
            <div className="mx-auto max-w-md">
              <div className="lg:hidden">
                <p className="text-sm font-medium uppercase tracking-[0.2em] text-gray-500">
                  Welcome
                </p>
                <h1 className="mt-3 text-3xl font-semibold tracking-tight text-gray-900">
                  Create your account
                </h1>
                <p className="mt-3 text-sm leading-6 text-gray-600">
                  Join and get started with a clean, secure signup experience.
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
                      {userNameErrorMessage || "Invalid username"}
                    </p>
                  )}
                </div>

                <div>
                  <label
                    htmlFor="fullName"
                    className="text-sm font-medium text-gray-700"
                  >
                    Full Name
                  </label>
                  <input
                    id="fullName"
                    type="text"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    required
                    className={`${inputBaseStyle} ${inputValidStyle}`}
                    placeholder="Enter your full name"
                  />
                </div>

                <div>
                  <label
                    htmlFor="email"
                    className="text-sm font-medium text-gray-700"
                  >
                    Email
                  </label>
                  <input
                    id="email"
                    type="email"
                    value={email}
                    onChange={handleEmailChange}
                    required
                    className={`${inputBaseStyle} ${
                      emailValid ? inputValidStyle : inputErrorStyle
                    }`}
                    placeholder="Enter your email"
                  />
                  {!emailValid && (
                    <p className="mt-2 text-sm text-red-600">
                      {emailErrorMessage || "Invalid email"}
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
                      setPasswordMatch(e.target.value === confirmPassword);
                    }}
                    required
                    className={`${inputBaseStyle} ${
                      passwordMatch ? inputValidStyle : inputErrorStyle
                    }`}
                    placeholder="Enter your password"
                  />
                </div>

                <div>
                  <label
                    htmlFor="confirmPassword"
                    className="text-sm font-medium text-gray-700"
                  >
                    Confirm Password
                  </label>
                  <input
                    id="confirmPassword"
                    type="password"
                    value={confirmPassword}
                    onChange={(e) => {
                      const value = e.target.value;
                      setConfirmPassword(value);
                      setPasswordMatch(password === value);
                    }}
                    required
                    className={`${inputBaseStyle} ${
                      passwordMatch ? inputValidStyle : inputErrorStyle
                    }`}
                    placeholder="Re-enter your password"
                  />
                  {!passwordMatch && (
                    <p className="mt-2 text-sm text-red-600">
                      Passwords do not match
                    </p>
                  )}
                </div>

                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full rounded-xl bg-gray-900 px-4 py-3 text-sm font-medium text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-70"
                >
                  {isSubmitting ? "Signing up..." : "Create Account"}
                </button>

                {generalMessage && (
                  <div
                    className={`rounded-xl border px-4 py-3 text-sm ${
                      generalMessage.toLowerCase().includes("successful")
                        ? "border-green-200 bg-green-50 text-green-700"
                        : "border-gray-200 bg-gray-50 text-gray-700"
                    }`}
                  >
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
