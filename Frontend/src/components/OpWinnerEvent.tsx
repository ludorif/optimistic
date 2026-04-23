//Copyright (c) 2025 Ludovic Riffiod
import React from "react";
import OpEvent from "./OpEvent.jsx";
import ExecuteRequest from "../AxiosManager.jsx";
import axios from "axios";

let currentAudio: HTMLAudioElement | null = null;

function PlayAudio(audioUrl: { path: string | undefined; }){
    if (currentAudio) {
        currentAudio.pause();
        currentAudio.src = "";
        currentAudio = null;
    }
    const audio = new Audio(audioUrl.path);
    currentAudio = audio;
    audio.onended = () => { currentAudio = null; };
    audio.play().catch(err => console.error("Playback error:", err));
}

function RequestVoiceOver(content: string){
    if (currentAudio && !currentAudio.ended) return;
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
