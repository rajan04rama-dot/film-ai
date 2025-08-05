"use client";
import { useState } from "react";
import axios from "axios";

export default function Home() {
  const [input, setInput] = useState("");
  const [recs, setRecs]   = useState([]);

  const getRecs = async () => {
    const res = await axios.post(
      process.env.NEXT_PUBLIC_BACKEND_URL + "/recommendations",
      { description: input }
    );
    setRecs(res.data);
  };

  return (
    <main className="p-8 max-w-xl mx-auto">
      <h1 className="text-2xl mb-4">Film AI 🎬</h1>
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Describe your mood or desired film…"
        className="w-full border p-2 rounded mb-2"
      />
      <button
        onClick={getRecs}
        className="bg-blue-600 text-white px-4 py-2 rounded"
      >
        Recommend
      </button>
      <div className="mt-6 space-y-4">
        {recs.map((m,i) => (
          <div key={i} className="border p-3 rounded">
            <h2 className="font-bold">{m.title}</h2>
            <p>{m.overview}</p>
          </div>
        ))}
      </div>
    </main>
  );
}
