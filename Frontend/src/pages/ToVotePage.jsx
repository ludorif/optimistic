//Copyright (c) 2025 Ludovic Riffiod
import React, {useEffect, useState} from "react";
import axios from "axios";
import OpEventToVoteOn from "../components/OpEventToVoteOn.jsx";
import ExecuteRequest, {GetTodayDateStr} from "../AxiosManager.jsx";
import Grid from "@mui/material/Grid";


const ToVotePage = () => {
    const [eventsToVoteOn, setEventsToVoteOn] = useState(null)
    const [toRefresh, setToRefresh] = useState(0);
    const [newEventText, setNewEventText] = useState("");

    useEffect(() => {
        ExecuteRequest(axios.get(`events/?date=${GetTodayDateStr()}`), UpdateEventsToVoteOn)
    }, [toRefresh]);

    function ForceRefresh() {
        setToRefresh(toRefresh + 1)
    }

    function VoteFor(eventId) {
        ExecuteRequest(axios.put('events/', {event_id: eventId}), ForceRefresh);
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
        ExecuteRequest(axios.post('events/', {story: newEventText.target.value, event_date:GetTodayDateStr() }), ForceRefresh)
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

        {GetProposeNewEventButtonOrError()}
        <Grid container spacing={10} justifyContent="center" alignItems="center"   >{eventsToVoteOn}</Grid>
    </div>;
};

export default ToVotePage;