"use client";

import { useRouter } from "next/navigation";

export default function HomePage() {
  const router = useRouter();

  return (
    <div style={{ padding: 40 }}>
      <h1>LLM Evaluation Dashboard</h1>
      <p>
        Compare large language models and detect hallucinations.
      </p>

      <div style={{ marginTop: 30 }}>
        <button
          onClick={() => router.push("/compare")}
          style={{
            padding: "10px 20px",
            fontSize: 16,
            cursor: "pointer"
          }}
        >
          Start New Comparison
        </button>

        <button
          onClick={() => router.push("/experiments")}
          style={{
            padding: "10px 20px",
            fontSize: 16,
            marginLeft: 10,
            cursor: "pointer"
          }}
        >
          View Past Experiments
        </button>

        <button
          onClick={() => router.push("/leaderboard")}
          style={{
            padding: "10px 20px",
            fontSize: 16,
            marginLeft: 10,
            cursor: "pointer"
          }}
        >
          View Leaderboard
        </button>
      </div>
    </div>
  );
}