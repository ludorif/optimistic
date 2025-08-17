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
        console.log(winnersArray);
        setWinners(winnersArray);
        ExecuteRequest(axios.get("events/"), UpdateAllEvents);
    }

    function UpdateAllEvents(eventsArray) {
        let localAllEvents = []
        let line =[];
        let date =Date.parse(eventsArray[0].date);

        eventsArray.forEach(
            function(event) {
                if (Date.parse(event.date) > date) {
                    date = Date.parse(event.date);
                    localAllEvents.push(<ul key={self.crypto.randomUUID()} className={styles.customUl}>{line}</ul>);
                    line = []
                }

                const isWinner = winners.find((item) => item._id === event._id);

                const style = isWinner ? styles.customDiv : null;

                line.push(<li key={self.crypto.randomUUID()}><OpWinnerEvent key={event._id} title={event.title} content={event.content}
                                              photoId={event.photoId} voteCount={event.votes} style={style}
                ></OpWinnerEvent></li>);
            });

        localAllEvents.push(<ul className={styles.customUl}>{line}</ul>);
        setAllEvents(localAllEvents)
    }

    useEffect(()=>{
        ExecuteRequest(axios.get("winners/"), UpdateWinners);
    },[])

    return (
        <div key={self.crypto.randomUUID()}>
            {allEvents}
        </div>
    );
}

export default WinnersPage;