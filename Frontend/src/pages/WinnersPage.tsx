//Copyright (c) 2025 Ludovic Riffiod
import React, { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from "react";
import axios from "axios";
import styled from "styled-components";
import OpWinnerEvent from "../components/OpWinnerEvent";
import ExecuteRequest from "../AxiosManager.jsx";
import titleStyle from "../Helper.jsx";
import { useNavigate } from "react-router-dom";
import { ArrowLine, ArrowOverlay } from "../components/ArrowOverlay.jsx";
import {DateGroup} from "../components/DateGroup";


const PageWrapper = styled.div`
    width: 100%;
    padding: 0 16px;
    box-sizing: border-box;
`;

const GridContainer = styled.div`
    position: relative;
`;


function groupEventsByDate(events: OEvent[]): { date: string; events: OEvent[] }[] {
    const groups: { date: string; events: OEvent[] }[] = [];
    let currentDate = "";
    let currentGroup: OEvent[] = [];
    for (const event of events) {
        const date = event.created_at.slice(0, 10);
        if (date !== currentDate) {
            if (currentGroup.length > 0) groups.push({ date: currentDate, events: currentGroup });
            currentDate = date;
            currentGroup = [];
        }
        currentGroup.push(event);
    }
    if (currentGroup.length > 0) groups.push({ date: currentDate, events: currentGroup });
    return groups;
}


function WinnersPage() {
    const [events, setEvents] = useState<OEvent[]>([]);
    const [winners, setWinners] = useState<OEvent[]>([]);
    const [arrows, setArrows] = useState<ArrowLine[]>([]);
    const navigate = useNavigate();

    const gridRef = useRef<HTMLDivElement>(null);
    const winnerCardRefs = useRef<Map<string, HTMLDivElement>>(new Map());

    const setWinnerRef = useCallback((id: string) => (el: HTMLDivElement | null) => {
        if (el) winnerCardRefs.current.set(id, el);
        else winnerCardRefs.current.delete(id);
    }, []);

    const computeArrows = useCallback(() => {
        if (!gridRef.current || winners.length < 2) {
            setArrows([]);
            return;
        }
        const lines: ArrowLine[] = [];
        for (let i = 0; i < winners.length - 1; i++) {
            const a = winnerCardRefs.current.get(String(winners[i].id));
            const b = winnerCardRefs.current.get(String(winners[i + 1].id));
            if (!a || !b) continue;
            lines.push({
                x1: a.offsetLeft + a.offsetWidth / 2,
                y1: a.offsetTop + a.offsetHeight,
                x2: b.offsetLeft + b.offsetWidth / 2,
                y2: b.offsetTop,
            });
        }
        setArrows(lines);
    }, [winners]);

    useLayoutEffect(() => {
        computeArrows();
    }, [computeArrows, events]);

    useEffect(() => {
        if (!gridRef.current) return;
        const ro = new ResizeObserver(computeArrows);
        ro.observe(gridRef.current);
        return () => ro.disconnect();
    }, [computeArrows]);

    useEffect(() => {
        const planetId = localStorage.getItem("planetId");
        if (!planetId || planetId === "undefined") {
            navigate("/Planet");
            return;
        }
        ExecuteRequest(axios.get("winners/"), setWinners);
    }, []);

    useEffect(() => {
        if (winners.length === 0) return;
        ExecuteRequest(
            axios.get(`events/?planet_id=${localStorage.getItem("planetId")}`),
            setEvents,
        );
    }, [winners]);

    const winnerIds = useMemo(() => new Set(winners.map((w) => String(w.id))), [winners]);
    const groups = useMemo(() => groupEventsByDate(events), [events]);

    return (
        <PageWrapper>
            <h1 style={titleStyle}>Events that won:</h1>
            <GridContainer ref={gridRef}>
                <ArrowOverlay arrows={arrows} />
                {groups.map((group) => (
                    <DateGroup
                        key={group.date}
                        date={group.date}
                        events={group.events}
                        winnerIds={winnerIds}
                        setWinnerRef={setWinnerRef}
                    />
                ))}
            </GridContainer>
        </PageWrapper>
    );
}

export default WinnersPage;
