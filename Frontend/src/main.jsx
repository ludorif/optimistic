//Copyright (c) 2025 Ludovic Riffiod
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./pages/Layout";
import History from "./pages/History";
import HomePage from "./pages/HomePage";
import ToVotePage from "./pages/ToVotePage";
import WinnersPage from "./pages/WinnersPage.jsx";
import PlanetPage from "./pages/PlanetPage";
import axios from "axios";
import SummaryPage from "./pages/SummaryPage.jsx";

axios.defaults.baseURL = 'http://127.0.0.1:5001';

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
                    <Route path="summary" element={<SummaryPage />} />
                </Route>
            </Routes>
        </BrowserRouter>
    );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
