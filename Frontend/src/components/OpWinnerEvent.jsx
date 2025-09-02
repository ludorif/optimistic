//Copyright (c) 2025 Ludovic Riffiod
import React from "react";
import OpEvent from "./OpEvent.jsx";
import ArcherElement from '../LocalPackage/react-archer-feature-react-19-migration/src/ArcherElement/ArcherElement';

export default function  OpWinnerEvent ({event,  count, isWinner}) {
    let element = <div style={{ border: '1px solid gray'}}>
        <OpEvent  event={event}>
        </OpEvent>
    </div>

    if (isWinner) {
        const nextWinner = (count + 1);
        return (
            <ArcherElement   id={count.toString()}
                           relations={[
                               {
                                   targetId: nextWinner,
                                   targetAnchor: 'top',
                                   sourceAnchor: 'bottom',
                                   style: { strokeDasharray: '5,5', lineStyle: 'curve' }
                               },
                           ]}>
                {element}
            </ArcherElement>
        );
    }

    return element;
}
