/*
 * Copyright (c) 2025 Ludovic Riffiod
 */

import React from "react";
import styled from "styled-components";

export type ArrowLine = { x1: number; y1: number; x2: number; y2: number };

const ArrowSvg = styled.svg`
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    overflow: visible;
    z-index: 1;
`;

export function ArrowOverlay({ arrows }: { arrows: ArrowLine[] }) {
    return (
        <ArrowSvg>
            <defs>
                <marker id="arrowhead" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
                    <polygon points="0 0, 8 3, 0 6" fill="#888" />
                </marker>
            </defs>
            {arrows.map((a, i) => {
                const cy = Math.max(Math.abs(a.y2 - a.y1) * 0.5, 80);
                const d = `M ${a.x1} ${a.y1} C ${a.x1} ${a.y1 + cy}, ${a.x2} ${a.y2 - cy}, ${a.x2} ${a.y2}`;
                return (
                    <path
                        key={i}
                        d={d}
                        fill="none"
                        stroke="#888"
                        strokeWidth="2"
                        strokeDasharray="6 4"
                    />
                );
            })}
        </ArrowSvg>
    );
}
