//Copyright (c) 2025 Ludovic Riffiod
import { Handle, Position, type NodeProps } from "@xyflow/react";
import OpWinnerEvent from "./OpWinnerEvent.jsx";
import React from "react";

export type WinnerFlowNodeData = {
    event: OEvent;
    isWinner: boolean;
};

export default function WinnerFlowNode({ data }: NodeProps<WinnerFlowNodeData>) {
    return (
        <div style={{ width: 750 }}>
            {data.isWinner ? (
                <>
                    <Handle type="target" position={Position.Top} id="top" />
                    <OpWinnerEvent event={data.event} isWinner />
                    <Handle type="source" position={Position.Bottom} id="bottom" />
                </>
            ) : (
                <OpWinnerEvent event={data.event} isWinner={false} />
            )}
        </div>
    );
}
