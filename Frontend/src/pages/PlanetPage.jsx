/*
 * Copyright (c) 2025 Ludovic Riffiod
 */


import Planet from "../components/Planet.jsx";
import Grid from "@mui/material/Grid";
import mars_surface from '../assets/mars_surface.png';
import lunar_surface from '../assets/lunar_surface.jpg';
import earth_surface from '../assets/earth_surface.jpg';
import titleStyle from "../Helper.jsx";
import React from "react";

const PlanetPage = () =>{

    return <>
    <h1 style={titleStyle}>Change your planet (WIP)</h1>
    <Grid container  justifyContent="center" alignItems="center" size={20} >
        <Grid size={4} >
        <Planet surfaceImage = {mars_surface}></Planet>
        </Grid>
        <Grid size={4} >
        <Planet surfaceImage = {lunar_surface}></Planet>
        </Grid>
        <Grid size={4} >
        <Planet surfaceImage = {earth_surface}></Planet>
        </Grid>
    </Grid>
    </>
}

export default PlanetPage;
