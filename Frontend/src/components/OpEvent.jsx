//Copyright (c) 2025 Ludovic Riffiod
import React from "react";
import styled from "styled-components";
import Grid from "@mui/material/Grid";

const Image = styled.img`
    width: 75%;          /* Takes full width of parent */
    aspect-ratio: 1 / 1;  /* Keeps it square */
    border-radius: 50%;   /* Circle shape */
    object-fit: cover;
`;



const Title = styled.h2`
    
    font-size: clamp(1rem, 2vw, 3rem);
    background: linear-gradient(90deg, #000000, #0000ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    height: 25px;

    border-top: 2px solid #333;
    border-bottom: 2px solid #333;
    padding: 10px 0;
    margin: 20px 0;
`;

const Content = styled.p`
    font-size: clamp(0.1rem, 1.5vw, 1rem);
    animation: fadeIn 2s ease-in-out;
    height: 100px;
`;


export default function  OpEvent ({event}) {
    return (
        <div className="newspaper" >
            <div >
                <Title>{event.title}</Title>
                <Content>{event.content} </Content>
            </div>
            <Image src={`https://images.pexels.com/photos/${event.photoId}/pexels-photo-${event.photoId}.jpeg`}/>
        </div>
    )
}