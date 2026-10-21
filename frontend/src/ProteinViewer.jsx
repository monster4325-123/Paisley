import { useEffect, useRef, useState } from "react";

import { createPluginUI } from "molstar/lib/mol-plugin-ui";
import { renderReact18 } from "molstar/lib/mol-plugin-ui/react18";
import { DefaultPluginUISpec } from "molstar/lib/mol-plugin-ui/spec";

import { Script } from "molstar/lib/mol-script/script";
import { StructureSelection } from "molstar/lib/mol-model/structure/query";

import "molstar/lib/mol-plugin-ui/skin/light.scss";


function ProteinViewer({
  structureUrl,
  mutationPosition,
}) {
  const viewerRef = useRef(null);
  const pluginRef = useRef(null);

  const [structureReady, setStructureReady] = useState(false);


  // --------------------------------------------------
  // 1. Initialize Mol* and load the structure
  // --------------------------------------------------
  useEffect(() => {
    let cancelled = false;

    async function initViewer() {
      if (!viewerRef.current || pluginRef.current) {
        return;
      }

      try {
        const plugin = await createPluginUI({
          target: viewerRef.current,
          render: renderReact18,
          spec: DefaultPluginUISpec(),
        });

        if (cancelled) {
          plugin.dispose();
          return;
        }

        pluginRef.current = plugin;

        if (!structureUrl) {
          return;
        }

        setStructureReady(false);

        const data = await plugin.builders.data.download({
          url: structureUrl,
        });

        const trajectory =
          await plugin.builders.structure.parseTrajectory(
            data,
            "pdb"
          );

        await plugin.builders.structure.hierarchy.applyPreset(
          trajectory,
          "default"
        );

        if (!cancelled) {
          setStructureReady(true);
        }

      } catch (error) {
        console.error(
          "Mol* viewer error:",
          error
        );
      }
    }

    initViewer();

    return () => {
      cancelled = true;

      if (pluginRef.current) {
        pluginRef.current.dispose();
        pluginRef.current = null;
      }
    };
  }, [structureUrl]);


  // --------------------------------------------------
  // 2. Select and focus the mutated residue
  // --------------------------------------------------
  useEffect(() => {

    if (
      !structureReady ||
      !pluginRef.current ||
      !mutationPosition
    ) {
      return;
    }

    try {

      const plugin = pluginRef.current;

      const structure =
        plugin.managers.structure.hierarchy
          .current.structures[0]
          ?.cell.obj?.data;

      if (!structure) {
        console.warn(
          "Mol* structure not available."
        );
        return;
      }

      const position = Number(
        mutationPosition
      );

      // Select the residue using its
      // author residue number.
      const selection =
        Script.getStructureSelection(
          (Q) =>
            Q.struct.generator.atomGroups({
              "residue-test":
                Q.core.rel.eq([
                  Q.struct.atomProperty
                    .macromolecular
                    .auth_seq_id(),
                  position,
                ]),
            }),
          structure
        );

      const loci =
        StructureSelection.toLociWithSourceUnits(
          selection
        );

      if (loci.elements.length === 0) {
        console.warn(
          `Residue ${position} was not found in Mol*.`
        );
        return;
      }

      // Select the residue
      plugin.managers.structure.selection.set(
        loci
      );

      // Show the mutation and its local structural environment
      plugin.managers.structure.focus.setFromLoci(loci);

      // Move the camera to the residue
      plugin.managers.camera.focusLoci(
        loci
      );

      // Highlight the residue
      plugin.managers.interactivity.lociHighlights.highlightOnly({
      loci,
     });

      console.log(
        `Mutation residue ${position} selected.`
      );

    } catch (error) {

      console.error(
        "Mutation highlighting error:",
        error
      );

    }

  }, [
    mutationPosition,
    structureReady,
  ]);


  return (
    <div
      ref={viewerRef}
      style={{
        width: "100%",
        height: "600px",
        position: "relative",
      }}
    />
  );
}


export default ProteinViewer;