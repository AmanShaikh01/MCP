// import React, { useState } from "react";
// import ResponseDisplay from "./Response";

// function App() {
//   const [query, setQuery] = useState("");
//   const [response, setResponse] = useState("");
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState("");

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     setLoading(true);
//     setError("");
//     setResponse("");

//     try {
//       const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/query`, {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//         },
//         body: JSON.stringify({ query }),
//       });

//       const data = await res.json();
//       if (res.ok) {
//         setResponse(data.response);
//       } else {
//         const errorMsg = data.error || (data.response ? JSON.parse(data.response).error : "Something went wrong");
//         setError(errorMsg);
//       }
//     } catch {
//       setError("Failed to connect to the server. Please check your connection and try again.");
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="min-h-screen bg-gradient-to-b from-[#0f172a] via-[#111827] to-[#0f172a] text-white relative overflow-hidden">
//       {/* Floating Neon Shapes */}
//       <div className="absolute top-20 left-10 w-16 h-16 bg-purple-500 rounded-full blur-xl opacity-70 animate-bounce"></div>
//       <div className="absolute bottom-40 right-16 w-24 h-24 bg-cyan-400 rounded-full blur-2xl opacity-60 animate-pulse"></div>
//       <div className="absolute top-1/3 right-1/4 w-0 h-0 
//         border-l-[40px] border-r-[40px] border-b-[70px] 
//         border-l-transparent border-r-transparent border-b-purple-400 
//         opacity-70 animate-spin-slow"></div>
//       <div className="absolute bottom-20 left-1/3 w-3 h-32 bg-gradient-to-b from-purple-400 to-cyan-400 rounded-full opacity-60 animate-float"></div>

//       {/* Navbar */}
//       <nav className="flex justify-between items-center px-10 py-4 bg-[#0f172a]/80 backdrop-blur-md border-b border-white/10 relative z-10">
//         <div className="flex items-center gap-2">
//           <span className="text-purple-400 text-2xl">🗄️</span>
//           <h1 className="text-lg font-bold">AI Database Editor</h1>
//           <span className="ml-2 px-2 py-0.5 text-xs rounded-full bg-purple-600">Beta</span>
//           <span className="ml-1 px-2 py-0.5 text-xs rounded-full bg-green-600">Neural</span>
//         </div>
//         <ul className="hidden md:flex gap-6 text-sm text-gray-300">
//           <li className="hover:text-white cursor-pointer">Features</li>
//           <li className="hover:text-white cursor-pointer">Documentation</li>
//           <li className="hover:text-white cursor-pointer">Pricing</li>
//         </ul>
//         <button className="ml-4 px-4 py-2 bg-purple-600 rounded-lg hover:bg-purple-700 text-sm">
//           GitHub
//         </button>
//       </nav>

//       {/* Hero */}
//       <section className="text-center px-6 mt-16 relative z-10">
//         <button className="px-4 py-1.5 bg-purple-900/50 border border-purple-500/50 text-sm rounded-full mb-4">
//           Powered by Advanced AI
//         </button>
//         <h2 className="text-cyan-400 text-sm mb-2">
//           The Future of Database Querying is Here.
//         </h2>
//         <p className="text-gray-300 max-w-2xl mx-auto">
//           AI Database Editor uses cutting-edge AI to transform your natural
//           language questions into precise SQL queries. Get custom database
//           insights delivered instantly—no technical knowledge required.
//         </p>
//       </section>

//       {/* Query System */}
//       <div className="max-w-xl mx-auto mt-10 bg-[#1e293b]/80 backdrop-blur-md p-6 rounded-2xl border border-white/10 shadow-lg relative z-10">
//         <h3 className="text-lg font-semibold mb-4 text-center text-cyan-400">
//           Query System
//         </h3>
//         <form onSubmit={handleSubmit}>
//           <input
//             type="text"
//             value={query}
//             onChange={(e) => setQuery(e.target.value)}
//             placeholder="Ask your query (e.g., students with CGPA > 8)"
//             className="w-full px-4 py-2 rounded-lg bg-[#0f172a] border border-gray-600 text-gray-200 focus:outline-none focus:ring-2 focus:ring-purple-500 mb-4"
//           />
//           <button 
//             type="submit"
//             disabled={loading}
//             className="w-full py-2 bg-gradient-to-r from-purple-500 to-cyan-500 rounded-lg font-semibold hover:opacity-90 transition disabled:opacity-50"
//           >
//             {loading ? "Loading..." : "Submit Query"}
//           </button>
//         </form>
        
//         {error && (
//           <div className="mt-4 text-red-400 text-sm bg-red-900/50 p-3 rounded-lg border border-red-500/50">
//             {error}
//           </div>
//         )}

//         <ResponseDisplay response={response} />
        
//         <p className="text-xs text-gray-400 text-center mt-4">
//           Powered by Gemini LLM · Supabase · Flask
//         </p>
//         <button className="block mx-auto mt-3 text-purple-400 text-sm hover:underline">
//           ⚙ Configure API Keys First
//         </button>
//       </div>

//       {/* Features */}
//       <section className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto mt-16 px-6 relative z-10">
//         <div className="bg-[#1e293b]/70 border border-white/10 rounded-2xl p-6 text-center shadow-lg">
//           <h4 className="text-purple-400 text-lg mb-2">Natural Language</h4>
//           <p className="text-gray-300 text-sm">
//             Ask questions in plain English and get instant SQL results.
//           </p>
//         </div>
//         <div className="bg-[#1e293b]/70 border border-white/10 rounded-2xl p-6 text-center shadow-lg">
//           <h4 className="text-cyan-400 text-lg mb-2">AI Powered</h4>
//           <p className="text-gray-300 text-sm">
//             Advanced neural networks optimize every query for performance.
//           </p>
//         </div>
//         <div className="bg-[#1e293b]/70 border border-white/10 rounded-2xl p-6 text-center shadow-lg">
//           <h4 className="text-green-400 text-lg mb-2">Easy Setup</h4>
//           <p className="text-gray-300 text-sm">
//             Connect any database in minutes with our simple configuration.
//           </p>
//         </div>
//       </section>
//     </div>
//   );
// }

// export default App;

import React, { useState, useEffect, useCallback } from "react";

const API_URL = "http://localhost:5000";

export default function App() {
  // State for the entire application
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [activeTab, setActiveTab] = useState('query');
  const [history, setHistory] = useState([]);

  // Form states
  const [dbType, setDbType] = useState("supabase");
  const [connectionMethod, setConnectionMethod] = useState("connection_string");
  const [credentials, setCredentials] = useState({});
  const [mode, setMode] = useState("read-only");

  // Query states
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");

  const fetchHistory = useCallback(async () => {
    if (!isConnected) return;
    try {
      const res = await fetch(`${API_URL}/history`, {
        credentials: 'include'
      });
      const data = await res.json();
      if (res.ok) {
        setHistory(data.history || []);
      }
    } catch (err) {
      console.error("Failed to fetch history:", err);
    }
  }, [isConnected]);
  
  useEffect(() => {
    if (isConnected && activeTab === 'history') {
      fetchHistory();
    }
  }, [isConnected, activeTab, fetchHistory]);

  const handleConnect = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");
    try {
      const res = await fetch(`${API_URL}/connect`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: 'include',
        body: JSON.stringify({ db_type: dbType, ...credentials, mode }),
      });
      const data = await res.json();
      if (res.ok) {
        setIsConnected(true);
      } else {
        throw new Error(data.error || "Connection failed.");
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDisconnect = async () => {
    try {
      await fetch(`${API_URL}/disconnect`, { 
        method: "POST",
        credentials: 'include'
      });
    } catch (err) {
      console.error("Failed to disconnect cleanly:", err);
    } finally {
      setIsConnected(false);
      setCredentials({});
      setQuery("");
      setResponse("");
      setError("");
      setHistory([]);
      setActiveTab('query');
    }
  };

  const handleQuerySubmit = async (e) => {
    e.preventDefault();
    if (!query) return;
    setIsLoading(true);
    setError("");
    setResponse("");
    try {
      const res = await fetch(`${API_URL}/query`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: 'include',
        body: JSON.stringify({ query }),
      });
      const data = await res.json();
      if (res.ok) {
        setResponse(data.response);
        if (mode === 'read-write') {
           fetchHistory();
        }
      } else {
        throw new Error(data.error || "Query failed.");
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRevert = async (historyId) => {
    setIsLoading(true);
    setError("");
    try {
      const res = await fetch(`${API_URL}/revert`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ history_id: historyId }),
      });
      const data = await res.json();
      if(res.ok) {
        fetchHistory();
      } else {
        throw new Error(data.error || 'Failed to revert change.');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };
  
  // --- UI Components ---

  const renderConnectionForm = () => (
    <form onSubmit={handleConnect} className="space-y-4">
      <h2 className="text-xl font-medium text-gray-700 text-center">
        Connect to Your Database
      </h2>

      <div>
        <label className="text-sm font-medium text-gray-600">Database Type</label>
        <select
          value={dbType}
          onChange={(e) => {
            setDbType(e.target.value);
            setCredentials({});
            setConnectionMethod("connection_string");
          }}
          className="w-full mt-1 px-4 py-3 border border-gray-300 rounded-xl"
        >
          <option value="supabase">Supabase (PostgreSQL)</option>
          <option value="postgresql">PostgreSQL</option>
          <option value="mysql">MySQL</option>
          <option value="mongodb">MongoDB</option>
        </select>
      </div>

      {/* Connection Method Toggle for SQL databases */}
      {dbType !== "mongodb" && (
        <div>
          <label className="text-sm font-medium text-gray-600">Connection Method</label>
          <div className="flex gap-2 mt-1">
            <button
              type="button"
              onClick={() => {
                setConnectionMethod("connection_string");
                setCredentials({});
              }}
              className={`flex-1 py-2 px-4 rounded-lg text-sm font-medium ${
                connectionMethod === "connection_string"
                  ? "bg-indigo-600 text-white"
                  : "bg-gray-100 text-gray-600"
              }`}
            >
              Connection String
            </button>
            <button
              type="button"
              onClick={() => {
                setConnectionMethod("individual");
                setCredentials({});
              }}
              className={`flex-1 py-2 px-4 rounded-lg text-sm font-medium ${
                connectionMethod === "individual"
                  ? "bg-indigo-600 text-white"
                  : "bg-gray-100 text-gray-600"
              }`}
            >
              Individual Fields
            </button>
          </div>
        </div>
      )}

      {/* Connection String Method */}
      {connectionMethod === "connection_string" && dbType !== "mongodb" && (
        <div>
          <label className="text-sm font-medium text-gray-600">
            Connection String
            {dbType === "supabase" && (
              <span className="text-xs text-gray-500 ml-2">
                (Find in Supabase → Project Settings → Database → Connection String → URI)
              </span>
            )}
          </label>
          <input
            type="password"
            placeholder={
              dbType === "supabase"
                ? "postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres"
                : dbType === "postgresql"
                ? "postgresql://user:password@host:5432/dbname"
                : "mysql://user:password@host:3306/dbname"
            }
            onChange={(e) => setCredentials({ connection_string: e.target.value })}
            className="w-full mt-1 px-4 py-3 border border-gray-300 rounded-xl text-sm"
            required
          />
          {dbType === "supabase" && (
            <p className="text-xs text-blue-600 mt-1">
              💡 Tip: In Supabase, go to Settings → Database → Connection string → copy the URI and replace [YOUR-PASSWORD] with your actual password
            </p>
          )}
        </div>
      )}

      {/* MongoDB Connection String */}
      {dbType === "mongodb" && (
        <div>
          <label className="text-sm font-medium text-gray-600">
            Connection String
            <span className="text-xs text-gray-500 ml-2">
              (MongoDB Atlas connection string)
            </span>
          </label>
          <input
            type="password"
            placeholder="mongodb+srv://user:pass@cluster.mongodb.net/dbname"
            onChange={(e) => setCredentials({ connection_string: e.target.value })}
            className="w-full mt-1 px-4 py-3 border border-gray-300 rounded-xl text-sm"
            required
          />
        </div>
      )}

      {/* Individual Fields Method */}
      {connectionMethod === "individual" && dbType !== "mongodb" && (
        <>
          <div className="grid grid-cols-2 gap-4">
            <input
              type="text"
              placeholder="Host (e.g., localhost)"
              onChange={(e) => setCredentials({ ...credentials, host: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 rounded-xl"
              required
            />
            <input
              type="text"
              placeholder={`Port (default: ${dbType === 'mysql' ? '3306' : '5432'})`}
              onChange={(e) => setCredentials({ ...credentials, port: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 rounded-xl"
            />
          </div>
          <input
            type="text"
            placeholder="Database Name"
            onChange={(e) => setCredentials({ ...credentials, dbname: e.target.value })}
            className="w-full px-4 py-3 border border-gray-300 rounded-xl"
            required
          />
          <input
            type="text"
            placeholder="Username"
            onChange={(e) => setCredentials({ ...credentials, user: e.target.value })}
            className="w-full px-4 py-3 border border-gray-300 rounded-xl"
            required
          />
          <input
            type="password"
            placeholder="Password"
            onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
            className="w-full px-4 py-3 border border-gray-300 rounded-xl"
            required
          />
        </>
      )}

      <div>
        <label className="text-sm font-medium text-gray-600">Operation Mode</label>
        <select 
          value={mode} 
          onChange={(e) => setMode(e.target.value)} 
          className="w-full mt-1 px-4 py-3 border border-gray-300 rounded-xl"
        >
          <option value="read-only">Read-Only (Recommended)</option>
          <option value="read-write">Read & Write (Advanced)</option>
        </select>
        {mode === 'read-write' && (
          <p className="text-xs text-yellow-600 mt-1">
            ⚠️ Warning: This mode allows the AI to make changes to your database.
          </p>
        )}
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-3 rounded-xl font-medium disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isLoading ? "Connecting..." : "Connect"}
      </button>
      <p className="text-xs text-gray-500 text-center mt-2">
        🔒 Your credentials are used for temporary connections and are never stored permanently.
      </p>
    </form>
  );

  const renderQueryInterface = () => (
    <div>
      <div className="flex justify-between items-center mb-4 border-b">
         <div className="flex items-center gap-4">
            <button 
              onClick={() => setActiveTab('query')} 
              className={`py-2 px-3 text-sm font-medium ${
                activeTab === 'query' 
                  ? 'text-indigo-600 border-b-2 border-indigo-600' 
                  : 'text-gray-500'
              }`}
            >
              Query
            </button>
            {mode === 'read-write' && (
              <button 
                onClick={() => setActiveTab('history')} 
                className={`py-2 px-3 text-sm font-medium ${
                  activeTab === 'history' 
                    ? 'text-indigo-600 border-b-2 border-indigo-600' 
                    : 'text-gray-500'
                }`}
              >
                History
              </button>
            )}
         </div>
         <button 
           onClick={handleDisconnect} 
           className="text-sm text-gray-500 hover:text-red-600"
         >
          Disconnect
        </button>
      </div>

      {activeTab === 'query' ? (
        <>
          <form onSubmit={handleQuerySubmit} className="space-y-4">
            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask your query... (e.g., 'How many students are in the Computer department?')"
              className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-400"
              rows="3"
            />
            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-3 rounded-xl font-medium disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? "Processing..." : "Submit Query"}
            </button>
          </form>

          {isLoading && activeTab === 'query' && (
            <div className="text-center mt-4 text-gray-600">
              Processing your query...
            </div>
          )}

          {response && (
            <div className="mt-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-2">Response</h3>
              <pre className="text-sm bg-gray-100 p-4 rounded-lg max-h-80 overflow-auto whitespace-pre-wrap">
                {response}
              </pre>
            </div>
          )}
        </>
      ) : (
        renderHistoryTab()
      )}
    </div>
  );

  const renderHistoryTab = () => (
    <div>
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Activity Log</h3>
      {history.length === 0 ? (
        <p className="text-sm text-gray-500">No changes have been made in this session yet.</p>
      ) : (
        <ul className="space-y-2">
          {history.map((item, index) => (
            <li key={index} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg border">
              <div>
                <p className="text-sm font-medium text-gray-700">{item.description}</p>
                <p className="text-xs text-gray-500">
                  {new Date(item.timestamp).toLocaleTimeString()}
                </p>
              </div>
              <button
                onClick={() => handleRevert(index)}
                disabled={item.reverted || isLoading}
                className={`text-xs font-semibold px-3 py-1 rounded-full ${
                  item.reverted 
                    ? 'bg-gray-200 text-gray-500 cursor-not-allowed' 
                    : 'bg-blue-100 text-blue-700 hover:bg-blue-200'
                }`}
              >
                {item.reverted ? 'Reverted' : 'Revert'}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );

  return (
    <main className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <section className="w-full max-w-2xl p-8 bg-white shadow-lg rounded-2xl border">
        <h1 className="text-3xl font-bold text-indigo-600 text-center mb-2">
          AI Database Assistant
        </h1>
        <p className="text-center text-gray-500 mb-6 text-sm">
          Connect to your database and ask questions in plain English.
        </p>

        {error && (
          <div className="my-4 text-red-600 text-sm bg-red-100 p-3 rounded-lg">
            <strong>Error:</strong> {error}
          </div>
        )}

        {isConnected ? renderQueryInterface() : renderConnectionForm()}
        
      </section>
    </main>
  );
}