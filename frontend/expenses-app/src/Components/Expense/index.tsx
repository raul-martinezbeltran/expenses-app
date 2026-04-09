export default function Expense({
  name,
  amount,
  created_at,
}: {
  name: string;
  amount: string;
  created_at: string;
}) {
  return (
    <div className="overflow-hidden rounded-3xl border border-gray-200 bg-white shadow-sm">
      <div className="border-b border-gray-200 bg-gray-50 px-6 py-4">
        <p className="text-sm font-medium uppercase tracking-[0.2em] text-gray-500">
          Expense
        </p>
      </div>

      <div className="p-6">
        <div className="flex items-center justify-between gap-4">
          <h3 className="text-xl font-semibold tracking-tight text-gray-900">
            {name}
          </h3>
          <span className="rounded-xl bg-gray-900 px-4 py-2 text-sm font-medium text-white">
            ${amount}
          </span>
        </div>

        <p className="mt-4 text-sm leading-6 text-gray-600">
          Created on {created_at}
        </p>
      </div>
    </div>
  );
}
