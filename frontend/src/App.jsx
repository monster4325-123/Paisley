import { useState } from "react";
import ProteinViewer from "./ProteinViewer";
import {
  getProteinFromUniProt,
  getProteinFromAlphaFold,
  getProteinFromRCSB,
  analyzeMutation
} from "./services/api";

function App() {
  const [accession, setAccession] = useState("P04637");
  const [protein, setProtein] = useState(null);
  const [alphaFold, setAlphaFold] = useState(null);
  const [rcsb, setRcsb] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [mutation, setMutation] = useState("");
  const [mutationResult, setMutationResult] = useState(null);
  const [mutationLoading, setMutationLoading] = useState(false);
  const [mutationError, setMutationError] = useState("");

const searchProtein = async () => {
  try {
    setLoading(true);
    setError("");
    setProtein(null);
    setAlphaFold(null);

    const proteinData = await getProteinFromUniProt(accession);
    const alphaFoldData = await getProteinFromAlphaFold(accession);

    setProtein(proteinData);
    setAlphaFold(alphaFoldData);
  } catch (err) {
    setError(err.message);
  } finally {
    setLoading(false);
  }
};
const handleMutationAnalysis = async () => {
  try {
    setMutationLoading(true);
    setMutationError("");
    setMutationResult(null);

    const result = await analyzeMutation(
      accession,
      mutation
    );

    setMutationResult(result);

  } catch (err) {
    setMutationError(err.message);
  } finally {
    setMutationLoading(false);
  }
};
  return (
    <div className="min-h-screen bg-slate-950 p-8 text-white">
      <h1 className="text-4xl font-bold text-cyan-400 mb-2">
        Paisley
      </h1>

      <p className="text-gray-400 mb-6">
        Protein Structure Viewer
      </p>

      {/* Protein Search */}
      <div className="mb-8 flex gap-3">
        <input
          type="text"
          value={accession}
          onChange={(e) => setAccession(e.target.value)}
          placeholder="Enter UniProt accession"
          className="px-4 py-3 rounded-lg bg-slate-800 border border-slate-700 text-white"
        />

        <button
          onClick={searchProtein}
          className="px-6 py-3 rounded-lg bg-cyan-500 text-black font-semibold"
        >
          Search
        </button>
      </div>

      {/* Loading */}
      {loading && (
        <p className="text-gray-400 mb-6">
          Fetching protein...
        </p>
      )}

      {/* Error */}
      {error && (
        <p className="text-red-400 mb-6">
          {error}
        </p>
      )}

      {/* Protein Information */}
      {protein && (
        <div className="mb-8 p-6 bg-slate-900 rounded-xl border border-slate-700">
          <h2 className="text-2xl font-bold text-cyan-400 mb-4">
            {protein.protein_name}
          </h2>

          <p className="text-gray-300">
            <strong>Accession:</strong> {protein.accession}
          </p>

          <p className="text-gray-300">
            <strong>Gene:</strong> {protein.gene}
          </p>

          <p className="text-gray-300">
            <strong>Organism:</strong> {protein.organism}
          </p>

          <p className="text-gray-300">
            <strong>Length:</strong> {protein.length}
          </p>
        </div>
      )}
      {alphaFold && (
  <div className="mb-8 p-6 bg-slate-900 rounded-xl border border-slate-700">
    <h2 className="text-2xl font-bold text-cyan-400 mb-4">
      AlphaFold Structure
    </h2>

    <p className="text-gray-300">
      <strong>Entry ID:</strong> {alphaFold.entry_id}
    </p>

    <p className="text-gray-300">
      <strong>Confidence:</strong> {alphaFold.confidence}
    </p>

    <p className="text-gray-300">
      <strong>Confidence Type:</strong> {alphaFold.confidence_type}
    </p>

    <p className="text-gray-300 mt-3">
      <strong>Structure:</strong>{" "}
      <a
        href={alphaFold.pdb_url}
        target="_blank"
        rel="noopener noreferrer"
        className="text-cyan-400 underline"
      >
        View PDB
      </a>
    </p>
  </div>
  
)}
<div className="mb-8 p-6 bg-slate-900 rounded-xl border border-slate-700">
  <h2 className="text-2xl font-bold text-cyan-400 mb-4">
    RCSB PDB Structure
  </h2>

  <div className="flex gap-3">
    <input
      type="text"
      placeholder="Enter PDB ID (e.g. 1TUP)"
      id="pdbInput"
      className="px-4 py-3 rounded-lg bg-slate-800 border border-slate-700 text-white"
    />

    <button
      onClick={async () => {
        try {
          const pdbId = document.getElementById("pdbInput").value;

          if (!pdbId) return;

          const data = await getProteinFromRCSB(pdbId);
          setRcsb(data);
        } catch (err) {
          setError(err.message);
        }
      }}
      className="px-6 py-3 rounded-lg bg-cyan-500 text-black font-semibold"
    >
      Load Structure
    </button>
  </div>
</div>
{rcsb && (
  <div className="mb-8 p-6 bg-slate-900 rounded-xl border border-slate-700">
    <h2 className="text-2xl font-bold text-cyan-400 mb-4">
      RCSB Structure
    </h2>

    <p className="text-gray-300">
      <strong>PDB ID:</strong> {rcsb.pdb_id}
    </p>

    <p className="mt-3">
      <a
        href={rcsb.structure_url}
        target="_blank"
        rel="noopener noreferrer"
        className="text-cyan-400 underline"
      >
        View on RCSB PDB
      </a>
    </p>
  </div>
)}
{/* Mutation Analysis */}
<div className="mb-8 p-6 bg-slate-900 rounded-xl border border-slate-700">

  <h2 className="text-2xl font-bold text-cyan-400 mb-2">
    Mutation Analysis
  </h2>

  <p className="text-gray-400 mb-5">
    Enter a mutation such as R175H to validate it against the
    protein sequence.
  </p>

  <div className="flex gap-3">

    <input
      type="text"
      value={mutation}
      onChange={(e) => setMutation(e.target.value)}
      placeholder="Example: R175H"
      className="px-4 py-3 rounded-lg bg-slate-800 border border-slate-700 text-white"
    />

    <button
      onClick={handleMutationAnalysis}
      className="px-6 py-3 rounded-lg bg-cyan-500 text-black font-semibold"
    >
      Analyze Mutation
    </button>

  </div>

  {/* Loading */}
  {mutationLoading && (
    <p className="text-gray-400 mt-4">
      Analyzing mutation...
    </p>
  )}

  {/* Error */}
  {mutationError && (
    <p className="text-red-400 mt-4">
      {mutationError}
    </p>
  )}

  {/* Result */}
 {mutationResult && (
  <div className="mt-6 p-5 bg-slate-800 rounded-lg border border-slate-700">

    <h3 className="text-xl font-bold text-white mb-4">
      Mutation Analysis Result
    </h3>

    {/* Mutation Information */}
    <div className="mb-6">
      <h4 className="text-lg font-semibold text-cyan-400 mb-3">
        Mutation Information
      </h4>

      <p className="text-gray-300 mb-2">
        <strong>Mutation:</strong>{" "}
        {mutationResult.mutation}
      </p>

      <p className="text-gray-300 mb-2">
        <strong>Position:</strong>{" "}
        {mutationResult.position}
      </p>

      <p className="text-gray-300 mb-2">
        <strong>Original Amino Acid:</strong>{" "}
        {mutationResult.original_amino_acid}
      </p>

      <p className="text-gray-300 mb-2">
        <strong>New Amino Acid:</strong>{" "}
        {mutationResult.new_amino_acid}
      </p>

      <p
        className={
          mutationResult.valid
            ? "text-green-400 font-semibold mt-4"
            : "text-red-400 font-semibold mt-4"
        }
      >
        {mutationResult.valid
          ? "✓ Valid mutation"
          : "✕ Invalid mutation"}
      </p>

      <p className="text-gray-400 mt-2">
        {mutationResult.message}
      </p>
    </div>
    {/* Mutation Properties */}
{mutationResult.valid &&
  mutationResult.property_comparison && (
    <div className="mb-6 pt-5 border-t border-slate-700">

      <h4 className="text-lg font-semibold text-cyan-400 mb-3">
        Mutation Properties
      </h4>

      <div className="mb-4">

        <p className="text-white text-lg font-semibold">
          {mutationResult.property_comparison.original_name}
          {" "}
          ({mutationResult.property_comparison.original_code})
          {" → "}
          {mutationResult.property_comparison.mutant_name}
          {" "}
          ({mutationResult.property_comparison.mutant_code})
        </p>

        <p className="text-gray-400 mt-1">
          Position {mutationResult.position}
        </p>

      </div>

      <div className="overflow-x-auto">

        <table className="w-full text-left">

          <thead>
            <tr className="border-b border-slate-600">

              <th className="py-2 text-gray-400">
                Property
              </th>

              <th className="py-2 text-gray-400">
                Original
              </th>

              <th className="py-2 text-gray-400">
                Mutant
              </th>

            </tr>
          </thead>

          <tbody>

            <tr className="border-b border-slate-700">

              <td className="py-2 text-gray-300">
                Class
              </td>

              <td className="py-2 text-white">
                {mutationResult.property_comparison.original_class}
              </td>

              <td className="py-2 text-white">
                {mutationResult.property_comparison.mutant_class}
              </td>

            </tr>

            <tr className="border-b border-slate-700">

              <td className="py-2 text-gray-300">
                Charge
              </td>

              <td className="py-2 text-white">
                {mutationResult.property_comparison.original_charge}
              </td>

              <td className="py-2 text-white">
                {mutationResult.property_comparison.mutant_charge}
              </td>

            </tr>

            <tr className="border-b border-slate-700">

              <td className="py-2 text-gray-300">
                Polarity
              </td>

              <td className="py-2 text-white">
                {mutationResult.property_comparison.original_polarity}
              </td>

              <td className="py-2 text-white">
                {mutationResult.property_comparison.mutant_polarity}
              </td>

            </tr>

          </tbody>

        </table>

      </div>

    </div>
  )}
  {/* Explainable Interpretation */}
{mutationResult.valid &&
  mutationResult.interpretation && (
    <div className="mb-6 pt-5 border-t border-slate-700">

      <h4 className="text-lg font-semibold text-cyan-400 mb-3">
        Explainable Interpretation
      </h4>

      <div className="p-4 bg-slate-900 rounded-lg border border-slate-700">

        <p className="text-gray-300 leading-7">
          {mutationResult.interpretation}
        </p>

      </div>

    </div>
  )}

    {/* Structural Information */}
    {mutationResult.valid &&
      mutationResult.structure_source && (
        <div className="mb-6 pt-5 border-t border-slate-700">

          <h4 className="text-lg font-semibold text-cyan-400 mb-3">
            Structural Context
          </h4>

          <p className="text-gray-300 mb-2">
            <strong>Structure Source:</strong>{" "}
            {mutationResult.structure_source}
          </p>

          <p className="text-gray-300 mb-2">
            <strong>Chain:</strong>{" "}
            {mutationResult.structure_chain}
          </p>

          <p className="text-gray-300 mb-2">
            <strong>Residue:</strong>{" "}
            {mutationResult.structure_residue_name}{" "}
            {mutationResult.structure_residue_number}
          </p>

          <p className="text-gray-300 mb-2">
            <strong>X:</strong>{" "}
            {mutationResult.structure_coordinates?.x}
          </p>

          <p className="text-gray-300 mb-2">
            <strong>Y:</strong>{" "}
            {mutationResult.structure_coordinates?.y}
          </p>

          <p className="text-gray-300 mb-2">
            <strong>Z:</strong>{" "}
            {mutationResult.structure_coordinates?.z}
          </p>

        </div>
      )}

    {/* Nearby Residues */}
    {mutationResult.nearby_residues?.length > 0 && (
      <div className="pt-5 border-t border-slate-700">

        <h4 className="text-lg font-semibold text-cyan-400 mb-3">
          Nearby Residues
        </h4>

        <div className="overflow-x-auto">

          <table className="w-full text-left">

            <thead>
              <tr className="border-b border-slate-600">
                <th className="py-2 text-gray-400">
                  Chain
                </th>

                <th className="py-2 text-gray-400">
                  Residue
                </th>

                <th className="py-2 text-gray-400">
                  Position
                </th>

                <th className="py-2 text-gray-400">
                  Distance (Å)
                </th>
              </tr>
            </thead>

            <tbody>

              {mutationResult.nearby_residues.map(
                (residue, index) => (
                  <tr
                    key={`${residue.chain}-${residue.residue_number}-${index}`}
                    className="border-b border-slate-700"
                  >

                    <td className="py-2 text-gray-300">
                      {residue.chain}
                    </td>

                    <td className="py-2 text-white font-semibold">
                      {residue.residue_name}
                    </td>

                    <td className="py-2 text-gray-300">
                      {residue.residue_number}
                    </td>

                    <td className="py-2 text-gray-300">
                      {residue.distance} Å
                    </td>

                  </tr>
                )
              )}

            </tbody>

          </table>

        </div>
      </div>
    )}

  </div>
)}
</div>
      {/* 3D Protein Viewer */}
      <div className="bg-slate-900 rounded-xl overflow-hidden">
       <ProteinViewer 
          structureUrl={alphaFold?.pdb_url}
          mutationPosition={mutationResult?.position}
          nearbyResidues={mutationResult?.nearby_residues}
        />
      </div>
    </div>
  );
}

export default App;