/*
 * Copyright (c) 2025 Ludovic Riffiod
 */

import Globe from "react-globe.gl";
import React, {useState, useEffect} from "react";
import { scaleOrdinal } from 'https://esm.sh/d3-scale';
import lunar_surface from '../assets/lunar_surface.jpg';
import bumpImage from '../assets/lunar_bumpmap.jpg';
import backgroundImage from '../assets/night-sky.png';

const colorScale = scaleOrdinal(['orangered', 'mediumblue', 'darkgreen', 'yellow']);

const labelsTopOrientation = new Set(['Apollo 12', 'Luna 2', 'Luna 20', 'Luna 21', 'Luna 24', 'LCROSS Probe']); // avoid label collisions


const PlanetPage = () =>{
    const [landingSites, setLandingSites] = useState([]);

    useEffect(() => {
        fetch('../assets/moon_landings.json')
            .then(r =>r.json())
            .then(setLandingSites);
    }, []);
    return <Globe
        globeImageUrl={lunar_surface}
        bumpImageUrl={bumpImage}
        backgroundImageUrl={backgroundImage}
        showGraticules={true}
        labelsData={landingSites}
        labelText="label"
        labelSize={1.7}
        labelDotRadius={0.4}
        labelDotOrientation={d => labelsTopOrientation.has(d.label) ? 'top' : 'bottom'}
        labelColor={d => colorScale(d.agency)}
        labelLabel={d => <div>
            <div><b>{d.label}</b></div>
            <div>{d.agency} - {d.program} Program</div>
            <div>Landing on <i>{new Date(d.date).toLocaleDateString()}</i></div>
        </div>}
        onLabelClick={d => window.open(d.url, '_blank')}
    />;
}

export default PlanetPage;
