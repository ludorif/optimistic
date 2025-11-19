/*
 * Copyright (c) 2025 Ludovic Riffiod
 */

import  {ClickablePlanet} from "../../components/Planet.jsx";
import React, {useEffect} from "react";
import ExecuteRequest from "../../AxiosManager.jsx";
import axios from "axios";
import CreateNewPlanet from "../Planets/NewPlanet";
import ChoosePlanet from "../Planets/ChoosePlanet";
import ChangePlanet from "../Planets/ChangePlanet";

const PlanetPage = () => {

    enum EUserState {
        None,
        PlanetSelected,
        NewPlanet
    }

    const [UserState, SetUserState] = React.useState(EUserState.None);
    const [Planets, setPlanets] : any[] = React.useState([]) ;

    function SwitchToNewPlanet() {
        SetUserState(EUserState.NewPlanet)
    }

    function SwitchToChangePlanet(){
        SetUserState(EUserState.None)
        localStorage.removeItem("planetName")
    }


    function UpdatePlanets(planetsArray: any[]) {
        const planetsMap = planetsArray.map((item) =>
            <ClickablePlanet planetName={item.planet_name} type={item.planet_type}></ClickablePlanet>);
        setPlanets(planetsMap);
    }

    useEffect(()=> {
            ExecuteRequest(axios.get('planets/'), UpdatePlanets);
            const planetName = localStorage.getItem("planetName");
            if (planetName != null) {
                SetUserState(EUserState.PlanetSelected)
            }
        }, []
    )


    switch (UserState) {
        case EUserState.None:
            return <ChoosePlanet OnClickFunction={SwitchToNewPlanet} Planets={Planets}></ChoosePlanet>
        case EUserState.PlanetSelected:
            return <ChangePlanet OnClickFunction={SwitchToChangePlanet}/>
        case EUserState.NewPlanet:
            return <CreateNewPlanet/>
    }
}

export default PlanetPage;
