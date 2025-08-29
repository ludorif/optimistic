//Copyright (c) 2025 Ludovic Riffiod
import React from "react";
import OpEvent from "./OpEvent.jsx";
import Grid from "@mui/material/Grid";

export default function  OpEventToVoteOn ({event, onclickFunction}) {

    return (
        <Grid  size={4}   >
            <button onClick={onclickFunction} >
                <p>voteCount: {event.votes} </p>
                <OpEvent event={event} />
            </button>
        </Grid>
    );
}