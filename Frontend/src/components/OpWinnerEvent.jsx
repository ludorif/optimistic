import React from "react";
import OpEvent from "./OpEvent.jsx";

export default function  OpWinnerEvent ({title, content, photoId, style}) {
    return (
        <div  className={style}>
            <OpEvent title = {title} content = {content} photoId = {photoId}>
            </OpEvent>
        </div>
    );
}