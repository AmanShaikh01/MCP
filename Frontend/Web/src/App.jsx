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

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// import React, { useState, useEffect, useCallback } from "react";

// const API_URL = "http://localhost:5000";

// export default function App() {
//   // State for the entire application
//   const [isConnected, setIsConnected] = useState(false);
//   const [isLoading, setIsLoading] = useState(false);
//   const [error, setError] = useState("");
//   const [activeTab, setActiveTab] = useState('query');
//   const [history, setHistory] = useState([]);

//   // Form states
//   const [dbType, setDbType] = useState("supabase");
//   const [connectionMethod, setConnectionMethod] = useState("connection_string");
//   const [credentials, setCredentials] = useState({});
//   const [mode, setMode] = useState("read-only");

//   // Query states
//   const [query, setQuery] = useState("");
//   const [response, setResponse] = useState("");

//   const fetchHistory = useCallback(async () => {
//     if (!isConnected) return;
//     try {
//       const res = await fetch(`${API_URL}/history`, {
//         credentials: 'include'
//       });
//       const data = await res.json();
//       if (res.ok) {
//         setHistory(data.history || []);
//       }
//     } catch (err) {
//       console.error("Failed to fetch history:", err);
//     }
//   }, [isConnected]);

//   useEffect(() => {
//     if (isConnected && activeTab === 'history') {
//       fetchHistory();
//     }
//   }, [isConnected, activeTab, fetchHistory]);

//   const handleConnect = async (e) => {
//     e.preventDefault();
//     setIsLoading(true);
//     setError("");
//     try {
//       const res = await fetch(`${API_URL}/connect`, {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         credentials: 'include',
//         body: JSON.stringify({ db_type: dbType, ...credentials, mode }),
//       });
//       const data = await res.json();
//       if (res.ok) {
//         setIsConnected(true);
//       } else {
//         throw new Error(data.error || "Connection failed.");
//       }
//     } catch (err) {
//       setError(err.message);
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   const handleDisconnect = async () => {
//     try {
//       await fetch(`${API_URL}/disconnect`, {
//         method: "POST",
//         credentials: 'include'
//       });
//     } catch (err) {
//       console.error("Failed to disconnect cleanly:", err);
//     } finally {
//       setIsConnected(false);
//       setCredentials({});
//       setQuery("");
//       setResponse("");
//       setError("");
//       setHistory([]);
//       setActiveTab('query');
//     }
//   };

//   const handleQuerySubmit = async (e) => {
//     e.preventDefault();
//     if (!query) return;
//     setIsLoading(true);
//     setError("");
//     setResponse("");
//     try {
//       const res = await fetch(`${API_URL}/query`, {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         credentials: 'include',
//         body: JSON.stringify({ query }),
//       });
//       const data = await res.json();
//       if (res.ok) {
//         setResponse(data.response);
//         if (mode === 'read-write') {
//            fetchHistory();
//         }
//       } else {
//         throw new Error(data.error || "Query failed.");
//       }
//     } catch (err) {
//       setError(err.message);
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   const handleRevert = async (historyId) => {
//     setIsLoading(true);
//     setError("");
//     try {
//       const res = await fetch(`${API_URL}/revert`, {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         credentials: 'include',
//         body: JSON.stringify({ history_id: historyId }),
//       });
//       const data = await res.json();
//       if(res.ok) {
//         fetchHistory();
//       } else {
//         throw new Error(data.error || 'Failed to revert change.');
//       }
//     } catch (err) {
//       setError(err.message);
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   // --- UI Components ---

//   const renderConnectionForm = () => (
//     <form onSubmit={handleConnect} className="space-y-4">
//       <h2 className="text-xl font-medium text-gray-700 text-center">
//         Connect to Your Database
//       </h2>

//       <div>
//         <label className="text-sm font-medium text-gray-600">Database Type</label>
//         <select
//           value={dbType}
//           onChange={(e) => {
//             setDbType(e.target.value);
//             setCredentials({});
//             setConnectionMethod("connection_string");
//           }}
//           className="w-full mt-1 px-4 py-3 border border-gray-300 rounded-xl"
//         >
//           <option value="supabase">Supabase (PostgreSQL)</option>
//           <option value="postgresql">PostgreSQL</option>
//           <option value="mysql">MySQL</option>
//           <option value="mongodb">MongoDB</option>
//         </select>
//       </div>

//       {/* Connection Method Toggle for SQL databases */}
//       {dbType !== "mongodb" && (
//         <div>
//           <label className="text-sm font-medium text-gray-600">Connection Method</label>
//           <div className="flex gap-2 mt-1">
//             <button
//               type="button"
//               onClick={() => {
//                 setConnectionMethod("connection_string");
//                 setCredentials({});
//               }}
//               className={`flex-1 py-2 px-4 rounded-lg text-sm font-medium ${
//                 connectionMethod === "connection_string"
//                   ? "bg-indigo-600 text-white"
//                   : "bg-gray-100 text-gray-600"
//               }`}
//             >
//               Connection String
//             </button>
//             <button
//               type="button"
//               onClick={() => {
//                 setConnectionMethod("individual");
//                 setCredentials({});
//               }}
//               className={`flex-1 py-2 px-4 rounded-lg text-sm font-medium ${
//                 connectionMethod === "individual"
//                   ? "bg-indigo-600 text-white"
//                   : "bg-gray-100 text-gray-600"
//               }`}
//             >
//               Individual Fields
//             </button>
//           </div>
//         </div>
//       )}

//       {/* Connection String Method */}
//       {connectionMethod === "connection_string" && dbType !== "mongodb" && (
//         <div>
//           <label className="text-sm font-medium text-gray-600">
//             Connection String
//             {dbType === "supabase" && (
//               <span className="text-xs text-gray-500 ml-2">
//                 (Find in Supabase → Project Settings → Database → Connection String → URI)
//               </span>
//             )}
//           </label>
//           <input
//             type="password"
//             placeholder={
//               dbType === "supabase"
//                 ? "postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres"
//                 : dbType === "postgresql"
//                 ? "postgresql://user:password@host:5432/dbname"
//                 : "mysql://user:password@host:3306/dbname"
//             }
//             onChange={(e) => setCredentials({ connection_string: e.target.value })}
//             className="w-full mt-1 px-4 py-3 border border-gray-300 rounded-xl text-sm"
//             required
//           />
//           {dbType === "supabase" && (
//             <p className="text-xs text-blue-600 mt-1">
//               💡 Tip: In Supabase, go to Settings → Database → Connection string → copy the URI and replace [YOUR-PASSWORD] with your actual password
//             </p>
//           )}
//         </div>
//       )}

//       {/* MongoDB Connection String */}
//       {dbType === "mongodb" && (
//         <div>
//           <label className="text-sm font-medium text-gray-600">
//             Connection String
//             <span className="text-xs text-gray-500 ml-2">
//               (MongoDB Atlas connection string)
//             </span>
//           </label>
//           <input
//             type="password"
//             placeholder="mongodb+srv://user:pass@cluster.mongodb.net/dbname"
//             onChange={(e) => setCredentials({ connection_string: e.target.value })}
//             className="w-full mt-1 px-4 py-3 border border-gray-300 rounded-xl text-sm"
//             required
//           />
//         </div>
//       )}

//       {/* Individual Fields Method */}
//       {connectionMethod === "individual" && dbType !== "mongodb" && (
//         <>
//           <div className="grid grid-cols-2 gap-4">
//             <input
//               type="text"
//               placeholder="Host (e.g., localhost)"
//               onChange={(e) => setCredentials({ ...credentials, host: e.target.value })}
//               className="w-full px-4 py-3 border border-gray-300 rounded-xl"
//               required
//             />
//             <input
//               type="text"
//               placeholder={`Port (default: ${dbType === 'mysql' ? '3306' : '5432'})`}
//               onChange={(e) => setCredentials({ ...credentials, port: e.target.value })}
//               className="w-full px-4 py-3 border border-gray-300 rounded-xl"
//             />
//           </div>
//           <input
//             type="text"
//             placeholder="Database Name"
//             onChange={(e) => setCredentials({ ...credentials, dbname: e.target.value })}
//             className="w-full px-4 py-3 border border-gray-300 rounded-xl"
//             required
//           />
//           <input
//             type="text"
//             placeholder="Username"
//             onChange={(e) => setCredentials({ ...credentials, user: e.target.value })}
//             className="w-full px-4 py-3 border border-gray-300 rounded-xl"
//             required
//           />
//           <input
//             type="password"
//             placeholder="Password"
//             onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
//             className="w-full px-4 py-3 border border-gray-300 rounded-xl"
//             required
//           />
//         </>
//       )}

//       <div>
//         <label className="text-sm font-medium text-gray-600">Operation Mode</label>
//         <select
//           value={mode}
//           onChange={(e) => setMode(e.target.value)}
//           className="w-full mt-1 px-4 py-3 border border-gray-300 rounded-xl"
//         >
//           <option value="read-only">Read-Only (Recommended)</option>
//           <option value="read-write">Read & Write (Advanced)</option>
//         </select>
//         {mode === 'read-write' && (
//           <p className="text-xs text-yellow-600 mt-1">
//             ⚠️ Warning: This mode allows the AI to make changes to your database.
//           </p>
//         )}
//       </div>

//       <button
//         type="submit"
//         disabled={isLoading}
//         className="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-3 rounded-xl font-medium disabled:opacity-50 disabled:cursor-not-allowed"
//       >
//         {isLoading ? "Connecting..." : "Connect"}
//       </button>
//       <p className="text-xs text-gray-500 text-center mt-2">
//         🔒 Your credentials are used for temporary connections and are never stored permanently.
//       </p>
//     </form>
//   );

//   const renderQueryInterface = () => (
//     <div>
//       <div className="flex justify-between items-center mb-4 border-b">
//          <div className="flex items-center gap-4">
//             <button
//               onClick={() => setActiveTab('query')}
//               className={`py-2 px-3 text-sm font-medium ${
//                 activeTab === 'query'
//                   ? 'text-indigo-600 border-b-2 border-indigo-600'
//                   : 'text-gray-500'
//               }`}
//             >
//               Query
//             </button>
//             {mode === 'read-write' && (
//               <button
//                 onClick={() => setActiveTab('history')}
//                 className={`py-2 px-3 text-sm font-medium ${
//                   activeTab === 'history'
//                     ? 'text-indigo-600 border-b-2 border-indigo-600'
//                     : 'text-gray-500'
//                 }`}
//               >
//                 History
//               </button>
//             )}
//          </div>
//          <button
//            onClick={handleDisconnect}
//            className="text-sm text-gray-500 hover:text-red-600"
//          >
//           Disconnect
//         </button>
//       </div>

//       {activeTab === 'query' ? (
//         <>
//           <form onSubmit={handleQuerySubmit} className="space-y-4">
//             <textarea
//               value={query}
//               onChange={(e) => setQuery(e.target.value)}
//               placeholder="Ask your query... (e.g., 'How many students are in the Computer department?')"
//               className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-400"
//               rows="3"
//             />
//             <button
//               type="submit"
//               disabled={isLoading}
//               className="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-3 rounded-xl font-medium disabled:opacity-50 disabled:cursor-not-allowed"
//             >
//               {isLoading ? "Processing..." : "Submit Query"}
//             </button>
//           </form>

//           {isLoading && activeTab === 'query' && (
//             <div className="text-center mt-4 text-gray-600">
//               Processing your query...
//             </div>
//           )}

//           {response && (
//             <div className="mt-6">
//               <h3 className="text-lg font-semibold text-gray-800 mb-2">Response</h3>
//               <pre className="text-sm bg-gray-100 p-4 rounded-lg max-h-80 overflow-auto whitespace-pre-wrap">
//                 {response}
//               </pre>
//             </div>
//           )}
//         </>
//       ) : (
//         renderHistoryTab()
//       )}
//     </div>
//   );

//   const renderHistoryTab = () => (
//     <div>
//       <h3 className="text-lg font-semibold text-gray-800 mb-4">Activity Log</h3>
//       {history.length === 0 ? (
//         <p className="text-sm text-gray-500">No changes have been made in this session yet.</p>
//       ) : (
//         <ul className="space-y-2">
//           {history.map((item, index) => (
//             <li key={index} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg border">
//               <div>
//                 <p className="text-sm font-medium text-gray-700">{item.description}</p>
//                 <p className="text-xs text-gray-500">
//                   {new Date(item.timestamp).toLocaleTimeString()}
//                 </p>
//               </div>
//               <button
//                 onClick={() => handleRevert(index)}
//                 disabled={item.reverted || isLoading}
//                 className={`text-xs font-semibold px-3 py-1 rounded-full ${
//                   item.reverted
//                     ? 'bg-gray-200 text-gray-500 cursor-not-allowed'
//                     : 'bg-blue-100 text-blue-700 hover:bg-blue-200'
//                 }`}
//               >
//                 {item.reverted ? 'Reverted' : 'Revert'}
//               </button>
//             </li>
//           ))}
//         </ul>
//       )}
//     </div>
//   );

//   return (
//     <main className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
//       <section className="w-full max-w-2xl p-8 bg-white shadow-lg rounded-2xl border">
//         <h1 className="text-3xl font-bold text-indigo-600 text-center mb-2">
//           AI Database Assistant
//         </h1>
//         <p className="text-center text-gray-500 mb-6 text-sm">
//           Connect to your database and ask questions in plain English.
//         </p>

//         {error && (
//           <div className="my-4 text-red-600 text-sm bg-red-100 p-3 rounded-lg">
//             <strong>Error:</strong> {error}
//           </div>
//         )}

//         {isConnected ? renderQueryInterface() : renderConnectionForm()}

//       </section>
//     </main>
//   );
// }

import React, {
  useState,
  useEffect,
  useCallback,
  useRef,
  useMemo,
} from "react";
import {
  Database,
  Zap,
  History,
  LogOut,
  Loader2,
  Link,
  CornerUpLeft,
  MessageSquare,
  AlertTriangle,
  CheckCircle,
  ChevronDown,
  Server,
  Settings,
  Lock,
  Unlock,
  Code,
  GitBranch,
  Lightbulb,
} from "lucide-react";

// IMPORTANT: Do not change the API URL or function names/values.
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000";

// --- Custom Components for Modern UI ---

// Interactive Button Component (Changed to Cyan/Dark)
const Button = ({
  children,
  onClick,
  disabled,
  variant = "primary",
  className = "",
  type = "button",
}) => {
  const baseStyle =
    "py-3 px-6 rounded-xl font-semibold transition-all duration-300 flex items-center justify-center gap-2 relative overflow-hidden";
  let variantStyle;

  switch (variant) {
    case "primary":
      // Changed from indigo to cyan (Dark theme contrast)
      variantStyle =
        "bg-cyan-500 hover:bg-cyan-600 text-gray-900 disabled:bg-cyan-700 disabled:cursor-not-allowed";
      break;
    case "secondary":
      // Changed from light gray to dark gray
      variantStyle =
        "bg-gray-800 hover:bg-gray-700 text-gray-200 border border-gray-700 disabled:opacity-50";
      break;
    case "danger":
      variantStyle =
        "bg-red-600 hover:bg-red-700 text-white disabled:opacity-50";
      break;
    case "outline":
      // Changed from indigo outline to cyan outline
      variantStyle =
        "bg-gray-900 border border-cyan-500 text-cyan-400 hover:bg-gray-800 disabled:opacity-50";
      break;
    default:
      // Changed from indigo to cyan
      variantStyle =
        "bg-cyan-500 hover:bg-cyan-600 text-gray-900 disabled:opacity-50";
  }

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`${baseStyle} ${variantStyle} ${className}`}
    >
      {children}
    </button>
  );
};

// Updated Input component to handle validation highlighting (Changed to Dark/Cyan)
const Input = ({
  label,
  type = "text",
  value,
  onChange,
  placeholder,
  required = false,
  helpText,
  isPassword = false,
  className = "",
  isInvalid = false,
}) => (
  <div className={className}>
    {/* Enhanced Contrast for Label */}
    <label className="text-sm font-extrabold text-gray-200 flex items-center justify-between">
      {label}
      {/* Changed from indigo to cyan */}
      {helpText && <span className="text-xs text-cyan-400">{helpText}</span>}
    </label>
    <input
      type={isPassword ? "password" : type}
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      // Apply dark mode styles and cyan focus
      className={`w-full mt-1 px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 transition bg-gray-800 text-gray-100
                  ${isInvalid ? "border-red-500 focus:ring-red-500" : "border-gray-700 focus:ring-cyan-500"}`}
      required={required}
    />
  </div>
);

// Helper for getting relevant icon based on option value
const getOptionIcon = (value) => {
  switch (value) {
    case "supabase":
      return <Server size={18} />;
    case "postgresql":
      return <Database size={18} />;
    case "mysql":
      return <Code size={18} />;
    case "mongodb":
      return <GitBranch size={18} />;
    case "read-only":
      return <Lock size={18} />;
    case "read-write":
      return <Unlock size={18} />;
    default:
      return null;
  }
};

// CustomDropdown Component (Icon-Enabled and Modern - Changed to Dark/Cyan)
const CustomDropdown = ({
  label,
  value,
  onChange,
  children,
  className = "",
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  const options = useMemo(() => {
    return React.Children.map(children, (child) => ({
      value: child.props.value,
      label: child.props.children,
    }));
  }, [children]);

  const selectedOption = options.find((opt) => opt.value === value);

  const handleSelect = (optionValue) => {
    // CRITICAL: Mimic the native event structure expected by App.jsx handlers
    const fakeEvent = {
      target: { value: optionValue },
    };
    onChange(fakeEvent);
    setIsOpen(false);
  };

  // Close when clicking outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [dropdownRef]);

  return (
    <div className={className} ref={dropdownRef}>
      {/* Enhanced Contrast for Label */}
      <label className="text-sm font-extrabold text-gray-200">{label}</label>
      <div className="relative mt-1">
        {/* The main button/trigger (Input Box Look) */}
        <button
          type="button"
          onClick={() => setIsOpen(!isOpen)}
          // Changed to dark mode styles and cyan focus
          className="w-full px-4 py-3 border border-gray-700 rounded-lg bg-gray-800 flex items-center justify-between text-left transition duration-200 focus:ring-2 focus:ring-cyan-500 hover:border-cyan-500"
        >
          <span className="text-gray-100 font-medium flex items-center gap-2">
            {getOptionIcon(selectedOption?.value)}
            {selectedOption?.label || "Select an option..."}
          </span>
          <ChevronDown
            size={18}
            className={`text-gray-400 transition-transform ${isOpen ? "rotate-180" : "rotate-0"}`}
          />
        </button>

        {/* The options list (Custom Dropdown Menu) */}
        {isOpen && (
          <ul className="absolute z-20 w-full mt-1 bg-gray-800 border border-gray-700 rounded-lg shadow-xl max-h-60 overflow-y-auto">
            {options.map((option) => (
              <li
                key={option.value}
                onClick={() => handleSelect(option.value)}
                // Changed to cyan highlight
                className={`px-4 py-2 cursor-pointer transition-all duration-150 text-gray-200 font-medium flex items-center gap-2
                                    ${
                                      option.value === value
                                        ? "bg-cyan-600 text-gray-900 hover:bg-cyan-700" // Highlighted selected item
                                        : "hover:bg-gray-700" // Hover effect for unselected item
                                    }`}
              >
                {getOptionIcon(option.value)}
                {option.label}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

// --- Updated Floating Error Dialog Component (Subtle Overlay - Changed to Dark) ---
const FloatingErrorDialog = ({ error, onClose }) => {
  if (!error) return null;

  return (
    // Using dark overlay
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-gray-900/40 backdrop-blur-sm transition-opacity">
      {/* Dialog Content - Using dark mode base */}
      <div className="bg-gray-900 rounded-xl shadow-2xl max-w-sm w-full p-6 mx-4 transform transition-all scale-100 animate-in fade-in zoom-in-95 duration-300 border border-red-700">
        <div className="flex items-center space-x-4 mb-4 pb-3 border-b border-red-900">
          <AlertTriangle size={24} className="text-red-400 flex-shrink-0" />
          <h4 className="text-xl font-extrabold text-red-400">
            Connection Error
          </h4>
        </div>

        <p className="text-sm text-gray-300 mb-6">{error}</p>

        <Button onClick={onClose} className="w-full" variant="danger">
          OK
        </Button>
      </div>
    </div>
  );
};

// --- Main App Component (Logic Unchanged, Colors Updated) ---

export default function App() {
  // --- STATE ---
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  // Dedicated error state for the floating dialog (Connection Form)
  const [connectionError, setConnectionError] = useState("");
  // Dedicated state to track which fields are empty and required
  const [invalidFields, setInvalidFields] = useState({});
  // Dedicated error state for inline display (Query Interface)
  const [queryError, setQueryError] = useState("");

  const [activeTab, setActiveTab] = useState("query");
  const [history, setHistory] = useState([]);

  // Form states (PRESERVED)
  const [dbType, setDbType] = useState("supabase");
  const [connectionMethod, setConnectionMethod] = useState("connection_string");
  const [credentials, setCredentials] = useState({});
  const [mode, setMode] = useState("read-only");

  // Query states (PRESERVED)
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");

  // UI state for showing/hiding form
  const [showConnectForm, setShowConnectForm] = useState(true);

  // Function to close the connection error dialog and clear the error state
  const closeConnectionErrorDialog = () => {
    setConnectionError("");
  };

  // --- FUNCTION LOGIC ---

  const fetchHistory = useCallback(async () => {
    if (!isConnected) return;
    try {
      const res = await fetch(`${API_URL}/history`, {
        credentials: "include",
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
    if (isConnected && activeTab === "history") {
      fetchHistory();
    }
  }, [isConnected, activeTab, fetchHistory]);

  const handleConnect = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setConnectionError(""); // Clear connection error before attempt
    setInvalidFields({}); // Clear previous invalid fields

    // --- Client-side Validation for Empty Fields (New Logic) ---
    let requiredFields = {};
    let missingFields = {};

    // 1. Determine which fields are required based on connection method
    if (connectionMethod === "connection_string" || dbType === "mongodb") {
      requiredFields = { connection_string: credentials.connection_string };
    } else {
      // individual fields
      requiredFields = {
        dbname: credentials.dbname,
        host: credentials.host,
        user: credentials.user,
        password: credentials.password,
      };
    }

    // 2. Check for missing values and populate missingFields map
    for (const [key, value] of Object.entries(requiredFields)) {
      if (!value || String(value).trim() === "") {
        missingFields[key] = true;
      }
    }

    // 3. If missing fields exist, stop, show dialog, and highlight fields
    if (Object.keys(missingFields).length > 0) {
      setInvalidFields(missingFields);
      setConnectionError("Please fill in all required connection fields.");
      setIsLoading(false);
      return;
    }
    // --- End Client-side Validation ---

    try {
      const res = await fetch(`${API_URL}/connect`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ db_type: dbType, ...credentials, mode }),
      });
      const data = await res.json();
      if (res.ok) {
        setTimeout(() => {
          setIsConnected(true);
          setShowConnectForm(false);
        }, 300);
      } else {
        const errorMessage = data.error || "Connection failed.";
        setConnectionError(errorMessage); // Sets the error for the floating dialog
      }
    } catch (err) {
      setConnectionError(err.message);
    } finally {
      setTimeout(() => setIsLoading(false), 500);
    }
  };

  const handleDisconnect = async () => {
    try {
      await fetch(`${API_URL}/disconnect`, {
        method: "POST",
        credentials: "include",
      });
    } catch (err) {
      console.error("Failed to disconnect cleanly:", err);
    } finally {
      setIsConnected(false);
      setCredentials({});
      setQuery("");
      setResponse("");
      setConnectionError("");
      setInvalidFields({}); // Clear invalid fields on disconnect
      setQueryError("");
      setHistory([]);
      setActiveTab("query");
      setShowConnectForm(true);
    }
  };

  const handleQuerySubmit = async (e) => {
    e.preventDefault();
    if (!query) return;
    setIsLoading(true);
    setQueryError("");
    setResponse("");
    try {
      const res = await fetch(`${API_URL}/query`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ query }),
      });
      const data = await res.json();
      if (res.ok) {
        setResponse(data.response);
        if (mode === "read-write") {
          fetchHistory();
        }
      } else {
        const errorMessage = data.error || "Query failed.";
        setQueryError(errorMessage);
      }
    } catch (err) {
      setQueryError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRevert = async (historyId) => {
    setIsLoading(true);
    setQueryError("");
    try {
      const res = await fetch(`${API_URL}/revert`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ history_id: historyId }),
      });
      const data = await res.json();
      if (res.ok) {
        fetchHistory();
      } else {
        const errorMessage = data.error || "Failed to revert change.";
        setQueryError(errorMessage);
      }
    } catch (err) {
      setQueryError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  // Function to handle changes and clear invalid state for the field
  const handleCredentialChange = (key, value) => {
    setCredentials((prev) => ({ ...prev, [key]: value }));
    if (invalidFields[key] && value) {
      setInvalidFields((prev) => ({ ...prev, [key]: false }));
    }
  };

  // --- UI RENDERING COMPONENTS ---

  const renderConnectionForm = () => (
    <div className="h-full flex flex-col">
      <h3 className="text-xl font-bold text-gray-100 mb-4 flex-shrink-0">
        Connect to Your Database
      </h3>

      {/* Scrollable Form Content (Flex Grow is important for scrollless page) */}
      <div className="flex-grow min-h-0 overflow-y-auto pr-2">
        <form onSubmit={handleConnect} className="space-y-4">
          {/* Side-by-Side Dropdowns (Database Type and Operation Mode) */}
          <div className="grid grid-cols-2 gap-4">
            <CustomDropdown
              label="Database Type"
              value={dbType}
              onChange={(e) => {
                setDbType(e.target.value);
                setCredentials({});
                setConnectionMethod("connection_string");
                setInvalidFields({}); // Clear invalid state on type change
              }}
            >
              <option value="supabase">Supabase (PostgreSQL)</option>
              <option value="postgresql">PostgreSQL</option>
              <option value="mysql">MySQL</option>
              <option value="mongodb">MongoDB</option>
            </CustomDropdown>

            <CustomDropdown
              label="Operation Mode"
              value={mode}
              onChange={(e) => setMode(e.target.value)}
            >
              <option value="read-only">Read-Only (Recommended)</option>
              <option value="read-write">Read & Write (Advanced)</option>
            </CustomDropdown>
          </div>

          {mode === "read-write" && (
            // Changed to dark mode warning styles
            <p className="text-xs text-yellow-400 flex items-center bg-yellow-900/40 p-3 rounded-lg flex-shrink-0 border border-yellow-700">
              <AlertTriangle className="mr-2" size={16} />
              Warning: This mode allows the AI to make changes to your database.
            </p>
          )}

          {/* Connection Method Tabs */}
          {dbType !== "mongodb" && (
            <div className="pt-2">
              <label className="text-sm font-extrabold text-gray-200">
                Connection Method
              </label>
              <div className="flex gap-2 mt-2 p-1 bg-gray-800 rounded-xl border border-gray-700">
                <Button
                  variant={
                    connectionMethod === "connection_string"
                      ? "primary"
                      : "secondary"
                  }
                  onClick={() => {
                    setConnectionMethod("connection_string");
                    setCredentials({});
                    setInvalidFields({}); // Clear invalid state on method change
                  }}
                  className="flex-1 py-2 text-sm"
                >
                  <Link size={16} /> Connection String (URL)
                </Button>
                <Button
                  variant={
                    connectionMethod === "individual" ? "primary" : "secondary"
                  }
                  onClick={() => {
                    setConnectionMethod("individual");
                    setCredentials({});
                    setInvalidFields({}); // Clear invalid state on method change
                  }}
                  className="flex-1 py-2 text-sm"
                >
                  <Database size={16} /> Individual Fields
                </Button>
              </div>
            </div>
          )}

          {/* Connection String Fields (Smooth Transition) */}
          <div
            className={`
              rounded-xl border transition-all duration-500 ease-in-out
              ${
                connectionMethod === "connection_string" || dbType === "mongodb"
                  ? "opacity-100 max-h-60 p-4 bg-gray-800 border-cyan-700" // Dark mode accent BG
                  : "opacity-0 max-h-0 p-0 overflow-hidden border-transparent"
              }`}
          >
            <div
              className={`transition-opacity duration-300 ${connectionMethod === "connection_string" || dbType === "mongodb" ? "opacity-100 delay-300" : "opacity-0"}`}
            >
              {(connectionMethod === "connection_string" ||
                dbType === "mongodb") && (
                <>
                  <Input
                    label="Connection String (URL)"
                    type="text"
                    isPassword={true}
                    placeholder={
                      dbType === "supabase"
                        ? "postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres"
                        : dbType === "postgresql"
                          ? "postgresql://user:password@host:5432/dbname"
                          : dbType === "mysql"
                            ? "mysql://user:password@host:3306/dbname"
                            : "mongodb+srv://user:pass@cluster.mongodb.net/dbname"
                    }
                    onChange={(e) =>
                      handleCredentialChange(
                        "connection_string",
                        e.target.value,
                      )
                    }
                    required={true}
                    helpText={
                      dbType === "supabase"
                        ? "Supabase URI"
                        : dbType === "mongodb"
                          ? "MongoDB Atlas"
                          : ""
                    }
                    isInvalid={invalidFields.connection_string} // New prop for highlighting
                  />

                  {/* SUPABASE TIP - Changed to dark mode cyan accent */}
                  {dbType === "supabase" && (
                    <p className="text-xs text-cyan-400 flex items-start bg-cyan-900/40 p-3 rounded-lg mt-3 border border-cyan-700">
                      <Lightbulb
                        className="mr-2 flex-shrink-0 text-cyan-500"
                        size={16}
                      />
                      <span className="font-medium">
                        💡 Tip: In Supabase, go to **Settings** → **Database** →
                        **Connection string** → copy the URI and replace
                        `[YOUR-PASSWORD]` with your actual password.
                      </span>
                    </p>
                  )}
                </>
              )}
            </div>
          </div>

          {/* Individual Fields (Smooth Transition) */}
          <div
            className={`
              rounded-xl border transition-all duration-500 ease-in-out
              ${
                connectionMethod === "individual" && dbType !== "mongodb"
                  ? "opacity-100 max-h-96 p-4 bg-gray-800 border-cyan-700" // Dark mode accent BG
                  : "opacity-0 max-h-0 p-0 overflow-hidden border-transparent"
              }`}
          >
            <div
              className={`transition-opacity duration-300 ${connectionMethod === "individual" && dbType !== "mongodb" ? "opacity-100 delay-300 space-y-4" : "opacity-0 space-y-0"}`}
            >
              {connectionMethod === "individual" && dbType !== "mongodb" && (
                <>
                  {/* Host, Port, and Database Name in one row (grid-cols-3) */}
                  <div className="grid grid-cols-3 gap-4">
                    <Input
                      label="Database Name"
                      placeholder="Database Name"
                      onChange={(e) =>
                        handleCredentialChange("dbname", e.target.value)
                      }
                      required={true}
                      className="col-span-1"
                      isInvalid={invalidFields.dbname} // New prop for highlighting
                    />
                    <Input
                      label="Host"
                      placeholder="e.g., localhost"
                      onChange={(e) =>
                        handleCredentialChange("host", e.target.value)
                      }
                      required={true}
                      className="col-span-1"
                      isInvalid={invalidFields.host} // New prop for highlighting
                    />
                    <Input
                      label="Port"
                      placeholder={`Default: ${dbType === "mysql" ? "3306" : "5432"}`}
                      onChange={(e) =>
                        handleCredentialChange("port", e.target.value)
                      }
                      className="col-span-1"
                    />
                  </div>
                  {/* Username and Password in one row (grid-cols-2) */}
                  <div className="grid grid-cols-2 gap-4">
                    <Input
                      label="Username"
                      placeholder="Username"
                      onChange={(e) =>
                        handleCredentialChange("user", e.target.value)
                      }
                      required={true}
                      isInvalid={invalidFields.user} // New prop for highlighting
                    />
                    <Input
                      label="Password"
                      type="password"
                      isPassword={true}
                      placeholder="Password"
                      onChange={(e) =>
                        handleCredentialChange("password", e.target.value)
                      }
                      required={true}
                      isInvalid={invalidFields.password} // New prop for highlighting
                    />
                  </div>
                </>
              )}
            </div>
          </div>
        </form>
      </div>

      {/* Connect Button with Loading Animation */}
      <Button
        type="submit"
        disabled={isLoading}
        onClick={handleConnect}
        className="w-full mt-4 flex-shrink-0"
      >
        {isLoading ? (
          <div className="flex items-center gap-2">
            <Loader2 className="animate-spin" size={20} />
            Connecting...
          </div>
        ) : (
          <div className="flex items-center gap-2">
            <Link size={20} />
            Connect
          </div>
        )}
      </Button>

      {/* Security Note */}
      <p className="text-xs text-gray-500 text-center mt-4 flex-shrink-0">
        🔒 Your credentials are used for temporary connections and are never
        stored permanently.
      </p>
    </div>
  );

  const renderQueryInterface = () => (
    <div className="h-full flex flex-col">
      {/* Header/Nav Area (Fixed Height) */}
      <div className="flex justify-between items-center pb-3 mb-4 border-b border-gray-700 flex-shrink-0">
        <div className="flex items-center gap-6">
          <Button
            variant={activeTab === "query" ? "primary" : "outline"}
            onClick={() => setActiveTab("query")}
            className="py-1.5 px-3 text-sm"
          >
            <Zap size={16} /> Query
          </Button>
          {mode === "read-write" && (
            <Button
              variant={activeTab === "history" ? "primary" : "outline"}
              onClick={() => setActiveTab("history")}
              className="py-1.5 px-3 text-sm"
            >
              <History size={16} /> History
            </Button>
          )}
        </div>
        <div className="flex items-center gap-4">
          {/* Changed status colors to dark mode friendly */}
          <div
            className={`p-2 rounded-lg text-sm font-medium flex items-center gap-2 ${isConnected ? "bg-green-900/40 text-green-400" : "bg-red-900/40 text-red-400"}`}
          >
            {isConnected
              ? `Mode: ${mode === "read-write" ? "R/W" : "R-O"}`
              : "Disconnected"}
          </div>
          <Button
            variant="secondary"
            onClick={handleDisconnect}
            className="py-1.5 px-3 text-sm"
          >
            <LogOut size={16} /> Disconnect
          </Button>
        </div>
      </div>

      {/* Content Area - Fixed height, internal scroll container */}
      <div className="flex-grow min-h-0 overflow-y-auto pr-2">
        {activeTab === "query" ? renderQueryTab() : renderHistoryTab()}
      </div>
    </div>
  );

  const renderQueryTab = () => (
    <div className="space-y-4 h-full flex flex-col">
      <form
        onSubmit={handleQuerySubmit}
        className="flex flex-col space-y-4 flex-shrink-0"
      >
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask your query... (e.g., 'How many students are in the Computer department?')"
          // Changed to dark mode input styles
          className="w-full px-4 py-3 border border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-cyan-500 transition resize-none bg-gray-800 text-gray-100"
          rows="4"
        />
        <Button type="submit" disabled={isLoading} className="w-full">
          {isLoading ? (
            <Loader2 className="animate-spin" size={20} />
          ) : (
            <MessageSquare size={20} />
          )}
          {isLoading ? "Processing..." : "Submit Query"}
        </Button>
      </form>

      {/* Response Area - Takes remaining space */}
      <div className="flex-grow mt-4 min-h-0 flex flex-col">
        <h3 className="text-lg font-semibold text-gray-100 mb-2 flex items-center flex-shrink-0">
          <Zap size={18} className="mr-2 text-cyan-400" /> AI Response
        </h3>
        {isLoading && (
          // Changed loading text color and background
          <div className="text-center text-cyan-400 p-4 bg-gray-800 rounded-lg flex-shrink-0">
            <Loader2 className="animate-spin mx-auto" size={20} />
            Processing your query...
          </div>
        )}
        {/* INLINE ERROR DISPLAY FOR QUERY INTERFACE - Changed to dark mode error styles */}
        {queryError && (
          <div className="my-2 p-3 rounded-xl bg-red-900/40 border border-red-700 text-red-400 text-sm font-medium flex items-start gap-3 flex-shrink-0">
            <AlertTriangle size={20} className="mt-0.5 flex-shrink-0" />
            <div>
              <strong>Error:</strong>
              <p className="mt-1 font-normal text-gray-200">{queryError}</p>
            </div>
          </div>
        )}
        {response && (
          // Changed response code block color to a cool/sky tone
          <pre className="text-sm bg-gray-950 text-sky-400 p-4 rounded-lg flex-grow overflow-y-auto whitespace-pre-wrap font-mono shadow-inner border border-gray-800">
            {response}
          </pre>
        )}
      </div>
    </div>
  );

  const renderHistoryTab = () => (
    <div className="h-full flex flex-col">
      <h3 className="text-lg font-semibold text-gray-100 mb-4 flex items-center flex-shrink-0">
        <History size={18} className="mr-2 text-cyan-400" /> Activity Log (
        {mode.toUpperCase()})
      </h3>
      {history.length === 0 ? (
        // Changed empty state colors
        <p className="text-sm text-gray-400 p-4 bg-gray-800 rounded-lg text-center flex-shrink-0">
          No changes have been made in this session yet.
        </p>
      ) : (
        <ul className="space-y-3 overflow-y-auto pr-2 flex-grow">
          {history.map((item, index) => (
            <li
              key={index}
              // Changed list item colors
              className={`flex justify-between items-center p-4 rounded-xl border transition-shadow ${item.reverted ? "bg-gray-800 border-gray-700" : "bg-gray-900 border-cyan-700 shadow-md shadow-black/30"}`}
            >
              <div>
                <p
                  className={`text-sm font-medium ${item.reverted ? "text-gray-500 line-through" : "text-gray-100"}`}
                >
                  {item.description}
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  {new Date(item.timestamp).toLocaleTimeString()}
                </p>
              </div>
              <Button
                onClick={() => handleRevert(index)}
                disabled={item.reverted || isLoading || mode !== "read-write"}
                variant={item.reverted ? "secondary" : "danger"}
                className="text-xs py-1.5 px-3"
              >
                {item.reverted ? (
                  <CheckCircle size={14} />
                ) : (
                  <CornerUpLeft size={14} />
                )}
                {item.reverted ? "Reverted" : "Revert"}
              </Button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );

  return (
    // The main container for the application. Changed background color.
    <main className="min-h-screen h-screen bg-gray-950 flex items-center justify-center p-4 overflow-hidden">
      {/* Wrapper uses max-w-6xl for maximum width */}
      <div className="w-full max-w-6xl h-full max-h-[95vh] flex flex-col">
        {/* Card-less main content area. Changed background and shadow. */}
        <div className="flex flex-col h-full overflow-hidden p-8 bg-gray-900 rounded-2xl shadow-2xl shadow-black/50">
          <header className="flex flex-col items-center mb-6 flex-shrink-0">
            {/* Database Icon and Title - Changed from indigo to cyan */}
            <h1 className="text-4xl font-extrabold text-cyan-400 mb-1 flex items-center gap-2">
              <Database className="animate-pulse" size={32} />
              AI Database Editor
            </h1>
            {/* Subtitle Text - Changed text color */}
            <p className="text-center text-gray-400 text-sm">
              Connect to your database and ask questions in plain English.
            </p>
          </header>

          {/* Main Content Area */}
          <div className="flex-grow min-h-0 relative">
            <div
              className={`absolute inset-0 transition-opacity duration-500 ${!isConnected || showConnectForm ? "opacity-100 z-10" : "opacity-0 pointer-events-none"}`}
            >
              {renderConnectionForm()}
            </div>
            <div
              className={`absolute inset-0 transition-opacity duration-500 ${isConnected && !showConnectForm ? "opacity-100 z-10" : "opacity-0 pointer-events-none"}`}
            >
              {renderQueryInterface()}
            </div>
          </div>
        </div>
      </div>

      {/* Floating Error Dialog for Connection Errors only (Now with subtle overlay) */}
      <FloatingErrorDialog
        error={connectionError}
        onClose={closeConnectionErrorDialog}
      />
    </main>
  );
}
