import React, { useState } from "react";
import { createExpense } from "../../utils/api";
import Navbar from "../../Components/Navbar";

export default function CreateExpense() {
  const [name, setName] = useState("");
  const [amount, setAmount] = useState("");

  const [nameValid, setNameValid] = useState(true);
  const [amountValid, setAmountValid] = useState(true);
  const [generalMessage, setGeneralMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validateName = (value: string) => {
    return value.trim().length >= 1 && value.trim().length < 255;
  };

  const validateAmount = (value: string) => {
    const parsed = Number(value);
    return value.trim().length > 0 && !Number.isNaN(parsed) && parsed > 0;
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const isNameValid = validateName(name);
    const isAmountValid = validateAmount(amount);

    setNameValid(isNameValid);
    setAmountValid(isAmountValid);
    setGeneralMessage("");

    if (!isNameValid || !isAmountValid) {
      return;
    }

    setIsSubmitting(true);

    try {
      await createExpense({ name, amount });
      setGeneralMessage("Expense created successfully");
      setName("");
      setAmount("");
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
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <main className="px-6 py-12 md:pl-64">
        <div className="mx-auto flex min-h-[80vh] max-w-5xl items-center justify-center">
          <div className="w-full max-w-3xl overflow-hidden rounded-3xl border border-gray-200 bg-white shadow-sm">
            <div className="border-b border-gray-200 bg-gray-50 px-8 py-8 sm:px-10">
              <p className="text-sm font-medium uppercase tracking-[0.2em] text-gray-500">
                New Expense
              </p>
              <h1 className="mt-3 text-3xl font-semibold tracking-tight text-gray-900">
                Create an expense entry
              </h1>
              <p className="mt-3 max-w-2xl text-sm leading-6 text-gray-600">
                Add a new expense by entering the name and amount below.
              </p>
            </div>

            <div className="px-8 py-8 sm:px-10 sm:py-10">
              <div className="mx-auto max-w-xl">
                <form onSubmit={handleSubmit} className="space-y-5">
                  <div>
                    <label
                      htmlFor="name"
                      className="text-sm font-medium text-gray-700"
                    >
                      Name
                    </label>
                    <input
                      id="name"
                      type="text"
                      value={name}
                      onChange={(e) => {
                        const value = e.target.value;
                        setName(value);
                        setNameValid(validateName(value));
                        setGeneralMessage("");
                      }}
                      required
                      className={`${inputBaseStyle} ${
                        nameValid ? inputValidStyle : inputErrorStyle
                      }`}
                      placeholder="Enter expense name"
                    />
                    {!nameValid && (
                      <p className="mt-2 text-sm text-red-600">
                        Please enter a valid name
                      </p>
                    )}
                  </div>

                  <div>
                    <label
                      htmlFor="amount"
                      className="text-sm font-medium text-gray-700"
                    >
                      Amount
                    </label>
                    <input
                      id="amount"
                      type="number"
                      step="0.01"
                      min="0"
                      value={amount}
                      onChange={(e) => {
                        const value = e.target.value;
                        setAmount(value);
                        setAmountValid(validateAmount(value));
                        setGeneralMessage("");
                      }}
                      required
                      className={`${inputBaseStyle} ${
                        amountValid ? inputValidStyle : inputErrorStyle
                      }`}
                      placeholder="Enter expense amount"
                    />
                    {!amountValid && (
                      <p className="mt-2 text-sm text-red-600">
                        Please enter a valid amount greater than 0
                      </p>
                    )}
                  </div>

                  <button
                    type="submit"
                    disabled={isSubmitting}
                    className="w-full rounded-xl bg-gray-900 px-4 py-3 text-sm font-medium text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-70"
                  >
                    {isSubmitting ? "Creating..." : "Create Expense"}
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
      </main>
    </div>
  );
}
