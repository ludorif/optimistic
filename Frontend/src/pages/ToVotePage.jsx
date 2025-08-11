import HistoryPart from "../components/HistoryPart.jsx";
import React, {useEffect, useState} from "react";
import axios from "axios";
import EventToVote from "../components/EventToVote.jsx";
import styles from '../css/mystyle.module.css'



const ToVotePage = () => {
    const [renderAnimals, setState] = useState(null)
    const [toRefresh, setToRefresh] = useState(0);


    function Test(id){
        console.log(id)
        axios.post('http://127.0.0.1:5000/increase_vote', {event_id:id}).then(
            () => setToRefresh(toRefresh + 1)
        ).catch(
            error => {console.error('There was an error!', error);}
        )
    }

    useEffect(() => {
        axios.get(' http://127.0.0.1:5000/to_vote')
            .then(response => {
                const obj = JSON.parse(response.data);

                const lines = []
                obj.forEach(
                    item => {
                        lines.push(item)
                    }
                )

                const renderAnimals = lines.map(item => (
                    <EventToVote key={item._id} title={item.title} content={item.content}
                                 photoId={item.photoId} voteCount={item.votes}
                                 onclickFunction={() => Test(item._id)}
                    ></EventToVote>));
                setState(renderAnimals)


            })
            .catch(error => {
                console.error('There was an error!', error);
            });
    }, [toRefresh]);

    return <div >
        <ul className={styles.customUl}>{renderAnimals}</ul>
        ;
    </div>;
};

export default ToVotePage;