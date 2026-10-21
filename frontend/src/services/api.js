const API_BASE_URL = "http://127.0.0.1:8000";

export async function getProteinFromUniProt(accession) {
  const response = await fetch(
    `${API_BASE_URL}/protein/uniprot/${accession}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch protein data");
  }

  return response.json();
}

export async function getProteinFromAlphaFold(accession) {
  const response = await fetch(
    `${API_BASE_URL}/protein/alphafold/${accession}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch AlphaFold data");
  }

  return response.json();
}

export async function getProteinFromRCSB(pdbId) {
  const response = await fetch(
    `${API_BASE_URL}/protein/rcsb/${pdbId}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch RCSB data");
  }

  return response.json();
}
export async function analyzeMutation(accession, mutation) {
  const response = await fetch(
    `${API_BASE_URL}/mutation/analyze`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        accession,
        mutation,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to analyze mutation");
  }

  return data;
}