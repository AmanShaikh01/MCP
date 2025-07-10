// {
//   "name": "web",
//   "private": true,
//   "version": "0.0.0",
//   "type": "module",
//   "scripts": {
//     "dev": "vite",
//     "build": "vite build",
//     "lint": "eslint .",
//     "preview": "vite preview"
//   },
//   "dependencies": {
//     "@tailwindcss/vite": "^4.1.10",
//     "react": "^19.1.0",
//     "react-dom": "^19.1.0",
//     "tailwindcss": "^4.1.10"
//   },
//   "devDependencies": {
//     "@eslint/js": "^9.29.0",
//     "@types/react": "^19.1.8",
//     "@types/react-dom": "^19.1.6",
//     "@vitejs/plugin-react": "^4.5.2",
//     "eslint": "^9.29.0",
//     "eslint-plugin-react-hooks": "^5.2.0",
//     "eslint-plugin-react-refresh": "^0.4.20",
//     "globals": "^16.2.0",
//     "vite": "^7.0.0"
//   }
// }

// import { useState } from 'react'

// const API_BASE_URL = 'http://localhost:5000'

// function App() {
//   const [query, setQuery] = useState('')
//   const [response, setResponse] = useState('')
//   const [loading, setLoading] = useState(false)
//   const [error, setError] = useState('')
//   const [dbStatus, setDbStatus] = useState(null)

//   const handleQuery = async (e) => {
//     e.preventDefault()
//     if (!query.trim()) return

//     setLoading(true)
//     setError('')
//     setResponse('')

//     try {
//       const res = await fetch(`${API_BASE_URL}/query`, {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ query: query.trim() }),
//       })

//       const data = await res.json()

//       if (!res.ok) {
//         throw new Error(data.error || 'Failed to process query')
//       }

//       setResponse(data.response)
//     } catch (err) {
//       setError(err.message || 'An error occurred')
//     } finally {
//       setLoading(false)
//     }
//   }

//   const testDatabase = async () => {
//     setLoading(true)
//     setError('')
//     setDbStatus(null)

//     try {
//       const res = await fetch(`${API_BASE_URL}/test-db`)
//       const data = await res.json()

//       if (!res.ok) {
//         throw new Error(data.error || 'Database test failed')
//       }

//       setDbStatus(data)
//     } catch (err) {
//       setError(err.message || 'Database connection failed')
//     } finally {
//       setLoading(false)
//     }
//   }

//   const clearResults = () => {
//     setResponse('')
//     setError('')
//     setDbStatus(null)
//   }

//   const formatResponse = (text) => {
//     if (!text) return ''
    
//     // Simple formatting for JSON responses
//     try {
//       const parsed = JSON.parse(text)
//       return JSON.stringify(parsed, null, 2)
//     } catch {
//       return text
//     }
//   }

//   return (
//     <div className="min-h-screen bg-gray-50">
//       <div className="max-w-4xl mx-auto p-6">
//         {/* Header */}
//         <div className="text-center mb-8">
//           <h1 className="text-3xl font-bold text-gray-900 mb-2">
//             Student Database Query System
//           </h1>
//           <p className="text-gray-600">
//             Query student records using natural language
//           </p>
//         </div>

//         {/* Database Status */}
//         <div className="mb-6">
//           <button
//             onClick={testDatabase}
//             disabled={loading}
//             className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
//           >
//             {loading ? 'Testing...' : 'Test Database Connection'}
//           </button>
//         </div>

//         {/* Query Form */}
//         <div className="bg-white rounded-lg shadow-md p-6 mb-6">
//           <form onSubmit={handleQuery} className="space-y-4">
//             <div>
//               <label htmlFor="query" className="block text-sm font-medium text-gray-700 mb-2">
//                 Enter your query:
//               </label>
//               <textarea
//                 id="query"
//                 value={query}
//                 onChange={(e) => setQuery(e.target.value)}
//                 placeholder="e.g., Show all students in Computer department with CGPA > 8.5"
//                 className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
//                 rows="3"
//                 disabled={loading}
//               />
//             </div>
//             <div className="flex gap-3">
//               <button
//                 type="submit"
//                 disabled={loading || !query.trim()}
//                 className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 disabled:opacity-50 transition-colors"
//               >
//                 {loading ? 'Processing...' : 'Send Query'}
//               </button>
//               <button
//                 type="button"
//                 onClick={clearResults}
//                 className="bg-gray-500 text-white px-6 py-2 rounded-lg hover:bg-gray-600 transition-colors"
//               >
//                 Clear
//               </button>
//             </div>
//           </form>
//         </div>

//         {/* Results Section */}
//         {(response || error || dbStatus) && (
//           <div className="bg-white rounded-lg shadow-md p-6">
//             <h2 className="text-xl font-semibold text-gray-900 mb-4">Results</h2>
            
//             {/* Error Display */}
//             {error && (
//               <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
//                 <div className="flex items-center">
//                   <div className="flex-shrink-0">
//                     <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
//                       <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
//                     </svg>
//                   </div>
//                   <div className="ml-3">
//                     <h3 className="text-sm font-medium text-red-800">Error</h3>
//                     <p className="text-sm text-red-700 mt-1">{error}</p>
//                   </div>
//                 </div>
//               </div>
//             )}

//             {/* Database Status Display */}
//             {dbStatus && (
//               <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
//                 <h3 className="text-sm font-medium text-green-800 mb-2">Database Status</h3>
//                 <div className="text-sm text-green-700 space-y-1">
//                   <p><strong>Status:</strong> {dbStatus.message}</p>
//                   <p><strong>Total Students:</strong> {dbStatus.total_students}</p>
//                   <p><strong>Departments:</strong> {dbStatus.departments?.join(', ')}</p>
//                   {dbStatus.cgpa_stats && (
//                     <p><strong>Students with CGPA {">"} 8:</strong> {dbStatus.cgpa_stats.count_above_8}</p>
//                   )}
//                 </div>
//               </div>
//             )}

//             {/* Query Response Display */}
//             {response && (
//               <div className="bg-gray-50 rounded-lg p-4">
//                 <h3 className="text-sm font-medium text-gray-800 mb-2">Query Response</h3>
//                 <pre className="text-sm text-gray-700 whitespace-pre-wrap overflow-x-auto">
//                   {formatResponse(response)}
//                 </pre>
//               </div>
//             )}
//           </div>
//         )}

//         {/* Example Queries */}
//         <div className="bg-white rounded-lg shadow-md p-6 mt-6">
//           <h2 className="text-xl font-semibold text-gray-900 mb-4">Example Queries</h2>
//           <div className="grid md:grid-cols-2 gap-4">
//             <div>
//               <h3 className="font-medium text-gray-800 mb-2">Search Queries:</h3>
//               <ul className="text-sm text-gray-600 space-y-1">
//                 <li>• "Show all students"</li>
//                 <li>• "List students in Computer department"</li>
//                 <li>• "Find students with CGPA {">"} 8.5"</li>
//                 <li>• "How many students in Mechanical?"</li>
//               </ul>
//             </div>
//             <div>
//               <h3 className="font-medium text-gray-800 mb-2">CRUD Operations:</h3>
//               <ul className="text-sm text-gray-600 space-y-1">
//                 <li>• "Add student John with roll 123"</li>
//                 <li>• "Update student 123 CGPA to 9.0"</li>
//                 <li>• "Delete student with roll 123"</li>
//                 <li>• "Add student Jane, Computer, 8.5 CGPA"</li>
//               </ul>
//             </div>
//           </div>
//         </div>  
//       </div>
//     </div>
//   )
// }

// export default App

// src/App.jsx
import React, { useState } from 'react'

export default function App() {
  const [query, setQuery] = useState('')
  const [response, setResponse] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setResponse('')

    try {
      const res = await fetch('http://localhost:5000/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      })

      const data = await res.json()
      if (res.ok) {
        setResponse(data.response)
      } else {
        setError(data.error || 'Something went wrong')
      }
    } catch (err) {
      setError('Failed to connect to server.')
    } finally {
      setLoading(false)
    }
  }

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
            {loading ? 'Loading...' : 'Submit Query'}
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
  )
}
