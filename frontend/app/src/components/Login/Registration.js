import React, { useState } from 'react';
import axios from 'axios';
// import Styles from '../Styles/Registration.css';
import {Link, useNavigate} from "react-router-dom";
import 'bootstrap/dist/css/bootstrap.min.css'

const Registration = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '', // Добавили поле для повтора пароля
    phone: '',
  });

  const [passwordsMatch, setPasswordsMatch] = useState(true); // Состояние для проверки совпадения паролей

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });

    // Проверяем совпадение паролей при изменении
    if (name === 'password' || name === 'confirmPassword') {
      setPasswordsMatch(formData.password === formData.confirmPassword);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Проверяем совпадение паролей перед отправкой
    if (formData.password !== formData.confirmPassword) {
      setPasswordsMatch(false);
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:8000/auth/register', formData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      console.log('Регистрация успешна:', response.data);
      navigate('/login')
    } catch (error) {
      console.error('Ошибка регистрации:', error);
    }
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <form onSubmit={handleSubmit}>
              <legend>Registration</legend>
              <div className="mb-3">
                <input type="text" name="name" value={formData.name} onChange={handleChange} className="form-control" placeholder="Name" />
              </div>
              <div className="mb-3">
                <input type="email" name="email" value={formData.email} onChange={handleChange} className="form-control" placeholder="Email" />
              </div>
              <div className="mb-3">
                <input type="password" name="password" value={formData.password} onChange={handleChange} className="form-control" placeholder="Password" />
              </div>
              <div className="mb-3">
                <input type="password" name="confirmPassword" value={formData.confirmPassword} onChange={handleChange} className="form-control" placeholder="Repeat password" />
              </div>
              <div className="mb-3">
                <input type="text" name="phone" value={formData.phone} onChange={handleChange} className="form-control" placeholder="Phone" />
              </div>
              <button type="submit" className="btn btn-primary">Register</button>
              {!passwordsMatch && <p className="text-danger mt-2">Passwords do not match.</p>}
          </form>
            <Link to="/login" className="btn btn-link">Back to Login</Link>
        </div>
      </div>
    </div>
  );
};

export default Registration;