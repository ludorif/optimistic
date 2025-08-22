import React, {useEffect, useRef, useState} from "react";
import axios from "axios";
import OpWinnerEvent from "../components/OpWinnerEvent.jsx";
import styles from "../css/mystyle.module.css";
import ExecuteRequest from "../AxiosManager.jsx";
import Grid from "@mui/material/Grid";
import { ArcherContainer, ArcherElement } from 'react-archer';




function WinnersPage () {
    const [allEvents, setAllEvents] = useState([])
    const [winners, setWinners] = useState([])
    const itemsRef = useRef(null);
    let count = 0;

    function UpdateWinners(winnersArray) {
        setWinners(winnersArray);
    }

    function GenerateNewOpEvent(event) {
        const isWinner = winners.find((item) => item._id === event._id) != null;

        //if (isWinner) {
            ++count;
        //}

        return <OpWinnerEvent key={event._id} event={event} isWinner={isWinner} count={count.toString()}></OpWinnerEvent>;

    }

    function GenerateNewLine(lineContent, lineIndex) {
        return <Grid ref={itemsRef} size={4} key={lineIndex} className={styles.customUl}>{lineContent}</Grid>
    }

    function UpdateAllEvents(eventsArray) {
        let localAllEvents = []
        let lineContent = [];
        let date = Date.parse(eventsArray[0].date);
        let lineIndex = 0;

        for (let event of eventsArray) {
            const parsedDate = Date.parse(event.date)
            if (parsedDate > date) {
                localAllEvents.push(GenerateNewLine(lineContent, lineIndex));
                date = parsedDate;
                lineContent = []
                ++lineIndex;
            }

            lineContent.push(GenerateNewOpEvent(event));
        }

        localAllEvents.push(GenerateNewLine(lineContent, lineIndex));
        setAllEvents(localAllEvents)
    }

    useEffect(() => {
        ExecuteRequest(axios.get("winners/"), UpdateWinners);
    }, [])

    useEffect(() => {
        if (winners.length === 0) {
            return;
        }
        ExecuteRequest(axios.get("events/"), UpdateAllEvents);
    }, [winners])


    return (
        <div>
            <ArcherContainer strokeColor="red">
                {allEvents}

                <ArcherElement
                    id="element4"
                    relations={[
                        {
                            targetId: '1',
                            targetAnchor: 'right',
                            sourceAnchor: 'left',
                            label: 'Arrow 3',
                        },
                    ]}
                >
                    <div>Element 4</div>
                </ArcherElement>
            </ArcherContainer>
        </div>

    );
}

export default WinnersPage;