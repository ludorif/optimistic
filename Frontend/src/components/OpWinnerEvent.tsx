//Copyright (c) 2025 Ludovic Riffiod
import React from "react";
import OpEvent from "./OpEvent.jsx";
import ExecuteRequest from "../AxiosManager.jsx";
import axios from "axios";

var globalVar = "";


function PlayAudio(audioUrl: { path: string | undefined; }){
    const audio = new Audio(audioUrl.path);
    audio.onended = () => {globalVar = ""};
    audio.play().catch(err => console.log("Playback error:", err));
}

function RequestVoiceOver(content: any){
    console.log(globalVar);
    if(globalVar == "true"){
        return;
    }
    globalVar = "true";

    ExecuteRequest(axios.get(`voiceOver/?content="${content}"`), PlayAudio);
}

export default function OpWinnerEvent({ event, isWinner }) {
    return (
        <div style={{ border: isWinner ? "2px solid #666" : "1px solid gray" }}>
            <OpEvent event={event} />
            <button onClick={() => RequestVoiceOver(event.content)}> Voice over </button>
        </div>
    );
}
