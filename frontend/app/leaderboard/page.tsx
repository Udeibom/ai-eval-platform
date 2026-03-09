import { getAllExperimentSummaries } from "@/lib/api";
import { ExperimentSummary } from "@/types/experiment";

export default async function LeaderboardPage() {
  const experiments: ExperimentSummary[] = await getAllExperimentSummaries();

  const sorted = [...experiments].sort(
    (a, b) => b.mean_score - a.mean_score
  );

  return (
    <div className="max-w-6xl mx-auto p-8">
      <h1 className="text-3xl font-bold mb-8">Leaderboard</h1>

      <table className="w-full border-collapse">
        <thead>
          <tr className="border-b">
            <th className="text-left p-2">Model</th>
            <th className="p-2">Mean Score</th>
            <th className="p-2">Hallucination %</th>
            <th className="p-2">Avg Latency</th>
          </tr>
        </thead>

        <tbody>
          {sorted.map((exp) => (
            <tr key={exp.experiment_id} className="border-b">
              <td className="p-2">{exp.model_name}</td>
              <td className="p-2">{exp.mean_score.toFixed(2)}</td>
              <td className="p-2">
                {(exp.hallucination_rate * 100).toFixed(1)}%
              </td>
              <td className="p-2">{exp.avg_latency.toFixed(0)} ms</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}