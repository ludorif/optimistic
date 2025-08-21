import React, {useEffect, useState} from "react";
import axios from "axios";
import OpEventToVoteOn from "../components/OpEventToVoteOn.jsx";
import OpWinnerEvent from "../components/OpWinnerEvent.jsx";
import styles from "../css/mystyle.module.css";
import ExecuteRequest from "../AxiosManager.jsx";

function WinnersPage () {
    const [allEvents, setAllEvents] = useState([])
    const [winners, setWinners] = useState([])

    function UpdateWinners(winnersArray) {
        setWinners(winnersArray);
    }

    function GenerateNewOpEvent(event) {
        const isWinner = winners.find((item) => item._id === event._id) != null;

        const style = isWinner ? styles.customDiv : null;

        return <li key={event._id}>
            <OpWinnerEvent key={event._id} title={event.title} content={event.content}
                           photoId={event.photoId} voteCount={event.votes} style={style}>
            </OpWinnerEvent>
        </li>
    }

    function GenerateNewLine(lineContent, lineIndex) {
    return <ul key={lineIndex} className={styles.customUl}>{lineContent}</ul>
    }

    function UpdateAllEvents(eventsArray) {
        let localAllEvents = []
        let lineContent = [];
        let date = Date.parse(eventsArray[0].date);
        let lineIndex = 0;

        for (let event of eventsArray) {
            const parsedDate = Date.parse(event.date)
            if (parsedDate > date)
            {
                localAllEvents.push(GenerateNewLine(lineContent, lineIndex));
                date = parsedDate;
                lineContent = []
                ++ lineIndex;
            }

            lineContent.push(GenerateNewOpEvent(event));
        }

        localAllEvents.push(GenerateNewLine(lineContent, lineIndex));
        setAllEvents(localAllEvents)
    }

    useEffect(()=>{
        ExecuteRequest(axios.get("winners/"), UpdateWinners);
    },[])

    useEffect(() => {
        if(winners.length === 0){
            return;
        }
        ExecuteRequest(axios.get("events/"), UpdateAllEvents);
        }, [winners])


    return (
        <div >
            {allEvents}
        </div>
    );
}

export default WinnersPage;