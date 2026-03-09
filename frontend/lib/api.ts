import { Experiment } from "@/types/experiment";
import { ExperimentSummary } from "@/types/experiment";

export const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function getExperiments(): Promise<Experiment[]> {
  const res = await fetch(`${API_URL}/experiments`);
  if (!res.ok) {
    throw new Error("Failed to fetch experiments");
  }
  return res.json();
}

export async function getExperimentSummary(id: string) {
  const res = await fetch(`${API_URL}/experiments/${id}/summary`);
  if (!res.ok) {
    throw new Error("Failed to fetch experiment summary");
  }
  return res.json();
}

export async function getAllExperimentSummaries(): Promise<ExperimentSummary[]> {
  const res = await fetch(`${API_URL}/experiments/summaries`);

  if (!res.ok) {
    throw new Error("Failed to fetch experiment summaries");
  }

  const data = await res.json();

  // Handle APIs that wrap results
  return Array.isArray(data) ? data : data.summaries ?? data.data ?? [];
}

export async function compareExperiments(a: string, b: string) {
  const res = await fetch(
    `${API_URL}/experiments/compare?experiment_a=${a}&experiment_b=${b}`
  );
  if (!res.ok) throw new Error("Comparison failed");
  return res.json();
}

export async function compareStatistics(a: string, b: string) {
  const res = await fetch(
    `${API_URL}/experiments/compare/statistics?experiment_a=${a}&experiment_b=${b}`
  );
  if (!res.ok) throw new Error("Statistical test failed");
  return res.json();
}