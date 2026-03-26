//Copyright (c) 2025 Ludovic Riffiod
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./pages/Layout";
import History from "./pages/History";
import HomePage from "./pages/HomePage";
import ToVotePage from "./pages/ToVotePage";
import WinnersPage from "./pages/WinnersPage";
import PlanetPage from "./pages/Planets/PlanetPage";
import axios from "axios";
import React from "react";


axios.defaults.baseURL = import.meta.env.VITE_BACKEND_URL;


export default function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Layout />}>
                    <Route index element={<HomePage />} />
                    <Route path="history" element={<History />} />
                    <Route path="vote" element={<ToVotePage />} />
                    <Route path="winners" element={<WinnersPage />} />
                    <Route path="planet" element={<PlanetPage />} />
                </Route>
            </Routes>
        </BrowserRouter>
    );
}

const rootElement = document.getElementById("root");

if (!rootElement) {
    throw new Error("Root element not found");
}

const root = ReactDOM.createRoot(rootElement);
root.render(<App />);
