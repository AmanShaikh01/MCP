import React, { useState } from "react";
import ResponseDisplay from "./Response";

function App() {
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
        const errorMsg = data.error || (data.response ? JSON.parse(data.response).error : "Something went wrong");
        setError(errorMsg);
      }
    } catch {
      setError("Failed to connect to the server. Please check your connection and try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#0f172a] via-[#111827] to-[#0f172a] text-white relative overflow-hidden">
      {/* Floating Neon Shapes */}
      <div className="absolute top-20 left-10 w-16 h-16 bg-purple-500 rounded-full blur-xl opacity-70 animate-bounce"></div>
      <div className="absolute bottom-40 right-16 w-24 h-24 bg-cyan-400 rounded-full blur-2xl opacity-60 animate-pulse"></div>
      <div className="absolute top-1/3 right-1/4 w-0 h-0 
        border-l-[40px] border-r-[40px] border-b-[70px] 
        border-l-transparent border-r-transparent border-b-purple-400 
        opacity-70 animate-spin-slow"></div>
      <div className="absolute bottom-20 left-1/3 w-3 h-32 bg-gradient-to-b from-purple-400 to-cyan-400 rounded-full opacity-60 animate-float"></div>

      {/* Navbar */}
      <nav className="flex justify-between items-center px-10 py-4 bg-[#0f172a]/80 backdrop-blur-md border-b border-white/10 relative z-10">
        <div className="flex items-center gap-2">
          <span className="text-purple-400 text-2xl">🗄️</span>
          <h1 className="text-lg font-bold">AI Database Editor</h1>
          <span className="ml-2 px-2 py-0.5 text-xs rounded-full bg-purple-600">Beta</span>
          <span className="ml-1 px-2 py-0.5 text-xs rounded-full bg-green-600">Neural</span>
        </div>
        <ul className="hidden md:flex gap-6 text-sm text-gray-300">
          <li className="hover:text-white cursor-pointer">Features</li>
          <li className="hover:text-white cursor-pointer">Documentation</li>
          <li className="hover:text-white cursor-pointer">Pricing</li>
        </ul>
        <button className="ml-4 px-4 py-2 bg-purple-600 rounded-lg hover:bg-purple-700 text-sm">
          GitHub
        </button>
      </nav>

      {/* Hero */}
      <section className="text-center px-6 mt-16 relative z-10">
        <button className="px-4 py-1.5 bg-purple-900/50 border border-purple-500/50 text-sm rounded-full mb-4">
          Powered by Advanced AI
        </button>
        <h2 className="text-cyan-400 text-sm mb-2">
          The Future of Database Querying is Here.
        </h2>
        <p className="text-gray-300 max-w-2xl mx-auto">
          AI Database Editor uses cutting-edge AI to transform your natural
          language questions into precise SQL queries. Get custom database
          insights delivered instantly—no technical knowledge required.
        </p>
      </section>

      {/* Query System */}
      <div className="max-w-xl mx-auto mt-10 bg-[#1e293b]/80 backdrop-blur-md p-6 rounded-2xl border border-white/10 shadow-lg relative z-10">
        <h3 className="text-lg font-semibold mb-4 text-center text-cyan-400">
          Query System
        </h3>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask your query (e.g., students with CGPA > 8)"
            className="w-full px-4 py-2 rounded-lg bg-[#0f172a] border border-gray-600 text-gray-200 focus:outline-none focus:ring-2 focus:ring-purple-500 mb-4"
          />
          <button 
            type="submit"
            disabled={loading}
            className="w-full py-2 bg-gradient-to-r from-purple-500 to-cyan-500 rounded-lg font-semibold hover:opacity-90 transition disabled:opacity-50"
          >
            {loading ? "Loading..." : "Submit Query"}
          </button>
        </form>
        
        {error && (
          <div className="mt-4 text-red-400 text-sm bg-red-900/50 p-3 rounded-lg border border-red-500/50">
            {error}
          </div>
        )}

        <ResponseDisplay response={response} />
        
        <p className="text-xs text-gray-400 text-center mt-4">
          Powered by Gemini LLM · Supabase · Flask
        </p>
        <button className="block mx-auto mt-3 text-purple-400 text-sm hover:underline">
          ⚙ Configure API Keys First
        </button>
      </div>

      {/* Features */}
      <section className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto mt-16 px-6 relative z-10">
        <div className="bg-[#1e293b]/70 border border-white/10 rounded-2xl p-6 text-center shadow-lg">
          <h4 className="text-purple-400 text-lg mb-2">Natural Language</h4>
          <p className="text-gray-300 text-sm">
            Ask questions in plain English and get instant SQL results.
          </p>
        </div>
        <div className="bg-[#1e293b]/70 border border-white/10 rounded-2xl p-6 text-center shadow-lg">
          <h4 className="text-cyan-400 text-lg mb-2">AI Powered</h4>
          <p className="text-gray-300 text-sm">
            Advanced neural networks optimize every query for performance.
          </p>
        </div>
        <div className="bg-[#1e293b]/70 border border-white/10 rounded-2xl p-6 text-center shadow-lg">
          <h4 className="text-green-400 text-lg mb-2">Easy Setup</h4>
          <p className="text-gray-300 text-sm">
            Connect any database in minutes with our simple configuration.
          </p>
        </div>
      </section>
    </div>
  );
}

export default App;