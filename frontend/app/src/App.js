import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Registration from './components/Login/Registration';
import Login from './components/Login/Login';
import KakaoMap from "./components/KakaoMap/Kakao";
import {AuthProvider} from "./AuthContext";

function App() {
  return (
    <Router>
      <div>
          <AuthProvider>
              <Routes>
                  <Route path="/registration" element={<Registration />} />
                  <Route path="/login" element={<Login />} />
                  <Route path="/kakao" element={<KakaoMap />} /> {/* Добавьте маршрут для защищенной страницы */}
              </Routes>
          </AuthProvider>
      </div>
    </Router>
  );
}

export default App;

