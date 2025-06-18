import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Eye, EyeOff, Mail, Lock, User, BookOpen, Sparkles, ArrowRight } from 'lucide-react';

const LoginForm = ({ onToggleForm }) => {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [toggleLoading, setToggleLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Form submitted with data:', formData); // Debug log
    
    // Basic validation
    if (!formData.username || !formData.password) {
      console.log('Validation failed: missing username or password');
      return;
    }
    
    setLoading(true);
    
    try {
      const result = await login(formData.username, formData.password);
      console.log('Login result:', result);
      
      if (result.success) {
        console.log('Navigating to dashboard for user type:', result.userType);
        switch (result.userType) {
          case 'student':
            navigate('/student-home');
            break;
          case 'instructor':
            navigate('/instructor-home');
            break;
          case 'admin':
            navigate('/admin-home');
            break;
          default:
            console.log('Unknown user type, navigating to home');
            navigate('/');
        }
      } else {
        console.log('Login failed:', result.error);
      }
    } catch (error) {
      console.error('Login error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto animate-fade-in">
      {/* Header Section */}
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl mb-6 shadow-lg">
          <BookOpen className="w-10 h-10" />
        </div>
        <h2 className="text-4xl font-bold bg-clip-text mb-3 bg-gradient-to-r from-blue-300 to-blue-400 bg-transparent ">
          Welcome Back
        </h2>
        <p className="text-gray-600 text-lg">Sign in to continue your learning journey</p>
      </div>

      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="form-group">
          <label htmlFor="username" className="form-label">
            Username
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <User className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              className="form-input pl-12"
              placeholder="Enter your username"
              required
            />
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="password" className="form-label">
            Password
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <Lock className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type={showPassword ? 'text' : 'password'}
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              className="form-input pl-12 pr-12"
              placeholder="Enter your password"
              required
            />
            <button
              type="button"
              className="absolute inset-y-0 right-0 pr-4 flex items-center "
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? (
                <EyeOff className="h-5 w-5 text-gray-400" />
              ) : (
                <Eye className="h-5 w-5 text-gray-400" />
              )}
            </button>
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="btn btn-primary btn-full btn-lg"
          onClick={() => console.log('Button clicked!')}
        >
          {loading ? (
            <div className="flex items-center justify-center">
              <div className="loading-spinner mr-3"></div>
              Signing in...
            </div>
          ) : (
            <>
              Sign In
              <ArrowRight className="w-5 h-5 ml-2" />
            </>
          )}
        </button>
      </form>

      {/* Toggle Form */}
      <div className="mt-8 text-center">
        <p className="text-gray-600">
          Don't have an account?{' '}
          <button
            onClick={() => {
              console.log('Sign up here button clicked!');
              setToggleLoading(true);
              setTimeout(() => {
                onToggleForm();
                setToggleLoading(false);
              }, 100);
            }}
            disabled={toggleLoading}
            className="auth-toggle-button"
          >
            {toggleLoading ? 'Loading...' : 'Sign up here'}
          </button>
        </p>
      </div>


      {/* Features */}
      <div className="mt-8 grid grid-cols-1 gap-4">
        <div className="flex items-center p-4 bg-white rounded-xl shadow-sm border border-gray-100">
          <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center mr-4">
            <BookOpen className="w-5 h-5 text-green-600" />
          </div>
          <div>
            <h5 className="font-semibold text-gray-900">Access to 100+ Courses</h5>
            <p className="text-sm text-gray-600">Learn from industry experts</p>
          </div>
        </div>
        <div className="flex items-center p-4 bg-white rounded-xl shadow-sm border border-gray-100">
          <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mr-4">
            <Sparkles className="w-5 h-5 text-blue-600" />
          </div>
          <div>
            <h5 className="font-semibold text-gray-900">Interactive Learning</h5>
            <p className="text-sm text-gray-600">Engage with hands-on projects</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginForm; 