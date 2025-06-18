import { createContext, useContext, useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import toast from 'react-hot-toast';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(localStorage.getItem('token'));

  useEffect(() => {
    if (token) {
      try {
        const decoded = jwtDecode(token);
        const currentTime = Date.now() / 1000;
        
        if (decoded.exp < currentTime) {
          // Token expired
          logout();
        } else {
          setUser({
            id: decoded.sub,
            username: decoded.sub,
            userType: decoded.user_type,
            email: decoded.email
          });
        }
      } catch (error) {
        console.error('Error decoding token:', error);
        logout();
      }
    }
    setLoading(false);
  }, [token]);

  const login = async (username, password) => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Login failed');
      }

      const { access_token, user_type } = data;
      
      localStorage.setItem('token', access_token);
      setToken(access_token);
      
      const decoded = jwtDecode(access_token);
      setUser({
        id: decoded.sub,
        username: decoded.sub,
        userType: user_type,
        email: decoded.email
      });

      toast.success(`Welcome back, ${decoded.sub}!`);
      console.log('Login successful, userType:', user_type);
      return { success: true, userType: user_type };
    } catch (error) {
      console.error('Login error:', error);
      toast.error(error.message || 'Login failed');
      return { success: false, error: error.message };
    }
  };

  const register = async (userData) => {
    try {
      console.log('Sending registration request with data:', userData);
      
      const response = await fetch('http://localhost:8000/api/v1/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      const data = await response.json();
      console.log('Registration response:', data);

      if (!response.ok) {
        throw new Error(data.detail || 'Registration failed');
      }

      // After successful registration, automatically log in the user
      const loginResponse = await fetch('http://localhost:8000/api/v1/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          username: userData.username, 
          password: userData.password 
        }),
      });

      const loginData = await loginResponse.json();

      if (!loginResponse.ok) {
        throw new Error(loginData.detail || 'Auto-login failed after registration');
      }

      const { access_token, user_type } = loginData;
      
      localStorage.setItem('token', access_token);
      setToken(access_token);
      
      const decoded = jwtDecode(access_token);
      setUser({
        id: decoded.sub,
        username: decoded.sub,
        userType: user_type,
        email: decoded.email
      });

      toast.success(`Welcome, ${decoded.sub}! Your account has been created successfully.`);
      console.log('Registration and auto-login successful, userType:', user_type);
      return { success: true, userType: user_type };
    } catch (error) {
      console.error('Registration error:', error);
      toast.error(error.message || 'Registration failed');
      return { success: false, error: error.message };
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
    toast.success('Logged out successfully');
  };

  const isAuthenticated = () => {
    return !!user && !!token;
  };

  const hasRole = (role) => {
    return user?.userType === role;
  };

  const value = {
    user,
    loading,
    login,
    register,
    logout,
    isAuthenticated,
    hasRole,
    token
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}; 