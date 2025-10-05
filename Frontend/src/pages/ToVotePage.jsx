//Copyright (c) 2025 Ludovic Riffiod
import React, {useEffect, useState} from "react";
import axios from "axios";
import OpEventToVoteOn from "../components/OpEventToVoteOn.jsx";
import ExecuteRequest, {GetTodayDateStr} from "../AxiosManager.jsx";
import Grid from "@mui/material/Grid";
import titleStyle from "../Helper.jsx";


const ToVotePage = () => {
    const [eventsToVoteOn, setEventsToVoteOn] = useState(null)
    const [toRefresh, setToRefresh] = useState(0);
    const [newEventText, setNewEventText] = useState("");
    const [errorMessage, setErrorMessage] = useState("");

    useEffect(() => {
        const uuid = localStorage.getItem('UUID');
        if(uuid == null) {
            localStorage.setItem('UUID', crypto.randomUUID());
        }

        ExecuteRequest(axios.get(`events/?date=${GetTodayDateStr()}`), UpdateEventsToVoteOn)
    }, [toRefresh]);

    function ForceRefresh(error) {
        setToRefresh(toRefresh + 1)
        setErrorMessage(error == null ? "" :error.response.data.message)
    }

    function VoteFor(eventId) {
        ExecuteRequest(axios.put('events/', {event_id: eventId, uuid: localStorage.getItem('UUID')}), ForceRefresh);
    }

    function UpdateEventsToVoteOn(eventsArray) {
        const eventsMap = eventsArray.map(item => (
                <OpEventToVoteOn
                    key={item._id}
                    event = {item}
                    onclickFunction={() => VoteFor(item._id)}>
                </OpEventToVoteOn>
            ));

        setEventsToVoteOn(eventsMap)
    }

    function OnTextChanged(newEventText) {
        setNewEventText(newEventText);
    }

    function OnSubmitPressed() {
        ExecuteRequest(axios.post('events/', {story: newEventText.target.value, event_date:GetTodayDateStr(), uuid: localStorage.getItem('UUID') }), ForceRefresh)
    }

    const GetProposeNewEventButtonOrError = () => {

        const enoughEvents = eventsToVoteOn != null && eventsToVoteOn.length >= 3;

        return enoughEvents ?
            <p style={{color: "red"}}> Max events for today</p> :
            <>
                <input onChange={OnTextChanged}/>
                <button onClick={OnSubmitPressed}>Propose new event</button>
            </>
    }


    return <div>
        <h1 style={titleStyle}>Vote or create a new event:</h1>

        <p style={{color: "red"}}> {errorMessage}</p>
        {GetProposeNewEventButtonOrError()}
        <Grid container spacing={10} justifyContent="center" alignItems="center"   >{eventsToVoteOn}</Grid>
    </div>;
};

export default ToVotePage;
