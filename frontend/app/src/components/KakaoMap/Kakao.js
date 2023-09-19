import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../AuthContext";

const Kakao = () => {
  const [sd, setSd] = useState("");
  const [sgg, setSgg] = useState("");
  const [umd, setUmd] = useState("");
  const [results, setResults] = useState([]);
  const [map, setMap] = useState(null);
  const [markers, setMarkers] = useState([]);
  const [showFireStations, setShowFireStations] = useState(false);
  const [showHospitals, setShowHospitals] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedMarker, setSelectedMarker] = useState(null); // Добавляем состояние для выбранной метки

  const navigate = useNavigate();
  const { authenticated } = useAuth();

  useEffect(() => {
    if (!authenticated) {
      navigate("/login");
    }
  }, [authenticated, navigate]);

  // Инициализация карты
  useEffect(() => {
    if (!map) {
      const mapContainer = document.getElementById("map");
      const DEFAULT_LATITUDE = 37.5665;
      const DEFAULT_LONGITUDE = 126.9780;
      const options = {
        center: new window.kakao.maps.LatLng(DEFAULT_LATITUDE, DEFAULT_LONGITUDE),
        level: 10,
      };
      const newMap = new window.kakao.maps.Map(mapContainer, options);
      setMap(newMap);
    }
  }, [map]);

  // Обновление маркеров на карте
  useEffect(() => {
    if (map && results.length > 0) {
      // Удалите существующие маркеры
      markers.forEach((marker) => {
        marker.setMap(null);
      });

      // Создайте новый массив маркеров с обработчиками события клика
      const newMarkers = results.map((address) => {
        const markerPosition = new window.kakao.maps.LatLng(
          parseFloat(address.y),
          parseFloat(address.x)
        );
        const marker = new window.kakao.maps.Marker({
          position: markerPosition,
        });

        // Добавьте обработчик события клика на метку
        window.kakao.maps.event.addListener(marker, "click", () => {
          setSelectedMarker(address);
        });

        marker.setMap(map);
        return marker;
      });

      // Обновите состояние markers
      setMarkers(newMarkers);
    }
  }, [map, results]);

  const handleSearch = async () => {
    try {
      setLoading(true);
      setError(null);

      let endpoint = "";
      if (showFireStations) {
        endpoint = "fire_stations";
      } else if (showHospitals) {
        endpoint = "hospitals";
      }

      const response = await axios.post(
        `http://127.0.0.1:8000/kakao/geolocation/address/${endpoint}`,
        {
          sd,
          sgg,
          umd,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (response.status === 200) {
        const data = response.data;
        setResults(data);
        setSelectedMarker(null); // Сбрасываем выбранную метку при новом поиске
      } else {
        setError("Ошибка при выполнении запроса");
      }
    } catch (error) {
      setError("Ошибка при выполнении запроса");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1 className="mt-4">Search</h1>
      <div className="form-group">
        <label htmlFor="sd">SD:</label>
        <input
          type="text"
          className="form-control"
          id="sd"
          value={sd}
          onChange={(e) => setSd(e.target.value)}
        />
      </div>
      <div className="form-group">
        <label htmlFor="sgg">SGG:</label>
        <input
          type="text"
          className="form-control"
          id="sgg"
          value={sgg}
          onChange={(e) => setSgg(e.target.value)}
        />
      </div>
      <div className="form-group">
        <label htmlFor="umd">UMD:</label>
        <input
          type="text"
          className="form-control"
          id="umd"
          value={umd}
          onChange={(e) => setUmd(e.target.value)}
        />
      </div>
      <br />
      <button className="btn btn-primary" onClick={handleSearch} disabled={loading}>
        {loading ? "Searching..." : "Find"}
      </button>

      <div className="mt-4">
        <button
          className={`btn ${showFireStations ? "btn-primary" : "btn-secondary"}`}
          onClick={() => {
            setShowFireStations(true);
            setShowHospitals(false);
          }}
        >
          Fire Stations
        </button>{" "}
        <button
          className={`btn ${showHospitals ? "btn-primary" : "btn-secondary"}`}
          onClick={() => {
            setShowFireStations(false);
            setShowHospitals(true);
          }}
        >
          Hospitals
        </button>
      </div>

      <div id="map" style={{ height: "400px", marginTop: "20px" }}></div>

      <h2 className="mt-4">Result:</h2>
      {loading && <p>Loading...</p>}
      {error && <p>{error}</p>}
      {!loading && !error && results.length === 0 && <p>No results found.</p>}
      {!loading && !error && results.length > 0 && (
        <ul className="list-group">
          {results.map((address, index) => (
            <li className="list-group-item" key={index}>
              <strong>Address:</strong> {address.sd} {address.sgg} {address.umd} {address.num} <br />
              <strong>Name:</strong> {address.place_name}<br />
              <strong>Phone:</strong> {address.phone}<br />
            </li>
          ))}
        </ul>
      )}

      {selectedMarker && (
        <div>
          <h3>Selected Address:</h3>
          <p>
            <strong>Address:</strong> {selectedMarker.sd} {selectedMarker.sgg} {selectedMarker.umd} {selectedMarker.num}
          </p>
          <p>
            <strong>Name:</strong> {selectedMarker.place_name}
          </p>
          <p>
            <strong>Phone:</strong> {selectedMarker.phone}
          </p>
        </div>
      )}
    </div>
  );
};

export default Kakao;
