//Copyright (c) 2025 Ludovic Riffiod
import React from "react";
import OpEvent from "./OpEvent.jsx";
import ArcherElement from '../LocalPackage/react-archer-feature-react-19-migration/src/ArcherElement/ArcherElement';

export default function  OpWinnerEvent ({event,  count, isWinner}) {
    let element = <div>
        <OpEvent event={event}>
        </OpEvent>
    </div>

    if (isWinner) {
        const nextWinner = (count + 1);
        console.log(nextWinner);
        return (
            <ArcherElement id={count.toString()}
                           relations={[
                               {
                                   targetId: nextWinner,
                                   targetAnchor: 'middle',
                                   sourceAnchor: 'middle',
                               },
                           ]}>
                {element}
            </ArcherElement>
        );
    }

    return element;
}
