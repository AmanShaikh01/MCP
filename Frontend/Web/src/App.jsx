import React, { useState } from "react";

export default function App() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResponse("");

    try {
      const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/query`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });

      const data = await res.json();
      if (res.ok) {
        setResponse(data.response);
      } else {
        setError(data.error || "Something went wrong");
      }
    } catch {
      setError("Failed to connect to server.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-indigo-100 to-white flex items-center justify-center px-4">
      <section className="w-full max-w-xl p-8 bg-white shadow-xl rounded-2xl border border-gray-200">
        <h1 className="text-3xl font-semibold text-indigo-600 text-center mb-6">
          Student Query System
        </h1>
        <form onSubmit={handleSubmit} className="space-y-5">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask your query (e.g., students with CGPA > 8)"
            className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-400 text-sm"
          />
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-3 rounded-xl font-medium transition-all disabled:opacity-50"
          >
            {loading ? "Loading..." : "Submit Query"}
          </button>
        </form>

        {error && (
          <div className="mt-4 text-red-500 text-sm bg-red-100 p-2 rounded-lg border border-red-300">
            {error}
          </div>
        )}

        {response && (
          <pre className="mt-6 text-sm bg-gray-100 p-4 rounded-lg max-h-80 overflow-auto border border-gray-200 whitespace-pre-wrap">
            {response}
          </pre>
        )}

        <div className="mt-6 text-sm text-gray-500 text-center">
          Powered by Gemini LLM · Supabase · Flask
        </div>
      </section>
    </main>
  );
}
