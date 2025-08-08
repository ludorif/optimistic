import React from "react";



export default function  HistoryPart ({title, content, photoId}) {
    return (
        <div>
            <h2>{title}</h2>
            <p>{content} </p>
            <img width={500} height={500} src={`https://images.pexels.com/photos/${photoId}/pexels-photo-${photoId}.jpeg`}/>
        </div>
    );
}