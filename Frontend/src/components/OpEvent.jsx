import React from "react";
import styled from "styled-components";

const Image = styled.img`
    width: 500px;
    height: 500px;
    border-radius: 50%;
    overflow: hidden;
`;


export default function  OpEvent ({title, content, photoId}) {
    return ( 
        <>
        <h2>{title}</h2>
        <p>{content} </p>
        <Image  src={`https://images.pexels.com/photos/${photoId}/pexels-photo-${photoId}.jpeg`}/>
        </>
    )
}