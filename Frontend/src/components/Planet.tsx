/*
 * Copyright (c) 2025 Ludovic Riffiod
 */

/*
 * Copyright (c) 2025 Ludovic Riffiod
 */

import Globe from "react-globe.gl";
import React from "react";
import bumpImage from '../assets/lunar_bumpmap.jpg';
import backgroundImage from '../assets/night-sky.png';
import Grid from "@mui/material/Grid";
import {ToggleButton} from "@mui/material";
import Button from "@mui/material/Button";
import {useNavigate} from 'react-router-dom'; // Import useNavigate hook
import mars_surface from "../assets/mars_surface.png";
import lunar_surface from '../assets/lunar_surface.jpg';
import earth_surface from '../assets/earth_surface.jpg';


const Planet = ({surfaceImage}) =>{
    return <Globe
        width={300}
        height={300}
        globeImageUrl={surfaceImage}
        bumpImageUrl={bumpImage}
        backgroundImageUrl={backgroundImage}
        showGraticules={false}
    />;
}

function GetSurfaceImage(PlanetType:string) {
    return PlanetType === "moon" ? lunar_surface : PlanetType === "earth" ? earth_surface : mars_surface;
}

export const TypedPlanet = ({planetType}) =>{
    return <Planet surfaceImage={GetSurfaceImage(planetType)} />
}


export const ToggablePlanet = ({value, planetType}) =>{
    return <>
        <ToggleButton value={value} >
            <Planet surfaceImage={GetSurfaceImage(planetType)} />
        </ToggleButton>
    </>
}

export const ClickablePlanet = ({ planetName, planetType, planetId}) =>{
    const navigate = useNavigate();

    function ChoosePlanet() {
        console.log(planetId);
        localStorage.setItem("planetName", planetName)
        localStorage.setItem("planetType", planetType)
        localStorage.setItem("planetId", planetId);
        navigate('/history')
    }


    return <>

        <Grid >
            <p>{planetName}</p>
            <Planet surfaceImage={GetSurfaceImage(planetType)} />
            <Button variant="outlined" onClick={ChoosePlanet}> Select </Button>
        </Grid>

    </>
}

