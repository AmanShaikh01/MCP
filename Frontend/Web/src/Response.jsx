import React from "react";

const ResponseDisplay = ({ response }) => {
  if (!response) {
    return null;
  }

  let parsedData;
  try {
    parsedData = JSON.parse(response);
  } catch {
    return (
      <div className="mt-4 text-sm bg-[#0f172a] p-4 rounded-lg border border-gray-700">
        <p className="text-gray-300">{response}</p>
      </div>
    );
  }

  return (
    <div className="mt-4 text-sm bg-[#0f172a] p-4 rounded-lg border border-gray-700 max-h-60 overflow-auto">
      {parsedData.message && <p className="mb-3 text-cyan-400 font-medium">{parsedData.message}</p>}
      
      {parsedData.students && (
        <div>
          {parsedData.students.length === 1 ? (
            parsedData.students.map((student, index) => (
              <div key={index} className="p-3 bg-[#1e293b] rounded-md border border-gray-600">
                <p className="font-semibold text-white">{student.name}</p>
                <p className="text-xs text-gray-400 mt-1">Roll No: {student.roll_number}</p>
                <p className="text-xs text-gray-400">Department: {student.department}</p>
                <p className="text-xs text-gray-400">CGPA: {student.cgpa}</p>
              </div>
            ))
          ) : (
            <ul className="space-y-2">
              {parsedData.students.map((student, index) => (
                <li key={index} className="p-2 bg-[#1e293b] rounded-md border border-gray-600 text-gray-300">
                  {student.name}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}

      {parsedData.error && <p className="text-red-400 font-medium">Error: {parsedData.error}</p>}
    </div>
  );
};

export default ResponseDisplay;