import React, { useState } from 'react';
import axios from 'axios';
import {Link, useNavigate} from "react-router-dom";
import { useAuth } from '../../AuthContext';
import 'bootstrap/dist/css/bootstrap.min.css'

const Login = () => {
  const navigate = useNavigate();
  const { setAuthenticated } = useAuth();
  const [formData, setLoginData] = useState({
    email: '',
    password: '',
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setLoginData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:8000/auth/login', formData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      console.log('Successful:', response.data);

      // При успешной аутентификации сохраняем токен в localStorage
      localStorage.setItem('access_token', response.data.access_token);

      // Устанавливаем состояние аутентификации в true
      setAuthenticated(true);

      // Переход на другую страницу после аутентификации
      navigate('/kakao');
    } catch (error) {
      console.error('Error login:', error);
    }
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <div className="card">
            <div className="card-body">
              <h2 className="card-title" align="center">Login</h2>
              <br/>
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label htmlFor="email" className="form-label">Email</label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    className="form-control"
                    placeholder="Enter your email"
                    value={formData.email}
                    onChange={handleInputChange}
                  />
                </div>
                <div className="mb-3">
                  <label htmlFor="password" className="form-label">Password</label>
                  <input
                    type="password"
                    id="password"
                    name="password"
                    className="form-control"
                    placeholder="Enter your password"
                    value={formData.password}
                    onChange={handleInputChange}
                  />
                </div>
                <button type="submit" className="btn btn-primary">Login</button>
              </form>
              <p className="mt-3">
                Don't have an account? <Link to="/registration">Register</Link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;