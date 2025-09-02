//Copyright (c) 2025 Ludovic Riffiod
export default function ExecuteRequest(promise, ResultFunction) {
    promise
        .then(response => {
            if(ResultFunction === null)
            {
                return;
            }

            if(response.data === null)
            {
                ResultFunction()
                return;
            }

            const resultObject = JSON.parse(response.data);
            const resultArray =[]
            resultObject.forEach(
                item => {
                    resultArray.push(item)
                }
            )
            ResultFunction(resultArray);
        })
        .catch(error => {
            ResultFunction(error);
            console.error('There was an error!', error);
        });
}

export function GetTodayDateStr(){
    const todayDate = new Date()

    //We add 1 since getUTCMonth returns a value between 0 and 11. We use padStart to always have 2 digits: 01,02...
    const month = (todayDate.getUTCMonth()+1).toString().padStart(2, "0");
    const day = todayDate.getUTCDate().toString().padStart(2, "0");

    return todayDate.getUTCFullYear() + '-' + month + '-' + day;
}
