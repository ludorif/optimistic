/*
 * Copyright (c) 2025 Ludovic Riffiod
 */

/*
 * Copyright (c) 2025 Ludovic Riffiod
 */

import Globe from "react-globe.gl";
import React, {useState, useEffect} from "react";
import { scaleOrdinal } from 'https://esm.sh/d3-scale';
import bumpImage from '../assets/lunar_bumpmap.jpg';
import backgroundImage from '../assets/night-sky.png';
import moon_landings from '../assets/moon_landings.json';

const colorScale = scaleOrdinal(['orangered', 'mediumblue', 'darkgreen', 'yellow']);

const labelsTopOrientation = new Set(['Apollo 12', 'Luna 2', 'Luna 20', 'Luna 21', 'Luna 24', 'LCROSS Probe']); // avoid label collisions


const Planet = ({surfaceImage}) =>{
    const [landingSites, setLandingSites] = useState([]);

    useEffect(() => {
        fetch({moon_landings})
            .then(r =>r.json())
            .then(setLandingSites);
    }, []);

    return <Globe
        width={400}
        height={400}
        globeImageUrl={surfaceImage}
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

export default Planet;
