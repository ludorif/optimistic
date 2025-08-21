import React, {useEffect, useState} from "react";
import axios from "axios";
import OpEventToVoteOn from "../components/OpEventToVoteOn.jsx";
import styles from '../css/mystyle.module.css'
import ExecuteRequest, {GetTodayDateStr} from "../AxiosManager.jsx";



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
            <OpEventToVoteOn key={item._id} title={item.title} content={item.content}
                             photoId={item.photoId} voteCount={item.votes}
                             onclickFunction={() => VoteFor(item._id)}
            ></OpEventToVoteOn>));
        setEventsToVoteOn(eventsMap)
    }

    function OnTextChanged(newEventText) {
        setNewEventText(newEventText);
    }

    function OnSubmitPressed() {
        ExecuteRequest(axios.post('events/?story=' + newEventText), ForceRefresh)
    }


    return <div>
        <ul >{eventsToVoteOn}</ul>
        <input onChange={OnTextChanged}/>
        <button onClick={OnSubmitPressed}>Propose new event</button>
    </div>;
};

export default ToVotePage;