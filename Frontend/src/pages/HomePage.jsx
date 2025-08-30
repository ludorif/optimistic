//Copyright (c) 2025 Ludovic Riffiod
import React from 'react'
import '../css/App.css'

const HomePage = () => {
    return (
        <div className="homepage">
            <header className="header">
                <h1>Optimistic</h1>
                <p>An open-source project designed with several goals in mind:</p>
                <ul>
                    <li>Showcase my full-stack and AI development skills</li>
                    <li>Experiment with and test emerging technologies</li>
                    <li>
                        Build a playful space that envisions an optimistic, climate-positive
                        world
                    </li>
                </ul>
            </header>

            <section className="card">
                <h2>Concept</h2>
                <p>The platform works around the idea of daily optimistic events:</p>
                <ul>
                    <li>Users can submit events</li>
                    <li>The community votes for their favorite event of the day</li>
                    <li>A winner is declared daily</li>
                </ul>
                <p>
                    All events are intentionally uplifting, imaginative, and
                    climate-positive, ensuring a positive and future-focused experience.
                </p>
            </section>

            <section className="card">
                <h2>Tech Stack</h2>
                <ul>
                    <li>
                        <strong>Backend:</strong> Python with FastAPI
                    </li>
                    <li>
                        <strong>Frontend:</strong> React (JavaScript)
                    </li>
                    <li>
                        <strong>AI:</strong> Gemini API to generate events from user stories
                    </li>
                    <li>
                        <strong>Media:</strong> Pexels API for imagery
                    </li>
                    <li>
                        <strong>Database:</strong> MongoDB
                    </li>
                    <li>
                        <strong>Hosting:</strong> Render.com
                    </li>
                </ul>
            </section>

            <section className="card">
                <h2>Roadmap</h2>
                <ul>
                    <li>Deepen AI integrations and experimentation</li>
                    <li>Introduce multiple worlds for diverse optimistic scenarios</li>
                    <li>Enhance the UI/UX design for a more engaging look and feel</li>
                </ul>
            </section>
        </div>
    );
}


export default HomePage
