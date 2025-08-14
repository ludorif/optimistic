import React, {useEffect, useState} from "react";
import axios from "axios";
import EventToVote from "../components/EventToVote.jsx";
import WinnerPart from "../components/WinnerPart.jsx";
import styles from "../css/mystyle.module.css";

function WinnersPage () {

    const [winners, setWinners] = useState([])


    function ChangeStyleForWinner(){

    }

    useEffect(()=>{
        axios.get("history/all_dates").then(response => {
            const obj = JSON.parse(response.data);


            const events =[]
            obj.events.forEach(
                item => {
                    events.push(item)
                }
            )



            let local = []
            let test =[];
            let date =Date.parse(events[0].date);


            events.forEach(function(event) {

                if( Date.parse(event.date) > date){
                    date = Date.parse(event.date);
                    test.push(<ul className={styles.customUl}>{local}</ul>);
                    local = []
                }

                const style =  (obj.winners.find((item) => item._id === event._id)) ? styles.customDiv : null;

                local.push(<li> <WinnerPart key={event._id} title={event.title} content={event.content}
                                       photoId={event.photoId} voteCount={event.votes}  style={style}
                ></WinnerPart></li>);
            });

            test.push(<ul className={styles.customUl}>{local}</ul>);
            setWinners(test)


        }).catch(
            err => {console.log(err)}
        )

    },[])

    return (
        <div>
            {winners}
        </div>
    );
}

export default WinnersPage;