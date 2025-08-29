//Copyright (c) 2025 Ludovic Riffiod
import React from "react";
import styled from "styled-components";
import Grid from "@mui/material/Grid";

const Image = styled.img`
    width: 300px;
    height: 300px;
    border-radius: 50%;
    overflow: hidden;
`;


export default function  OpEvent ({event}) {
    return (
        <>
            <div style={{ height:200}}>
                <h2>{event.title}</h2>
                <p>{event.content} </p>
            </div>
            <Image src={`https://images.pexels.com/photos/${event.photoId}/pexels-photo-${event.photoId}.jpeg`}/>
        </>
    )
}