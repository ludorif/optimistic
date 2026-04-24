/*
 * Copyright (c) 2025 Ludovic Riffiod
 */


import React from "react";
import styled from "styled-components";
import OpWinnerEvent from "./OpWinnerEvent";

const DateSection = styled.div`
    margin-bottom: 40px;
`;

const DateLabel = styled.h3`
    color: #aaa;
    margin-bottom: 12px;
`;

const EventGrid = styled.div`
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
`;

export function DateGroup({
                       date,
                       events,
                       winnerIds,
                       setWinnerRef,
                   }: {
    date: string;
    events: OEvent[];
    winnerIds: Set<string>;
    setWinnerRef: (id: string) => (el: HTMLDivElement | null) => void;
}) {
    return (
        <DateSection>
            <DateLabel>{date}</DateLabel>
            <EventGrid>
                {events.map((event) => {
                    const isWinner = winnerIds.has(String(event.id));
                    return isWinner ? (
                        <div key={event.id} ref={setWinnerRef(String(event.id))}>
                            <OpWinnerEvent event={event} isWinner />
                        </div>
                    ) : (
                        <OpWinnerEvent key={event.id} event={event} isWinner={false} />
                    );
                })}
            </EventGrid>
        </DateSection>
    );
}
