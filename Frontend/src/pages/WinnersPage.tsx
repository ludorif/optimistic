import React, { useEffect, useMemo, useState } from "react";
import axios from "axios";
import {
    ReactFlow,
    Background,
    Controls,
    type Edge,
    type Node,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import WinnerFlowNode, { type WinnerFlowNodeData } from "../components/WinnerFlowNode";
import ExecuteRequest from "../AxiosManager.jsx";
//Copyright (c) 2025 Ludovic Riffiod
import titleStyle from "../Helper.jsx";
import { useNavigate } from "react-router-dom";

const NODE_W = 750;
const NODE_H = 750;
const DAY_GAP = 500;
const COLS = 3;

const winnerNodeTypes = { winnerEvent: WinnerFlowNode };

function nodeIdForEvent(event: OEvent & { _id?: string }) {
    return event._id != null ? `e-${event._id}` : `e-${event.id}`;
}

function buildWinnerFlow(
    eventsArray: OEvent[],
    winners: OEvent[],
): { nodes: Node<WinnerFlowNodeData>[]; edges: Edge[] }
{
    const nodes: Node<WinnerFlowNodeData>[] = [];
    const winnerIdsOrdered: string[] = [];

    if (eventsArray.length === 0) {
        return { nodes, edges: [] };
    }

    const winnerSet = (e: OEvent) => winners.some((w) => w.id === e.id);

    let date = Date.parse(eventsArray[0].created_at);
    let globalY = 0;
    let currentLine: OEvent[] = [];

    const flushLine = () => {
        if (currentLine.length === 0) return;
        currentLine.forEach((event, idx) => {
            const col = idx % COLS;
            const rowInLine = Math.floor(idx / COLS);
            const isWinner = winnerSet(event);
            const id = nodeIdForEvent(event);
            nodes.push({
                id,
                type: "winnerEvent",
                position: { x: col * NODE_W, y: globalY + rowInLine * NODE_H },
                data: { event, isWinner },
                draggable: false,
            });
            if (isWinner) {
                winnerIdsOrdered.push(id);
            }
        });
        const rows = Math.ceil(currentLine.length / COLS);
        globalY += rows * NODE_H + DAY_GAP;
        currentLine = [];
    };

    for (const event of eventsArray) {
        const parsedDate = Date.parse(event.created_at);
        if (parsedDate > date) {
            flushLine();
            date = parsedDate;
        }
        currentLine.push(event);
    }
    flushLine();

    const edges: Edge[] = [];
    for (let i = 0; i < winnerIdsOrdered.length - 1; i++) {
        edges.push({
            id: `winner-chain-${winnerIdsOrdered[i]}-${winnerIdsOrdered[i + 1]}`,
            source: winnerIdsOrdered[i],
            sourceHandle: "bottom",
            target: winnerIdsOrdered[i + 1],
            targetHandle: "top",
            style: { stroke: "#888", strokeDasharray: "5 5" },
            type: "smoothstep",
        });
    }

    return { nodes, edges };
}

function WinnersPage() {
    const [events, setEvents] = useState<OEvent[]>([]);
    const [winners, setWinners] = useState<OEvent[]>([]);
    const navigate = useNavigate();
    const planetId = localStorage.getItem("planetId");

    if (planetId == null) {
        navigate("/Planet");
    }

    function UpdateWinners(winnersArray: OEvent[]) {
        setWinners(winnersArray);
    }

    function UpdateEvents(eventsArray: OEvent[]) {
        setEvents(eventsArray);
    }

    useEffect(() => {
        ExecuteRequest(axios.get("winners/"), UpdateWinners);
    }, []);

    useEffect(() => {
        if (winners.length === 0) {
            return;
        }
        ExecuteRequest(
            axios.get(`events/?planet_id=${localStorage.getItem("planetId")}`),
            UpdateEvents,
        );
    }, [winners]);

    const { nodes, edges } = useMemo(
        () => buildWinnerFlow(events, winners),
        [events, winners],
    );

    return (
        <div style={{ width: "100%", height: "calc(100vh - 120px)", minHeight: 480 }}>
            <h1 style={titleStyle}>Events that won:</h1>
            <div style={{ width: "100%", height: "calc(100% - 48px)" }}>
                <ReactFlow
                    nodes={nodes}
                    edges={edges}
                    nodeTypes={winnerNodeTypes}
                    fitView = {true}
                    fitViewOptions={{ padding: 0.15 }}
                    nodesDraggable={false}
                    nodesConnectable={false}
                    elementsSelectable={false}
                    panOnDrag={false}
                    panOnScroll={true}
                    zoomOnScroll={false}
                    zoomOnPinch={false}
                    zoomOnDoubleClick={false}
                >

                </ReactFlow>
            </div>
        </div>
    );
}

export default WinnersPage;
