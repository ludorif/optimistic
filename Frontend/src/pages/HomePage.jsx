import React from 'react'
import '../App.css'
import {ArcherContainer, ArcherElement} from "react-archer";

const HomePage = () => {

    return (
        <div>

            <ArcherContainer strokeColor="red">
                <ArcherElement id="root">
                    <p> List of worlds swipe</p>
                </ArcherElement>
                <br/>
                <ArcherElement
                    id="element4"
                    relations={[
                        {
                            targetId: 'root',
                            targetAnchor: 'right',
                            sourceAnchor: 'left',
                            label: 'Arrow 3',
                        },
                    ]}
                >
                    <div>Element 4</div>
                </ArcherElement>
            </ArcherContainer>
        </div>);
}


export default HomePage
