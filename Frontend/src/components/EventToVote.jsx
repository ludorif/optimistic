import React from "react";


export default function  EventToVote ({title, content, photoId, voteCount, onclickFunction}) {


    return (
        <button onClick={onclickFunction}>
            <h2>{title}</h2>
            <p>{content} </p>
            <img width={500} height={500} src={`https://images.pexels.com/photos/${photoId}/pexels-photo-${photoId}.jpeg`}/>
            <p>voteCount: {voteCount} </p>
        </button>
    );
}