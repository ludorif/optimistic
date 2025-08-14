import HistoryPart from "../components/HistoryPart.jsx";
import React, {useEffect, useState} from "react";
import axios from "axios";



const History = () => {
    const [dates, setDates] = useState(null)
    const [historyPerDate, setHistoryPerDate] = useState(null)
    const [currentSelectedDate, setCurrentSelectedDate] = useState(null)

    useEffect(
        ()=>{
            axios.get('get_dates')
                .then(response => {

                    const obj = JSON.parse(response.data);

                    const localDates =[]
                    obj.forEach(
                        item => {
                            console.log(item);
                            localDates.push(item)

                        }
                    )


                    const localDatesMap = localDates.map(item => (
                        <option key={self.crypto.randomUUID()} value={item}>{item}</option>));
                    setDates(localDatesMap)


                })
                .catch(error => {
                    console.error('There was an error!', error);
                });
        }, []
    )

    const handleHistory = () => {

        axios.get(`history/${currentSelectedDate}`)
            .then(response => {
                const obj = JSON.parse(response.data);
                console.log(obj[0].photoId);

                const lines =[]
                obj.forEach(
                    item => {
                        lines.push(item)
                    }
                )

                const historyPerDate = lines.map(item => (
                    <HistoryPart key={item._id} title={item.title} content={item.content} photoId={item.photoId}></HistoryPart>));
                setHistoryPerDate(historyPerDate)



            })
            .catch(error => {
                console.error('There was an error!', error);
            });

    }

    function DefineWinner() {
        axios.get(`define_winner/${currentSelectedDate}`)
            .then(response => {
                console.log(response.data);
            })
            .catch(error => {
                console.error('There was an error!', error);
            });
    }

    function dateChanged(newDate) {
        setCurrentSelectedDate(newDate.target.value);
        handleHistory();
    }

    return <div>
        <button onClick={handleHistory}>History</button>
        <button onClick={DefineWinner}> DefineWinner</button>
        <br/>
        <select name="dateSelector" id="dateSelector" onChange={dateChanged}>
            {dates}
        </select>
        <ul>{historyPerDate}</ul>;
    </div>;
};

export default History;