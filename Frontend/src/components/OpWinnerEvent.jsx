import React from "react";
import OpEvent from "./OpEvent.jsx";
import Grid from "@mui/material/Grid";
import {ArcherElement} from "react-archer";

export default function  OpWinnerEvent ({event, isWinner, count}) {
    if (isWinner) {
        console.log(count);
        return (
            <div >
            <ArcherElement id={count}>
                    <OpEvent event={event}>
                    </OpEvent>
            </ArcherElement>
            </div>
        );
    } else {

        return (
                <div >
                    <ArcherElement id={count}>
                    <OpEvent event={event}>
                    </OpEvent>
                    </ArcherElement>
                </div>
        );
    }
}