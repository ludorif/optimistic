//Copyright (c) 2025 Ludovic Riffiod
import React from "react";
import OpEvent from "./OpEvent.jsx";
import ArcherElement from '../LocalPackage/react-archer-feature-react-19-migration/src/ArcherElement/ArcherElement';
import ExecuteRequest from "../AxiosManager.jsx";
import axios from "axios";

var globalVar = "";


function PlayAudio(audioUrl){
    const audio = new Audio(audioUrl.path);
    audio.onended = () => {globalVar = ""};
    audio.play().catch(err => console.log("Playback error:", err));
}

function RequestVoiceOver(content){
    console.log(globalVar);
    if(globalVar == "true"){
        return;
    }
    globalVar = "true";

    ExecuteRequest(axios.get(`voiceOver/?content="${content}"`), PlayAudio);
}

export default function  OpWinnerEvent ({event,  count, isWinner}) {
    let element = <div style={{ border: '1px solid gray'}}>
        <OpEvent  event={event}>
        </OpEvent>
        <button onClick={()=>{RequestVoiceOver(event.content)}} > Voice over </button>
    </div>

    if (isWinner) {
        const nextWinner = (count + 1);
        return (
            <ArcherElement   id={count.toString()}
                           relations={[
                               {
                                   targetId: nextWinner,
                                   targetAnchor: 'top',
                                   sourceAnchor: 'bottom',
                                   style: { strokeDasharray: '5,5', lineStyle: 'curve' }
                               },
                           ]}>
                {element}

            </ArcherElement>
        );
    }

    return element;
}
