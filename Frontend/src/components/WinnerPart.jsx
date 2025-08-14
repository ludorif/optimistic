import React from "react";
import styles from "../css/mystyle.module.css";


export default function  WinnerPart ({title, content, photoId, style}) {
    return (
        <div  className={style}>
            <h2>{title}</h2>
            <p>{content} </p>
            <img width={500} height={500} src={`https://images.pexels.com/photos/${photoId}/pexels-photo-${photoId}.jpeg`}/>
        </div>
    );
}