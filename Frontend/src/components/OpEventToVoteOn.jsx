import React from "react";
import OpEvent from "./OpEvent.jsx";

export default function  OpEventToVoteOn ({title, content, photoId, voteCount, onclickFunction}) {

    return (
        <button onClick={onclickFunction}>
            <OpEvent title = {title} content = {content} photoId = {photoId}>
            </OpEvent>
            <p>voteCount: {voteCount} </p>
        </button>
    );
}